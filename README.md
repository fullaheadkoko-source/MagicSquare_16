# MagicSquare (4×4, 빈칸 2개)

부분적으로 채워진 **4×4 마방진**에서 `0`인 두 칸에 누락된 두 수를 배정해 **행·열·대각선 합 34**를 만족시키거나, 계약 위반·해 없음을 **표준 코드·문구**로 반환하는 학습용 시스템입니다.

---

## 문서 관계 (한 줄)

**`Report/05.PRD_Export.md`**는 **`docs/PRD.md`**와 내용을 맞춘 **PRD보내기**이며, 입·출력·에러·불변식·검증의 **공식 스펙 사본**으로 쓰입니다.

---

## 무엇을 기준으로 개발할까

| 구분 | 기준 문서 |
|:---|:---|
| **본문·To-Do·검증 기준(중심)** | [`docs/Magic_Square_Implementation_TODO_Traceability.md`](docs/Magic_Square_Implementation_TODO_Traceability.md) — EPIC/US/TASK, RED/GREEN/REFACTOR, 시나리오 레벨 L0–L3, 테스트·코드 추적 |
| **스토리 표현 (As a / AC)** | [`Report/04.4x4_Magic_Square_Epic_Journey_Stories_Technical_Verification_Report.md`](Report/04.4x4_Magic_Square_Epic_Journey_Stories_Technical_Verification_Report.md) |
| **오류·계약·테스트 ID 요약** | [`Report/02.4x4_Magic_Square_DualTrack_TDD_CleanArchitecture_Design_Report.md`](Report/02.4x4_Magic_Square_DualTrack_TDD_CleanArchitecture_Design_Report.md) — **에러 우선순위·I-05는 `docs/PRD.md` / `Report/05`가 최종** |
| **실행·ECB·TDD·커버리지** | [`Report/03.CursorRules_Export.md`](Report/03.CursorRules_Export.md) + 프로젝트 루트 **`.cursorrules`** |
| **빌드 메타** | 루트에 **`pyproject.toml`이 생기면** 의존성·스크립트(`pytest`, `ruff` 등)는 그 파일을 따릅니다. *(현재 저장소에는 없을 수 있음.)* |

---

## 사용자 스토리 개요 (`Report/04` Level 3)

| # | 한 줄 |
|:---:|:---|
| **1** | **입력 검증** — 4×4, 빈칸(`0`) 2개, `0` 또는 1..16, 0 제외 중복 없음 |
| **2** | **빈칸 탐색** — row-major로 정확히 두 좌표 |
| **3** | **누락 숫자** — 1..16 중 빠진 두 수, 오름차순 |
| **4** | **마방진 판정** — 행·열·두 대각선 합 일치(완성 시 34) |
| **5** | **두 조합 시도** — small→첫 빈칸 먼저, 실패 시 reverse, 성공 시 길이 6 배열 |

---

## 계약·오류 요약 (`Report/02` + 최종 PRD `docs/PRD.md` / `Report/05`)

### 입력 (요약)

- 정수 **4×4**, 값은 **`0` 또는 1..16**, **`0`은 정확히 2개**, 0 제외 **중복 없음**.

### 성공 출력

- **`int[6]`**: `[r1, c1, n1, r2, c2, n2]` — 좌표는 **1-index**, `n1`·`n2` 순서는 PRD §5.2 결정 규칙 따름.

### 표준 에러 (`code` / `message` 문자열 완전 일치)

| code | message (정확히 일치) |
|:---|:---|
| `UI_INVALID_SHAPE` | `Matrix must be 4x4.` |
| `UI_INVALID_EMPTY_COUNT` | `Matrix must contain exactly 2 empty cells (0).` |
| `UI_OUT_OF_RANGE` | `Cell values must be 0 or 1..16.` |
| `UI_DUPLICATE_NON_ZERO` | `Non-zero values must be unique.` |
| `UI_UNSOLVABLE` | `No magic square completion exists for this input.` |
| `UI_DATA_ERROR` | `Failed to persist or load the matrix.` *(선택 Data 기능 시)* |

**우선순위 (첫 위반 1개만):** Shape → EmptyCount → Range → Duplicate → Unsolvable → Data  

**I-05**(누락 정확히 2개)는 위 입력 계약이 만족되면 **도출**되므로 별도 에러 단계 없음 (`docs/PRD.md` §5.3).

---

## 실행·품질 (`Report/03` + `.cursorrules` + `pyproject.toml`)

- **언어**: Python **3.10+**
- **테스트**: **pytest**, AAA, 테스트명 `test_` 접두사
- **커버리지 하한**: 전체 **80%** 이상; 레이어별 목표는 To-Do 문서 및 PRD §7.2 (Domain 95%+ / Boundary 85%+ / Data 80%+)
- **TDD**: RED → GREEN → REFACTOR 순서 준수, 테스트 없이 구현 추가 금지
- **`pyproject.toml` 추가 후** 권장 예시 (프로젝트 구조에 맞게 조정):

