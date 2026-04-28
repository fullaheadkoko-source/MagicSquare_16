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
from magicsquare.constants import MATRIX_SIZE


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
                edit.setPlaceholderText("0")
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

            raise ValueError(
                "Solver is not implemented yet (next GREEN commits will add solve())."
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

