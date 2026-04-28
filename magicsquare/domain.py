"""Pure domain rules — no UI, IO, or framework imports."""

from __future__ import annotations

from magicsquare.constants import EMPTY_CELL_VALUE, MATRIX_SIZE


def find_blank_coords(matrix: list[list[int]]) -> list[tuple[int, int]]:
    """Return the two empty cells (value ``0``) in row-major scan order.

    Args:
        matrix: A ``MATRIX_SIZE``×``MATRIX_SIZE`` grid using ``0`` for blanks.

    Returns:
        Exactly two ``(row, col)`` pairs, **0-based** indices, row-major order.
    """
    result: list[tuple[int, int]] = []
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            if matrix[row][col] == EMPTY_CELL_VALUE:
                result.append((row, col))
    return result
