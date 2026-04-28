# Magic Square 4×4 완성 시스템 — 구현 To-Do (Concept-to-Code Traceability)

**역할**: 시니어 아키텍트·TDD 코치용 실습 보드  
**작성 기준일**: 2026-04-28  

---

## 1. 문서·규칙 출처 (읽는 순서)

| 우선순위 | 문서 | To-Do에서 쓰는 내용 |
|:---:|:---|:---|
| **1 (주)** | `Report/05.PRD_Export.md` | 완료 조건, 입·출력·에러 계약, 불변식 I-xx, Dual-Track·MLOps 정렬, 스토리 AC, 검증 §10 |
| **2** | `Report/04.4x4_Magic_Square_Epic_Journey_Stories_Technical_Verification_Report.md` | Epic·여정·스토리·Level 4 Gherkin 시나리오 분해 |
| **3** | `Report/02.4x4_Magic_Square_DualTrack_TDD_CleanArchitecture_Design_Report.md` | ECB 컴포넌트명, T-D-/T-UI-/IT- 테스트 ID, 계약·에러 코드 표 (※에러 우선순위는 **05 PRD**가 최종) |
| **4** | `Report/03.CursorRules_Export.md` | RED/GREEN/REFACTOR 규칙, ECB 금지사항, pytest·커버리지 하한, 의존성 방향 |

**정합성 메모**: `Report/02`에 남아 있는 `MissingNotTwo` 단계·`MissingNumbersNotTwoError`는 **주 소스 05 PRD**와 다를 수 있다. 구현·테스트의 **단일 진실**은 `Report/05.PRD_Export.md` §5.3(우선순위: Shape → EmptyCount → Range → Duplicate → Unsolvable → Data) 및 I-05 파생 설명을 따른다.

---

## 2. 적용 방법론 (요약)

- **Concept-to-Code Traceability**: 각 Task는 **불변식 I-xx / 스토리 / UX 규칙** 중 하나 이상과 연결된다.
- **Dual-Track UI + Logic TDD**: Task에 **Logic Track** 또는 **UI Track**을 명시한다. UI Track은 계약·표현만, Logic Track은 규칙·판정만.
- **To-Do → Scenario → Test → Code**: 각 Task에 Scenario Level, Test 이름, Code 대상을 필수 기재.
- **ECB**: Entity / Control / Boundary 중 하나만 책임으로 둔다.
- **RED → GREEN → REFACTOR**: Phase 필드로 강제한다.

---

## 3. Scenario Level 정의

| 레벨 | 의미 |
|:---:|:---|
| **L0** | 기능 개요(에픽·유스케이스 한 줄) |
| **L1** | 정상 흐름(Happy path) |
| **L2** | 경계·우선순위·결정성 |
| **L3** | 실패·불가·외부 I/O 오류 |

---

## 4. 추적 체인 템플릿

`Epic → User Story → Task(RED|GREEN|REFACTOR) → [L0–L3] → Test → Code(ECB)`  

완료 시 체크박스를 채운다.

---

# EPIC-001 — Invariant 기반 4×4 Magic Square 완성 시스템

**비즈니스 목표** (`Report/04` Level 1): 불변식 기반 사고·Dual-Track TDD·계약 명확화·ECB 준수로 **부분 보드(0 정확히 2칸)** 를 완성하거나 거부한다.

**성공 지표** (`Report/05` §7.2, `Report/04`): Domain Logic 95%+ · UI Boundary 85%+ · Data 80%+ · 계약 테스트 통과 · 하드코딩/매직 넘버 지양(`Report/03`).

---

## US-001 — Story 1: 입력 검증 (계약 위반 시 첫 오류 1개)

**As a** 학습자 **I want** 4×4·빈칸 2·범위·중복이 보장되길 **So that** Domain으로 잘못된 상태가 넘어가지 않는다. (`Report/04` §Level 3 Story 1, `Report/05` §9.1)

### Logic Track — Entity / Domain 검증