```bash
python -m pytest
python -m pytest --cov=entity --cov=boundary --cov-fail-under=80
```

---

## GUI 실행 (PyQt6)

```bash
python -m pip install -e ".[gui]"
python -m magicsquare
```

---

## ECB (`.cursorrules` / `Report/03`)

| 스테레오타입 | 책임 | 하지 말 것 |
|:---:|:---|:---|
| **Boundary** | 입출력 파싱·스키마 검증·결과/에러 포맷·IO 어댑터 | 마방진 판정·완성 알고리즘, Entity 내부 우회 의존 |
| **Control** | 유스케이스 오케스트레이션, Entity 조합, Boundary용 결과 구성 | 직접 IO |
| **Entity** | 4×4 상태·불변식·순수·결정적 규칙 | 프레임워크·IO |

**의존성:** `boundary → control → entity` 만 허용 (`control → boundary`, `entity → control` 등 금지).

---

## 검증 기준 (요약, 상세는 To-Do 문서)

- **통합**: 기본 배정 성공·반대 배정 성공·입력 오류·`UI_UNSOLVABLE`·(선택) Data 실패 등 **성공/실패 경로** (`Report/02` IT-* 시나리오, To-Do TASK-034~037).
- **추적성**: 불변식 I-xx ↔ 테스트 ↔ 모듈 (`docs/Magic_Square_Implementation_TODO_Traceability.md` §6 DoD, TASK-038~041).
- **회귀**: PRD에 고정된 **문구·우선순위·출력 포맷** 변경 시 테스트가 깨지는 것이 정상인 경우가 있음 (`docs/PRD.md` §7.3).

---

## 구현 To-Do 리스트 (체크박스·단계별 번호·추적 매트릭스)

**원본 보드(전 TASK 메타·코드 경로)**는 반드시 [`docs/Magic_Square_Implementation_TODO_Traceability.md`](docs/Magic_Square_Implementation_TODO_Traceability.md)와 함께 갱신합니다.  
아래 README 블록은 **실습 보드용 요약**이며, **Task → Req → Scenario(L1/L2/L3) → Test** 연결이 **Concept-to-Code Traceability** 연습용 골격입니다.

### 번호·표기 규칙

- **Epic → User Story → Task** 순으로 들여쓰기합니다.
- 한 Task 안에서 TDD를 쪼갤 때는 **`TASK-xxx-y`** 형식으로 **RED → GREEN → (필요 시) REFACTOR** 하위 단계를 둡니다.
- **Req ID**는 PRD 불변식·계약을 가리키는 **추적용 라벨**입니다 (아래 표).

### Req ID 범례 (요구 ↔ PRD)

| Req ID | 연결 (PRD / 도메인) |
|:---|:---|
| **REQ-001** | I-01 — 입력 4×4 형태 |
| **REQ-002** | I-02 — 빈칸(`0`) 정확히 2개 |
| **REQ-003** | I-03 — 값 0 또는 1..16 |
| **REQ-004** | I-04 — 0 제외 중복 없음 |
| **REQ-005** | I-05 — 누락 수 2개 (I-02~04에서 파생, 별도 에러 없음) |
| **REQ-006~009** | I-06~I-09 — 마방진 합·행·열·대각 |
| **REQ-010** | I-10 — `n1,n2` 결정적 순서 |
| **REQ-011** | 해 없음 → `UI_UNSOLVABLE` 계열 |
| **REQ-ERR** | §5.3 표준 `code`/`message`·우선순위 |
| **REQ-UX** | 성공 시 `result`만 / 실패 시 `error`만 (PRD·Report/02 UX 규칙) |

---

### EPIC-001 — Invariant 기반 4×4 Magic Square 완성 시스템

> 목표: `Report/04` Epic과 동일 — 계약된 입력만 Domain으로, 성공 시 `int[6]`, 실패 시 첫 위반 1건.

