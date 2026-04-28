"""Track B — Logic RED (pytest).

구현 없음: 각 테스트는 RED 단계에서 의도적으로 실패한다.
"""

import pytest


class TestFindBlankCoordsRed:
    """LOG-RED-01 — find_blank_coords (row-major, two blanks)."""

    def test_log_red_01_row_major_two_blanks(self) -> None:
        pytest.fail("RED: LOG-RED-01 — find_blank_coords order and count")


class TestFindNotExistNumsRed:
    """LOG-RED-02 — find_not_exist_nums (two missing, ascending)."""

    def test_log_red_02_two_missing_sorted(self) -> None:
        pytest.fail("RED: LOG-RED-02 — missing pair ascending")


class TestIsMagicSquareRed:
    """LOG-RED-03 .. LOG-RED-05 — is_magic_square (rows/cols/diags 34)."""

    def test_log_red_03_true_on_completed_magic_34(self) -> None:
        pytest.fail("RED: LOG-RED-03 — completed 4x4 magic constant 34")

    def test_log_red_04_false_when_line_sum_broken(self) -> None:
        pytest.fail("RED: LOG-RED-04 — not magic when any line != 34")

    def test_log_red_05_false_with_zero_remaining(self) -> None:
        pytest.fail("RED: LOG-RED-05 — incomplete board with 0 is False")


class TestSolutionRed:
    """LOG-RED-06 .. LOG-RED-09 — solution (6-tuple, order, reverse)."""

    def test_log_red_06_returns_six_ints_one_indexed(self) -> None:
        pytest.fail("RED: LOG-RED-06 — len 6, 1-index coords")

    def test_log_red_07_fill_yields_magic_square(self) -> None:
        pytest.fail("RED: LOG-RED-07 — apply n1,n2 then is_magic_square True")

    def test_log_red_08_small_first_on_first_blank_order(self) -> None:
        pytest.fail("RED: LOG-RED-08 — I-10 small→first blank try first")

    def test_log_red_09_reverse_try_after_forward_fails(self) -> None:
        pytest.fail("RED: LOG-RED-09 — reverse assignment when default fails")