- [ ] **TASK-001**  
  - **Phase**: RED  
  - **작업 제목**: 4×4 형태만 허용하는 보드 파싱 실패(I-01)  
  - **Scenario Level**: L3  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_10_invalid_row_count`, `test_TD_11_jagged_row_length` (명칭은 `Report/02` T-D-10, T-D-11에 대응)  
  - **연결 Code**: `entity/matrix4x4.py` — `Matrix4x4.from_raw` / `parse`  
  - **ECB**: **Entity**  
  - **체크포인트**: pytest **실패(RED)** 확인 후 TASK-002로 진행 (`Report/03` tdd_rules.red_phase)

- [ ] **TASK-002**  
  - **Phase**: GREEN  
  - **작업 제목**: I-01 만족 시 `Matrix4x4` 불변 4×4 보유  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_10`… 통과, `test_matrix4x4_valid_fixture_roundtrip`  
  - **연결 Code**: `entity/matrix4x4.py`  
  - **ECB**: **Entity**  
  - **체크포인트**: 최소 구현만 (`Report/03` green_phase)

- [ ] **TASK-003**  
  - **Phase**: RED  
  - **작업 제목**: 빈칸(0) 개수 I-02 위반 시 거부  
  - **Scenario Level**: L3  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_12_one_empty`, `test_TD_13_three_or_more_empties`  
  - **연결 Code**: `entity/input_constraint_validator.py` — `validate_empty_count`  
  - **ECB**: **Entity** (순수 규칙; Control에만 오케스트레이션 두지 말 것)  
  - **체크포인트**: `Report/05` §5.3 `UI_INVALID_EMPTY_COUNT`와 매핑될 도메인 실패 모델 정의

- [ ] **TASK-004**  
  - **Phase**: GREEN  
  - **작업 제목**: I-02 충족 시 통과  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_12_TD_13` 반대 케이스 통과  
  - **연결 Code**: `entity/input_constraint_validator.py`  
  - **ECB**: **Entity**

- [ ] **TASK-005**  
  - **Phase**: RED  
  - **작업 제목**: 셀 값 범위 I-03 위반(-1, 17 등) 거부  
  - **Scenario Level**: L3  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_14_negative`, `test_TD_15_above_16`  
  - **연결 Code**: `entity/input_constraint_validator.py` — `validate_cell_range`  
  - **ECB**: **Entity**

- [ ] **TASK-006**  
  - **Phase**: RED  
  - **작업 제목**: 0 제외 중복 I-04 위반 거부  
  - **Scenario Level**: L3  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_16_duplicate_nonzero`  
  - **연결 Code**: `entity/input_constraint_validator.py` — `validate_unique_nonzero`  
  - **ECB**: **Entity**

- [ ] **TASK-007**  
  - **Phase**: GREEN  
  - **작업 제목**: I-03 경계값 1·16 허용(T-D-30 계열)  
  - **Scenario Level**: L2  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_30_boundary_values_1_and_16`  
  - **연결 Code**: `entity/input_constraint_validator.py`  
  - **ECB**: **Entity**  
  - **체크포인트**: `Report/04` 경계 시나리오, `Report/05` I-03

- [ ] **TASK-008**  
  - **Phase**: REFACTOR  
  - **작업 제목**: 검증 책임 분리·명명 정리(동작 변경 없음)  
  - **Scenario Level**: L0  
  - **트랙**: Logic  
  - **연결 Test**: 기존 전부 유지 통과  
  - **연결 Code**: `entity/input_constraint_validator.py`, `entity/matrix4x4.py`  
  - **ECB**: **Entity**  
  - **체크포인트**: `Report/03` refactor_phase — 커버리지 하락 금지

### UI Track — Boundary (비즈니스 규칙 금지, 계약·매핑만)

- [ ] **TASK-009**  
  - **Phase**: RED  
  - **작업 제목**: 잘못된 크기 입력 → `UI_INVALID_SHAPE` + 고정 `message`  
  - **Scenario Level**: L3  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_01_wrong_row_count`, `test_TUI_02_jagged_columns` (`Report/02` §2.3)  
  - **연결 Code**: `boundary/magic_square_response_builder.py`, `boundary/error_code_mapper.py`  
  - **ECB**: **Boundary**  
  - **체크포인트**: Domain **Mock** — UI 테스트가 알고리즘을 모름 (`Report/05` §4.1)

