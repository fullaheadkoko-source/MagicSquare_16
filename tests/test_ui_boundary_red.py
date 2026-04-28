"""Track A — UI / Boundary RED (pytest).

구현 없음: 각 테스트는 RED 단계에서 의도적으로 실패한다.
"""

import pytest


class TestUIBoundaryRed:
    """UI-RED-01 .. UI-RED-06 — Report/08, PRD §5."""

    def test_ui_red_01_rejects_non_4x4_shape(self) -> None:
        pytest.fail("RED: UI-RED-01 — non-4x4 must raise or UI_INVALID_SHAPE")

    def test_ui_red_02_rejects_empty_count_not_two(self) -> None:
        pytest.fail("RED: UI-RED-02 — exactly two zeros; UI_INVALID_EMPTY_COUNT")

    def test_ui_red_03_rejects_out_of_range_values(self) -> None:
        pytest.fail("RED: UI-RED-03 — 1..16 (0 empty only); UI_OUT_OF_RANGE")

    def test_ui_red_04_rejects_duplicate_non_zero(self) -> None:
        pytest.fail("RED: UI-RED-04 — unique non-zero; UI_DUPLICATE_NON_ZERO")

    def test_ui_red_05_solution_returns_length_six(self) -> None:
        pytest.fail("RED: UI-RED-05 — success path int[6]")

    def test_ui_red_06_solution_coordinates_one_indexed(self) -> None:
        pytest.fail("RED: UI-RED-06 — r,c in 1..4")
