# Tasks: Internet Search RAG with Agent Selection

**Input**: Design documents from `specs/001-rag-internet-search/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Automated tests are included in Phase 5 to verify the RAG logic before manual testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency management

- [x] T001 Install `duckduckgo-search` in `google-adk-venv` and update `requirements.txt`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T002 Implement `SessionState` and basic configuration in `rag_internet_search.py`
- [x] T003 Implement `get_available_gemini_models` using `litellm.model_list` in `rag_internet_search.py`
- [x] T004 Implement `internet_search` wrapper using `duckduckgo-search` in `rag_internet_search.py`

---

## Phase 3: User Story 2 - Agent Selection (Priority: P2)

**Goal**: Allow user to list and select a Gemini agent, defaulting to the latest one.

**Independent Test**: Run script, verify list appears, latest is auto-selected on Enter, or manual selection is stored.

- [x] T005 [US2] Implement `select_agent` CLI prompt and "latest" detection logic in `rag_internet_search.py`

---

## Phase 4: User Story 1 - Basic Internet RAG Search (Priority: P1)

**Goal**: Get concise 2-3 line verified answers with an option for more detail.

**Independent Test**: Ask "Who won the Super Bowl LVIII?", verify 2-3 line answer. Ask "explain", verify more detail.

- [x] T006 [US1] Implement core RAG completion loop with search tool integration in `rag_internet_search.py`
- [x] T007 [US1] Implement 2-3 line answer constraint in system prompt in `rag_internet_search.py`
- [x] T008 [US1] Implement "explain more" command using cached search results in `rag_internet_search.py`

---

## Phase 5: Polish & Validation

**Purpose**: Error handling, performance verification, and final tests.

- [x] T009 Add search failure fallbacks and user-friendly error messages in `rag_internet_search.py`
- [x] T010 [P] Create basic verification tests in `tests/test_rag_search.py`
- [x] T011 Run `tests/test_rag_search.py` and verify all RAG flows pass before manual handoff
- [x] T012 Perform manual verification as described in `specs/001-rag-internet-search/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup (T001).
- **User Stories (Phase 3 & 4)**: Depend on Foundational (Phase 2). 
  - Note: While US1 is P1, US2 (Agent Selection) is the entry point for the CLI flow.
- **Polish (Phase 5)**: Depends on all user story implementations.

### Implementation Strategy

- **MVP First**: Complete T001-T004 and T006-T007 to have a working "fixed agent" search RAG.
- **Incremental Delivery**: Add T005 for selection and T008 for details after MVP.