- [ ] **TASK-010**  
  - **Phase**: RED  
  - **작업 제목**: 빈칸 개수 오류 → `UI_INVALID_EMPTY_COUNT`  
  - **Scenario Level**: L3  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_03_one_zero`, `test_TUI_04_three_zeros`  
  - **연결 Code**: `boundary/magic_square_gateway.py` (입력 스키마 검증만)  
  - **ECB**: **Boundary**

- [ ] **TASK-011**  
  - **Phase**: RED  
  - **작업 제목**: 범위·중복 → `UI_OUT_OF_RANGE`, `UI_DUPLICATE_NON_ZERO`  
  - **Scenario Level**: L3  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_05_out_of_range`, `test_TUI_06_duplicate`  
  - **연결 Code**: `boundary/magic_square_gateway.py`  
  - **ECB**: **Boundary**

- [ ] **TASK-012**  
  - **Phase**: RED  
  - **작업 제목**: 복합 위반 시 **첫 위반 1개**만(`Report/05` §5.3, `Report/02` E-UX-02)  
  - **Scenario Level**: L2  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_31_error_priority_shape_before_empty_before_range` (논리는 `Report/02` T-D-31·우선순위를 **05** 순서로 구현)  
  - **연결 Code**: `boundary/error_code_mapper.py`  
  - **ECB**: **Boundary**

- [ ] **TASK-013**  
  - **Phase**: GREEN  
  - **작업 제목**: Boundary가 검증 실패 시 **Domain 호출 생략** (`Report/02` S-02)  
  - **Scenario Level**: L1  
  - **트랙**: UI  
  - **연결 Test**: `test_boundary_skips_domain_on_invalid_shape` (mock 검증)  
  - **연결 Code**: `boundary/magic_square_gateway.py`  
  - **ECB**: **Boundary**

---

## US-002 — Story 2: 빈칸 탐색 (row-major, 정확히 2좌표)

**AC** (`Report/05` §9.2, `Report/04` Story 2)

- [ ] **TASK-014**  
  - **Phase**: RED  
  - **작업 제목**: row-major 순서로 첫·둘째 빈칸 좌표 산출(UC-01)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_03_empty_cells_row_major_order` (`Report/02` T-D-03)  
  - **연결 Code**: `entity/blank_finder.py` — `find_empty_cells`  
  - **ECB**: **Entity**

- [ ] **TASK-015**  
  - **Phase**: GREEN  
  - **작업 제목**: `Cell` 값 객체·0-index 내부 표현 (`Report/02` §1.1)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_cell_internal_zero_index`  
  - **연결 Code**: `entity/cell.py`  
  - **ECB**: **Entity**

- [ ] **TASK-016**  
  - **Phase**: REFACTOR  
  - **작업 제목**: 빈칸 탐색 API 이름·의존성 정리  
  - **Scenario Level**: L0  
  - **트랙**: Logic  
  - **연결 Test**: TASK-014 테스트 유지  
  - **연결 Code**: `entity/blank_finder.py`  
  - **ECB**: **Entity**

---

## US-003 — Story 3: 누락 숫자·후보값 (1..16 중 정확히 2개 누락)

**AC** (`Report/05` §9.3, I-05는 §6.1 파생) — **후보값 필터링** = 누락 쌍 `(small, large)` 산출

- [ ] **TASK-017**  
  - **Phase**: RED  
  - **작업 제목**: 유효 보드에서 누락 2수 오름차순 산출(UC-02)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_missing_pair_sorted_for_known_partial_board`  
  - **연결 Code**: `entity/missing_numbers_finder.py` — `find_missing_pair`  
  - **ECB**: **Entity**

- [ ] **TASK-018**  
  - **Phase**: GREEN  
  - **작업 제목**: `MissingPair` 값 객체 (`Report/02` §1.1)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_missing_pair_value_object_immutable`  
  - **연결 Code**: `entity/missing_pair.py`  
  - **ECB**: **Entity**

---

## US-004 — Story 4: 마방진 판정 (행·열·대각, 상수 34)

**AC** (`Report/05` §9.4, I-06~I-09)

- [ ] **TASK-019**  
  - **Phase**: RED  
  - **작업 제목**: 완성 그리드에 대해 `is_magic_square` False/True (0 있으면 false 권장, `Report/02` §1.4)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_magic_rule_checker_valid_square`, `test_magic_rule_checker_with_zero_returns_false`  
  - **연결 Code**: `entity/magic_rule_checker.py`, 상수 `MAGIC_SUM = 34` (`Report/03` forbidden 매직 넘버 회피)  
  - **ECB**: **Entity**

