"""Track A — UI / Boundary RED (pytest).

구현 없음: 각 테스트는 RED 단계에서 의도적으로 실패한다.
(UI-RED-01은 GREEN: Boundary shape 검증.)
"""

import pytest

from magicsquare.boundary import UIBoundaryError, validate_4x4_shape


class TestUIBoundaryRed:
    """UI-RED-01 .. UI-RED-06 — Report/08, PRD §5."""

    def test_ui_red_01_rejects_non_4x4_shape(self) -> None:
        invalid = (
            [],  # empty
            [[1]],  # 1x1
            [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],  # 3×4
            [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]],  # 4×3
            [[1, 2, 3, 4], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4]],  # ragged
        )
        for board in invalid:
            with pytest.raises(UIBoundaryError) as ctx:
                validate_4x4_shape(board)
            assert ctx.value.code == "UI_INVALID_SHAPE"
            assert ctx.value.message == "Matrix must be 4x4."

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