- [ ] **US-001** — Story 1: 입력 검증 (Logic + UI Dual-Track)

  - [ ] **TASK-001~002** — `Matrix4x4` 보드 생성·형태 고정 (**Entity**, REQ-001)
    - [ ] **TASK-001-1** **RED** — `test_TD_10_invalid_row_count`, `test_TD_11_jagged_row_length` 실패 확인
    - [ ] **TASK-001-2** **GREEN** — `entity/matrix4x4.py` 최소 구현으로 위 테스트 통과
  - [ ] **TASK-003~004** — 빈칸 개수 검증 (**Entity**, REQ-002)
    - [ ] **TASK-003-1** **RED** — `test_TD_12_one_empty`, `test_TD_13_three_or_more_empties`
    - [ ] **TASK-003-2** **GREEN** — 정상 2빈칸 보드 통과
  - [ ] **TASK-005** — 값 범위 I-03 (**Entity**, REQ-003) — *RED 단일 Task이면 테스트 먼저*
  - [ ] **TASK-006** — 0 제외 중복 I-04 (**Entity**, REQ-004)
  - [ ] **TASK-007** — 경계 1·16 허용 (**Entity**, REQ-003, **L2**)
  - [ ] **TASK-008** — **REFACTOR** — `input_constraint_validator` / `matrix4x4` 책임·이름 정리 (동작 동일)

  - [ ] **TASK-009~012** — Boundary 입력 검증·에러 매핑 (**Boundary**, REQ-ERR, Dual-Track **UI**)
    - [ ] **TASK-009-1** **RED** — `UI_INVALID_SHAPE` + 고정 `message` (`test_TUI_01`, `test_TUI_02`)
    - [ ] **TASK-010-1** **RED** — `UI_INVALID_EMPTY_COUNT` (`test_TUI_03`, `test_TUI_04`)
    - [ ] **TASK-011-1** **RED** — `UI_OUT_OF_RANGE`, `UI_DUPLICATE_NON_ZERO` (`test_TUI_05`, `test_TUI_06`)
    - [ ] **TASK-012-1** **RED** — 복합 위반 시 **첫 위반 1개** (`test_TUI_31_error_priority`)
  - [ ] **TASK-013** — **GREEN** — 검증 실패 시 Domain **미호출** (`test_boundary_skips_domain_on_invalid_shape`)

- [ ] **US-002** — Story 2: 빈칸 탐색 (row-major)

  - [ ] **TASK-014** — `find_empty_cells` (**Entity**, REQ-002, UC-01)
    - [ ] **TASK-014-1** **RED** — `test_TD_03_empty_cells_row_major_order` 실패 확인
    - [ ] **TASK-014-2** **GREEN** — `entity/blank_finder.py` 구현
  - [ ] **TASK-015** — `Cell` 값 객체 (**Entity**, **L1**)
  - [ ] **TASK-016** — **REFACTOR** — 빈칸 API·의존성 정리

- [ ] **US-003** — Story 3: 누락 숫자·후보 `(small, large)`

  - [ ] **TASK-017** — **RED** — `test_missing_pair_sorted_for_known_partial_board` (**Entity**, REQ-005)
  - [ ] **TASK-018** — **GREEN** — `MissingPair` 값 객체 (`entity/missing_pair.py`)

- [ ] **US-004** — Story 4: 마방진 판정

  - [ ] **TASK-019** — `MagicRuleChecker` (**Entity**, REQ-006~009)
    - [ ] **TASK-019-1** **RED** — 완성 보드 True / `0` 포함 시 False 등
    - [ ] **TASK-019-2** **GREEN** — `MAGIC_SUM = 34` 상수화 (`Report/03` 매직 넘버 금지)
  - [ ] **TASK-020** — **GREEN** — 잘못된 합 **L2** 케이스 (`test_magic_rule_checker_wrong_row_sum`)

- [ ] **US-005** — Story 5: 완성·두 조합·`int[6]` 출력

  - [ ] **TASK-021~025** — `MagicSquareCompletionPolicy` (**Entity**, REQ-010, REQ-011)
    - [ ] **TASK-021-1** **RED** — 기본 배정 성공 `n1<n2` (`test_TD_01_default_assignment_success_order`)
    - [ ] **TASK-022-1** **RED** — 반대 배정 성공 (`test_TD_02_reverse_assignment_success`)
    - [ ] **TASK-023-1** **RED** — 두 조합 실패 (`test_TD_20_both_assignments_fail`)
    - [ ] **TASK-024-1** **GREEN** — `int[6]`·1-index·순서 규칙 (`test_complete_output_length6_one_indexed`)
    - [ ] **TASK-025-1** **REFACTOR** — `FillAttempt` 등 값 객체 분리

- [ ] **US-006** — Control: 유스케이스 오케스트레이션

  - [ ] **TASK-026** — **RED** — `CompleteMagicSquareUseCase` 흐름 고정 (`test_use_case_happy_path_delegates_to_entity`)
  - [ ] **TASK-027** — **GREEN** — Unsolvable 등 결과 타입 전달 (`test_use_case_propagates_unsolvable`)
  - [ ] **TASK-028** — **REFACTOR** — 포트 도입 여부·의존성 방향 점검 (`boundary → control → entity`만)