- [ ] **TASK-020**  
  - **Phase**: GREEN  
  - **작업 제목**: 행·열·대각 각각 합 34 불만족 시 False (L2 부분 완성 보드)  
  - **Scenario Level**: L2  
  - **트랙**: Logic  
  - **연결 Test**: `test_magic_rule_checker_wrong_row_sum`  
  - **연결 Code**: `entity/magic_rule_checker.py`  
  - **ECB**: **Entity**

---

## US-005 — Story 5: 완성 로직 (두 조합 시도·I-10·해 없음)

**AC** (`Report/05` §9.5, §5.2, `Report/04` Level 4 시나리오)

- [ ] **TASK-021**  
  - **Phase**: RED  
  - **작업 제목**: 기본 배정 성공 시 `n1<n2` 출력(T-D-01)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_01_default_assignment_success_order`  
  - **연결 Code**: `entity/magic_square_completion_policy.py`  
  - **ECB**: **Entity** (정책은 도메인 서비스로 두고 Control은 호출만)

- [ ] **TASK-022**  
  - **Phase**: RED  
  - **작업 제목**: 기본 실패·반대 성공 시 `n1>n2` 가능(T-D-02)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_02_reverse_assignment_success`  
  - **연결 Code**: `entity/magic_square_completion_policy.py`  
  - **ECB**: **Entity**

- [ ] **TASK-023**  
  - **Phase**: RED  
  - **작업 제목**: 두 조합 모두 실패 → 도메인 `UnsolvableMagicSquareError`(또는 동등 실패 타입)  
  - **Scenario Level**: L3  
  - **트랙**: Logic  
  - **연결 Test**: `test_TD_20_both_assignments_fail`  
  - **연결 Code**: `entity/magic_square_completion_policy.py`  
  - **ECB**: **Entity**

- [ ] **TASK-024**  
  - **Phase**: GREEN  
  - **작업 제목**: 성공 시 `int[6]` 1-index 좌표·`n1,n2` 규칙 충족  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_complete_output_length6_one_indexed`  
  - **연결 Code**: `entity/magic_square_completion_policy.py` (또는 `control`에서 조립 시 **좌표 변환만** — 규칙은 Entity)  
  - **ECB**: **Entity** (판정·배정) + 필요 시 **Control**에서 배열만 조립 (`Report/03` control 정의 준수)

- [ ] **TASK-025**  
  - **Phase**: REFACTOR  
  - **작업 제목**: `FillAttempt` 등 값 객체로 시도 단위 캡슐화 (`Report/02` §1.1)  
  - **Scenario Level**: L0  
  - **트랙**: Logic  
  - **연결 Test**: TASK-021~023 유지  
  - **연결 Code**: `entity/fill_attempt.py`, `magic_square_completion_policy.py`  
  - **ECB**: **Entity**

---

## US-006 — Control: 검증·해결 흐름 조율 (Boundary / Entity 사이)

**제약** (`Report/03`, `Report/05` §8): Control은 **오케스트레이션**만; 마방진 판정·배정 규칙은 Entity에 둔다.

- [ ] **TASK-026**  
  - **Phase**: RED  
  - **작업 제목**: `CompleteMagicSquareUseCase` — 검증 → 빈칸 → 누락 → 완성 시도 순서 고정  
  - **Scenario Level**: L0  
  - **트랙**: Logic  
  - **연결 Test**: `test_use_case_happy_path_delegates_to_entity`  
  - **연결 Code**: `control/complete_magic_square_use_case.py`  
  - **ECB**: **Control**  
  - **체크포인트**: Boundary에서 IO 금지 (`Report/03` control.must_not)

- [ ] **TASK-027**  
  - **Phase**: GREEN  
  - **작업 제목**: 도메인 실패를 Boundary가 매핑 가능한 결과 타입으로 전달(Result/Either)  
  - **Scenario Level**: L1  
  - **트랙**: Logic  
  - **연결 Test**: `test_use_case_propagates_unsolvable`  
  - **연결 Code**: `control/complete_magic_square_use_case.py`  
  - **ECB**: **Control**

- [ ] **TASK-028**  
  - **Phase**: REFACTOR  
  - **작업 제목**: Control이 Entity 구체 클래스에 직접 결합되지 않도록 포트(인터페이스) 도입 여부 검토  
  - **Scenario Level**: L0  
  - **트랙**: Logic  
  - **연결 Test**: 동작 동일  
  - **연결 Code**: `control/complete_magic_square_use_case.py`  
  - **ECB**: **Control**

---

## US-007 — Boundary: 성공 응답·에러 매핑·Dual-Track 통합

**AC** (`Report/05` §5.2~5.3, §9.1 UI Track, `Report/02` §2.2~2.3)

- [ ] **TASK-029**  
  - **Phase**: RED  
  - **작업 제목**: Domain 성공 `int[6]` → `result`만 포함(UX-01, T-UI-10, T-UI-11)  
  - **Scenario Level**: L1  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_10_TUI_11_success_payload_shape`  
  - **연결 Code**: `boundary/magic_square_response_builder.py`  
  - **ECB**: **Boundary**

