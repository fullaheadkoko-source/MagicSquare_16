"""Input validation and UI-facing error contracts — no PyQt."""

from __future__ import annotations

from magicsquare.constants import MATRIX_SIZE

_CODE_UI_INVALID_SHAPE = "UI_INVALID_SHAPE"
_MSG_INVALID_SHAPE = f"Matrix must be {MATRIX_SIZE}x{MATRIX_SIZE}."


class UIBoundaryError(Exception):
    """Raised when input violates the public boundary contract."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


def validate_4x4_shape(matrix: list[list[int]]) -> None:
    """Reject inputs whose outer shape is not ``MATRIX_SIZE``×``MATRIX_SIZE``.

    Args:
        matrix: Candidate puzzle grid.

    Raises:
        UIBoundaryError: ``UI_INVALID_SHAPE`` with PRD message if shape invalid.
    """
    if len(matrix) != MATRIX_SIZE:
        raise UIBoundaryError(_CODE_UI_INVALID_SHAPE, _MSG_INVALID_SHAPE)
    for row in matrix:
        if len(row) != MATRIX_SIZE:
            raise UIBoundaryError(_CODE_UI_INVALID_SHAPE, _MSG_INVALID_SHAPE)
