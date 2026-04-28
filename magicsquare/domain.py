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


def find_not_exist_nums(matrix: list[list[int]]) -> list[int]:
    """Return the two missing numbers from 1..(MATRIX_SIZE**2), ascending.

    This assumes the public contract holds (shape is MATRIX_SIZE×MATRIX_SIZE,
    values are 0 or 1..MATRIX_SIZE**2, 0 count is exactly two, and non-zero
    values are unique).
    """
    full = set(range(1, (MATRIX_SIZE * MATRIX_SIZE) + 1))
    present: set[int] = set()
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            value = matrix[row][col]
            if value != EMPTY_CELL_VALUE:
                present.add(value)
    missing = sorted(full - present)
    return missing