- [ ] **TASK-030**  
  - **Phase**: RED  
  - **작업 제목**: Domain “해 없음” → `UI_UNSOLVABLE` (T-UI-20)  
  - **Scenario Level**: L3  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_20_unsolvable_mapping`  
  - **연결 Code**: `boundary/error_code_mapper.py`  
  - **ECB**: **Boundary**

- [ ] **TASK-031**  
  - **Phase**: GREEN  
  - **작업 제목**: 실패 시 `error`만·성공 시 `result`만(UX-02)  
  - **Scenario Level**: L2  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_exclusive_result_or_error`  
  - **연결 Code**: `boundary/magic_square_response_builder.py`  
  - **ECB**: **Boundary**

---

## US-008 — Data(선택)·통합·테스트 커버리지 체크포인트

**참조** (`Report/02` §3, `Report/05` §10.1, `Report/03` testing)

### Data (Boundary가 규칙 판단 금지)

- [ ] **TASK-032**  
  - **Phase**: RED  
  - **작업 제목**: `MatrixRepository` save/load 라운드트립(T-DATA-01)  
  - **Scenario Level**: L1  
  - **트랙**: Logic (I/O 어댑터; ECB에서는 **Data 경계**로 별 패키지 가능 — 스테레오타입은 **Boundary**에 가깝되 저장만 담당)  
  - **연결 Test**: `test_TDATA_01_roundtrip`  
  - **연결 Code**: `data/matrix_repository.py` (또는 `boundary/persistence_adapter.py`가 포트 구현)  
  - **ECB**: **Boundary** (외부 I/O) — 도메인 규칙 **금지** (`Report/02` §3.1 금지 범위)  
  - **체크포인트**: `Report/03` — 테스트는 결정적, 외부 의존 최소

- [ ] **TASK-033**  
  - **Phase**: RED  
  - **작업 제목**: 저장/로드 실패 → `UI_DATA_ERROR` (IT-NG-03, `Report/05` 표)  
  - **Scenario Level**: L3  
  - **트랙**: UI  
  - **연결 Test**: `test_TUI_data_error_on_io_failure`  
  - **연결 Code**: `boundary/error_code_mapper.py`  
  - **ECB**: **Boundary**

### 통합 (Concept → E2E)

- [ ] **TASK-034**  
  - **Phase**: GREEN  
  - **작업 제목**: IT-OK-01 기본 배정 성공 End-to-End (`Report/02` §4.2)  
  - **Scenario Level**: L1  
  - **트랙**: UI + Logic (통합)  
  - **연결 Test**: `test_IT_OK_01_default_assignment`  
  - **연결 Code**: `tests/integration/test_flow_ok01.py` + 실제 Gateway+UseCase+Entity 연결  
  - **ECB**: **Control** + **Boundary** + **Entity** (통합은 전 레이어)  
  - **체크포인트**: `Report/04` Level 4 표 예시 보드 사용

- [ ] **TASK-035**  
  - **Phase**: GREEN  
  - **작업 제목**: IT-OK-02 반대 배정 성공  
  - **Scenario Level**: L1  
  - **트랙**: UI + Logic  
  - **연결 Test**: `test_IT_OK_02_reverse_assignment`  
  - **연결 Code**: 동상  
  - **ECB**: (통합)

- [ ] **TASK-036**  
  - **Phase**: GREEN  
  - **작업 제목**: IT-NG-01 입력 오류 시 Domain 미호출 (`Report/02` §4.2)  
  - **Scenario Level**: L3  
  - **트랙**: UI  
  - **연결 Test**: `test_IT_NG_01_three_zeros_no_domain_call`  
  - **연결 Code**: `boundary/magic_square_gateway.py`  
  - **ECB**: **Boundary**