- [ ] **US-007** — Boundary: Dual-Track UI (성공/실패 페이로드)

  - [ ] **TASK-029** — **RED** — 성공 시 `result`만 (T-UI-10, T-UI-11, **REQ-UX**)
  - [ ] **TASK-030** — **RED** — `UI_UNSOLVABLE` 매핑 (T-UI-20, **REQ-011**)
  - [ ] **TASK-031** — **GREEN** — `error` vs `result` 상호 배제 (T-UI exclusive)

- [ ] **US-008** — Data(선택)·통합·커버리지 게이트

  - [ ] **TASK-032~033** — 저장/로드·`UI_DATA_ERROR` (선택, **Boundary** I/O)
  - [ ] **TASK-034~037** — 통합 IT-OK-01/02, IT-NG-01/02 (**L1/L3**)
  - [ ] **TASK-038~040** — **REFACTOR** — 커버리지 entity ≥95%, boundary ≥85%, data ≥80% (선택 시)
  - [ ] **TASK-041** — **REFACTOR** — I-xx ↔ Test ↔ 모듈 추적 표 갱신 (`Report/02` §4.5 형식)

---

### Requirements 추적 매트릭스 (요약)

구현이 진행될수록 **상태** 열을 ✅ 통과 / 🔴 RED(테스트만 존재) / ⬜ 미착수 등으로 바꿉니다.

| Task ID | Req ID | Scenario | 테스트 (대표) | 상태 |
|:---|:---|:---|:---|:---:|
| TASK-001~002 | REQ-001 | L3 Fail / L1 Happy | `test_TD_10`, `test_TD_11` | ⬜ |
| TASK-003~004 | REQ-002 | L3 / L1 | `test_TD_12`, `test_TD_13` | ⬜ |
| TASK-005 | REQ-003 | L3 | `test_TD_14`, `test_TD_15` | ⬜ |
| TASK-006 | REQ-004 | L3 | `test_TD_16` | ⬜ |
| TASK-007 | REQ-003 | L2 Edge | `test_TD_30` | ⬜ |
| TASK-009~012 | REQ-ERR | L2/L3 | `test_TUI_01` … `test_TUI_31` | ⬜ |
| TASK-014 | REQ-002 | L1 | `test_TD_03` | ⬜ |
| TASK-017 | REQ-005 | L1 | `test_missing_pair_sorted_*` | ⬜ |
| TASK-019 | REQ-006~009 | L1/L2 | `test_magic_rule_checker_*` | ⬜ |
| TASK-021~024 | REQ-010, REQ-011 | L1/L3 | `test_TD_01`, `test_TD_02`, `test_TD_20`, `test_complete_output_*` | ⬜ |
| TASK-026 | REQ-001~011 | L0 개요 | `test_use_case_happy_path_*` | ⬜ |
| TASK-029~031 | REQ-UX, REQ-011 | L1/L2/L3 | `test_TUI_10`, `test_TUI_20`, `test_TUI_exclusive_*` | ⬜ |
| TASK-034~037 | 통합 | L1/L3 | `test_IT_OK_01`, `test_IT_NG_01` 등 | ⬜ |
| TASK-038~040 | §7.2 NFR | L0 게이트 | `pytest --cov=...` | ⬜ |

**Traceability:** `Task → Req → Scenario(L0–L3) → Test → Code` 한 줄이 곧 **C2C Traceability** 실습 단위입니다. (시나리오 레벨 정의는 [`docs/Magic_Square_Implementation_TODO_Traceability.md`](docs/Magic_Square_Implementation_TODO_Traceability.md) §3.)

---

### Epic 완료 정의 (DoD)

- [ ] 위 **US-001~007** 필수 Task·하위 RED/GREEN/REFACTOR 단계 완료
- [ ] 추적 매트릭스에서 **통합 행(TASK-034~037)** 이 ✅
- [ ] PRD §5.3 **에러 문구·우선순위**와 충돌 없음 (회귀 테스트로 고정)
- [ ] PRD §7.2 **커버리지** 목표 충족 (Data 미구현 시 README 또는 To-Do 문서에 예외 명시)
- [ ] `.cursorrules` / `Report/03` 기준 **ECB·TDD 순서** 위반 없음

---

## 저장소 안내

| 경로 | 설명 |
|:---|:---|
| `docs/PRD.md` | PRD 원본 |
| `docs/Magic_Square_Implementation_TODO_Traceability.md` | **구현 보드 (본 README의 중심)** |
| `Report/` | 설계·여정·규칙보내기·PRD Export·[납품 현황 `06`](Report/06.Project_Documentation_Delivery_Update.md)·[테스트 케이스 명세 `07`](Report/07.Test_Case_Specification_MS16_Form.md) |
| `Prompting/` | 문서 작성용 프롬프트 등 |

---

*Dual-Track UI + Logic TDD, Concept-to-Code Traceability, ECB는 To-Do 문서 §2와 `docs/PRD.md` §4를 참고하세요.*
