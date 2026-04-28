"""PyQt6 MVP screen for the 4×4 Magic Square solver."""

from __future__ import annotations

from typing import Final

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary import UIBoundaryError, validate_4x4_shape
from magicsquare.constants import EMPTY_CELL_VALUE, MATRIX_SIZE
from magicsquare.domain import find_blank_coords, find_not_exist_nums

_DEFAULT_MATRIX: Final[list[list[int]]] = [
    [EMPTY_CELL_VALUE, 3, 2, 13],
    [5, EMPTY_CELL_VALUE, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


class MagicSquareWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare 4×4")

        root = QWidget(self)
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)

        self._cells: list[list[QLineEdit]] = []
        grid = QGridLayout()
        layout.addLayout(grid)

        for r in range(MATRIX_SIZE):
            row: list[QLineEdit] = []
            for c in range(MATRIX_SIZE):
                edit = QLineEdit()
                edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                edit.setFixedWidth(48)
                edit.setText(str(_DEFAULT_MATRIX[r][c]))
                grid.addWidget(edit, r, c)
                row.append(edit)
            self._cells.append(row)

        actions = QHBoxLayout()
        layout.addLayout(actions)

        self._solve_btn = QPushButton("풀기")
        self._solve_btn.clicked.connect(self._on_solve_clicked)  # type: ignore[attr-defined]
        actions.addWidget(self._solve_btn)

        self._result_label = QLabel("결과: -")
        self._result_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self._result_label)

        self._hint_label: Final[QLabel] = QLabel(
            "입력: 0은 빈칸(정확히 2개). 현재 커밋은 shape만 검증합니다."
        )
        layout.addWidget(self._hint_label)

    def _read_matrix(self) -> list[list[int]]:
        matrix: list[list[int]] = []
        for r in range(MATRIX_SIZE):
            row: list[int] = []
            for c in range(MATRIX_SIZE):
                raw = self._cells[r][c].text().strip()
                if raw == "":
                    raw = "0"
                row.append(int(raw))
            matrix.append(row)
        return matrix

    def _on_solve_clicked(self) -> None:
        try:
            matrix = self._read_matrix()
            validate_4x4_shape(matrix)

            blanks = find_blank_coords(matrix)
            if len(blanks) != 2:
                raise ValueError(
                    "Matrix must contain exactly 2 empty cells (0)."
                )

            (r1, c1), (r2, c2) = blanks
            r1 += 1
            c1 += 1
            r2 += 1
            c2 += 1

            missing = find_not_exist_nums(matrix)
            if len(missing) != 2:
                raise ValueError("Internal error: expected exactly 2 missing numbers.")
            small, large = missing

            self._result_label.setText(
                "결과: "
                f"빈칸(0) 좌표=({r1},{c1}),({r2},{c2}) / "
                f"들어갈 후보 숫자=({small},{large}) / "
                f"이유=1..{MATRIX_SIZE*MATRIX_SIZE} 중 보드에 없는 값"
            )
        except (UIBoundaryError, ValueError) as exc:
            QMessageBox.warning(self, "입력 오류", str(exc))
        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, "오류", str(exc))


def run() -> None:
    app = QApplication([])
    window = MagicSquareWindow()
    window.show()
    app.exec()