- [ ] **TASK-037**  
  - **Phase**: GREEN  
  - **작업 제목**: IT-NG-02 `UI_UNSOLVABLE`  
  - **Scenario Level**: L3  
  - **트랙**: UI + Logic  
  - **연결 Test**: `test_IT_NG_02_unsolvable_board`  
  - **연결 Code**: 통합  
  - **ECB**: (통합)

### 커버리지·회귀 (품질 게이트)

- [ ] **TASK-038**  
  - **Phase**: REFACTOR  
  - **작업 제목**: Domain 라인 커버리지 **≥95%** 달성 (`Report/05` §7.2)  
  - **Scenario Level**: L0  
  - **트랙**: Logic  
  - **연결 Test**: `pytest --cov=entity --cov-fail-under=95` (패키지 경로는 실제 트리에 맞게 조정)  
  - **연결 Code**: `entity/` 전체  
  - **ECB**: **Entity**  
  - **체크포인트**: 미달 시 **기능 추가 없이** 테스트 보강 또는 도달 불가 dead code 제거 (`Report/03`)

- [ ] **TASK-039**  
  - **Phase**: REFACTOR  
  - **작업 제목**: Boundary 커버리지 **≥85%** (`Report/05` §7.2)  
  - **Scenario Level**: L0  
  - **트랙**: UI  
  - **연결 Test**: `pytest --cov=boundary --cov-fail-under=85`  
  - **연결 Code**: `boundary/`  
  - **ECB**: **Boundary**

- [ ] **TASK-040**  
  - **Phase**: REFACTOR  
  - **작업 제목**: Data(선택 구현 시) **≥80%** + T-DATA-03~04  
  - **Scenario Level**: L2  
  - **트랙**: UI  
  - **연결 Test**: `test_TDATA_03_missing_file`, `test_TDATA_04_corrupt_json`  
  - **연결 Code**: `data/matrix_repository.py`  
  - **ECB**: **Boundary**

- [ ] **TASK-041**  
  - **Phase**: REFACTOR  
  - **작업 제목**: Traceability 표 갱신 — I-xx ↔ Test ID ↔ 모듈 (`Report/02` §4.5 형식, `Report/05` §10.2)  
  - **Scenario Level**: L0  
  - **트랙**: Logic  
  - **연결 Test**: (문서/스크립트 검증, 선택) `test_traceability_matrix_script`  
  - **연결 Code**: `docs/TRACEABILITY.md` 또는 `Report/07.*` (팀 규칙에 따름)  
  - **ECB**: (문서)  
  - **체크포인트**: `Report/02` R-01~R-04 회귀 정책

---

## 5. 보드 생성·표현 — 요약 매핑 (요청 최소 항목)

| 요청 최소 항목 | 대표 Task | 주된 ECB |
|:---|:---:|:---:|
| 보드 생성 | TASK-001~002 | Entity |
| 보드 유효성 검사 | TASK-003~008, TASK-009~013 | Entity + Boundary |
| 빈칸 탐지 | TASK-014~016 | Entity |
| 후보값 필터링(누락 2수) | TASK-017~018 | Entity |
| 완성 로직 | TASK-021~025 | Entity |
| 잘못된 입력 처리 | TASK-009~013, TASK-036 | Boundary |
| 테스트 커버리지 체크포인트 | TASK-038~040 | 전층 |

---

## 6. 완료 정의 (Epic 단위 DoD)

- [ ] 모든 **US-001~007** 필수 Task의 체크박스 완료  
- [ ] `Report/05` §5.3 **에러 문구·코드·우선순위**와 통합 테스트 3건 이상 실패/성공 경로 통과  
- [ ] `Report/05` §7.2 커버리지 하한 충족(또는 미구현 Data 제외 시 문서에 예외 기록)  
- [ ] `Report/03` ECB 금지 위반 없음(리뷰 체크리스트)  

---

*본 문서는 `Report/05.PRD_Export.md`를 주 소스로 하며, 스토리·시나리오는 `Report/04`, 계약·테스트 ID는 `Report/02`, 품질·TDD·ECB는 `Report/03`을 보조 소스로 한다.*
