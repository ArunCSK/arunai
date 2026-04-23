# Task Breakdown Summary

**Feature**: Stock Agent Chat Application  
**Branch**: `001-stock-agent-chat`  
**Total Tasks**: 45  
**Estimated Time**: 10-11 hours (1 dev) | 8-9 hours (2 devs in parallel)

---

## 🎯 Task Overview

```
Phase 1: Setup (6 tasks, 1h)
├─ Project structure
├─ Dependencies 
└─ Testing infrastructure

Phase 2: Foundational (5 tasks, 2.5h) ⚠️ BLOCKING
├─ Stock data generator
├─ Agent initialization
├─ Tool definitions
└─ UI components

Phase 3: US1 - View Prices (5 tasks, 2h) [P] Can start after Phase 2
├─ Tests: data retrieval
├─ Tests: table display
└─ Implementation: dropdown + table

Phase 4: US2 - Chat Interface (6 tasks, 2h) [P] Parallel with Phase 3
├─ Tests: agent interaction
├─ Tests: chat display
└─ Implementation: chat UI + message handling

Phase 5: US3 - Agent Tools (7 tasks, 2h) [P] Parallel with Phase 3-4
├─ Tests: tool execution
├─ Tests: tool integration
├─ Implementation: tool handlers
└─ Tool call display

Phase 6: US4 - UI Polish (5 tasks, 1.5h) [P] After US1-3 functional
├─ Layout design
├─ Styling (company select, table, chat)
└─ Visual feedback & polish

Phase 7: Polish & Release (11 tasks, 1.5h)
├─ Comprehensive testing
├─ Documentation updates
├─ Performance validation
├─ Code cleanup
└─ Git release
```

---

## 📊 Task Distribution

| Phase | Task Count | Time | When to Start |
|-------|-----------|------|---------------|
| 1: Setup | 6 | 1h | Immediately |
| 2: Foundational | 5 | 2.5h | After Phase 1 |
| 3: US1 View Prices | 5 | 2h | After Phase 2 ✓ |
| 4: US2 Chat Interface | 6 | 2h | After Phase 2 ✓ |
| 5: US3 Agent Tools | 7 | 2h | After Phase 2 ✓ |
| 6: US4 UI Polish | 5 | 1.5h | After US1-3 ✓ |
| 7: Polish & Release | 11 | 1.5h | After all stories |
| **TOTAL** | **45** | **10-11h** | |

**✓ = Can run in parallel with other stories**

---

## 🔄 Execution Paths

### Sequential (1 Developer)

1. Do Phase 1 Setup (1h)
2. Do Phase 2 Foundational (2.5h)
3. Do Phase 3 US1 (2h)
4. Do Phase 4 US2 (2h)
5. Do Phase 5 US3 (2h)
6. Do Phase 6 UI Polish (1.5h)
7. Do Phase 7 Release (1.5h)

**Total: 12-13 hours**

### Parallel (2 Developers Recommended)

```
Timeline    | Developer A           | Developer B
────────────┼───────────────────────┼──────────────────────
0-1h        | Phase 1 Setup         | Phase 1 Setup
1-3.5h      | Phase 2 Foundational  | Phase 2 Foundational
3.5-5.5h    | Phase 4 User Story 2  | Phase 3 User Story 1
5.5-7.5h    | Phase 6 UI Polish     | Phase 5 User Story 3
7.5-9h      | Phase 7 Release (A)   | Phase 7 Release (B)
────────────┴───────────────────────┴──────────────────────
Total: ~9h wall-clock time (vs 12-13h sequential)
```

### Tasks That Can Run in Parallel

**Within Phase 1 (Setup)**:
- T003, T004, T005 (independent files)

**Within Phase 2 (Foundational)**:
- T008, T010, T011 can run in parallel with T007, T009

**After Phase 2 (User Stories)**:
- **All three stories (US1, US2, US3) can be implemented simultaneously**
- Different developers can tackle different stories
- No inter-story dependencies until Phase 6 (UI Polish)

**Recommended 2-Person Split**:
- **Person A**: Phases 1, 2A (Foundational part 1), 4 (Chat), 6 (Polish part 1)
- **Person B**: Waits, then Phases 3 (Prices), 5 (Tools), 6 (Polish part 2)

---

## 📋 Task Checklist Format

All tasks follow strict format for clarity:

```
- [ ] [ID] [P?] [Story?] Description with file path
```

Example tasks:

✅ Phase 1:
```
- [ ] T001 Create project directory structure per plan.md in repo root
- [ ] T003 [P] Create .env.example template with configuration variables
```

✅ Phase 2:
```
- [ ] T007 Implement mock stock data generator in src/stock_data.py
- [ ] T010 [P] Define and register tools in src/tools.py
```

✅ Phase 3 (User Story 1):
```
- [ ] T012 [P] [US1] Unit test: test stock data retrieval in tests/test_stock_data.py
- [ ] T014 [P] [US1] Implement stock data retrieval handler for Streamlit in stock_app.py
```

✅ Phase 7:
```
- [ ] T035 [P] Write comprehensive integration test in tests/test_integration.py
- [ ] T038 Update README.md with Stock Agent Chat feature
```

---

## ✅ Success Criteria Per Phase

### After Phase 1:
- ✅ Directory structure created: `src/`, `tests/`, root files
- ✅ `requirements.txt` has all dependencies listed
- ✅ `pytest` is configured and runnable
- ✅ `.gitignore` created

### After Phase 2 (GATE):
- ✅ `src/stock_data.py` generates mock prices w/o errors
- ✅ `src/agent.py` initializes CopilotAgent successfully
- ✅ `src/tools.py` defines 2 tools with handlers registered
- ✅ `src/ui/components.py` functions callable
- ✅ **NOW user stories can begin**

### After Phase 3 (User Story 1):
- ✅ `streamlit run stock_app.py` shows company dropdown
- ✅ Selecting company displays 5-day price table
- ✅ Prices update immediately on selection
- ✅ Invalid company shows friendly error
- ✅ Tests pass: `pytest tests/test_stock_data.py`

### After Phase 4 (User Story 2):
- ✅ Chat input visible in app
- ✅ User can type and submit message
- ✅ Agent responds (may be simple response)
- ✅ Chat history shows previous messages
- ✅ Tests pass: `pytest tests/test_agent.py`

### After Phase 5 (User Story 3):
- ✅ Agent calls `get_stock_data` tool when needed
- ✅ Agent calls `analyze_stock_data` for analysis
- ✅ Tool results incorporated in responses
- ✅ Tool invocations shown in chat
- ✅ Tests pass: `pytest tests/test_tools.py` + `test_integration.py`

### After Phase 6 (User Story 4):
- ✅ UI clean and professional
- ✅ Clear visual separation (stock data | chat)
- ✅ Chat resembles VS Code/GitHub chat
- ✅ Tool invocations clearly highlighted
- ✅ Demo-ready appearance

### After Phase 7 (Release):
- ✅ All tests pass: `pytest tests/` ≥80% coverage
- ✅ No Python warnings or errors
- ✅ Agent response time <3s
- ✅ Price refresh <2s
- ✅ README updated
- ✅ PR ready for review

---

## 🎓 Key Design Decisions Per Task

### Phase 1: Setup
- Minimalist dependencies (Streamlit, Copilot SDK, pytest)
- No external databases or complex packages
- Single `requirements.txt` for all dependencies

### Phase 2: Foundational
- Mock stock data (no API dependency)
- Dataclasses for type safety (not Pydantic)
- Session state for conversation persistence
- Test-first: write tests before implementation

### Phase 3: User Story 1 (Prices)
- Dropdown for company selection (simple, clear)
- Table format for prices (Streamlit native dataframe)
- Immediate refresh (Streamlit rerun on selection)
- Error messages for invalid companies

### Phase 4: User Story 2 (Chat)
- Streamlit's built-in `st.chat_message()` for UI
- Session state list for chat history
- Context passed to agent (company, prices, history)
- Loading indicator while waiting for response

### Phase 5: User Story 3 (Tools)
- Two core tools: get_stock_data, analyze_stock_data
- Tool handlers return success/error dicts (no exceptions)
- Tool results embedded in ChatMessage for transparency
- Tool invocations highlighted in UI

### Phase 6: UI Polish
- Wide layout for side-by-side (data | chat)
- GitHub Copilot chat style as inspiration
- Tool badges 🔧 to show invocations
- Help text and example questions

### Phase 7: Release
- Comprehensive testing (unit + integration) ≥80% coverage
- Documentation in README (single file per Constitution)
- Performance validation (<3s agent, <2s prices)
- Code cleanup and refactoring

---

## 📁 File Structure After All Tasks

```
.
├── stock_app.py                  (150 lines) ← Main entry point
├── requirements.txt              (5 lines)
├── .env.example                  (5 lines)
├── conftest.py                   (pytest config)
│
├── src/
│   ├── __init__.py              (models: StockPrice, Company, ChatMessage, ToolResult)
│   ├── stock_data.py            (100 lines) Stock data + mock generator
│   ├── agent.py                 (150 lines) Copilot SDK initialization
│   ├── tools.py                 (120 lines) Tool definitions + handlers
│   └── ui/
│       ├── __init__.py
│       └── components.py        (180 lines) Streamlit components
│
└── tests/
    ├── conftest.py
    ├── test_stock_data.py       (80 lines)  Data retrieval tests
    ├── test_agent.py            (100 lines) Agent interaction tests
    ├── test_tools.py            (90 lines)  Tool execution tests
    ├── test_ui_components.py    (100 lines) UI component tests
    └── test_integration.py      (120 lines) End-to-end workflows

Total: ~1,150 lines (production + tests)
```

---

## 🚀 Getting Started

### To Begin Development:

1. **Read Phase 1 tasks** in [tasks.md](tasks.md)
2. **Create the structure**:
   ```bash
   git checkout 001-stock-agent-chat
   python -m mkdir src/ui tests
   # Complete T001-T006
   ```
3. **Track progress**: Mark tasks complete as you finish
4. **Run frequently**: `pytest tests/` and `streamlit run stock_app.py`

### Recommended Workflow:

```bash
# Phase 1: Setup
git add -A && git commit -m "Setup: project structure and dependencies"

# Phase 2: Foundational  
# (T007-T011, all blocking tasks)
git add -A && git commit -m "Feat: agent infrastructure and data services"

# Phase 3-5: Run ~3 developers or sequence
git add -A && git commit -m "Feat: user stories 1-3 (prices, chat, tools)"

# Phase 6: Polish
git add -A && git commit -m "Refactor: UI improvements and styling"

# Phase 7: Release
git add -A && git commit -m "Docs: README updates and final testing"
git push origin 001-stock-agent-chat
# Create PR for review
```

---

## 📊 Task Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 45 |
| Setup Phase | 6 tasks |
| Foundational Phase (blocking) | 5 tasks |
| User Story 1 (P1) | 5 tasks |
| User Story 2 (P1) | 6 tasks |
| User Story 3 (P1) | 7 tasks |
| User Story 4 (P2) | 5 tasks |
| Polish & Release | 11 tasks |
| Test Tasks | 11 (optional per spec) |
| Implementation Tasks | 34 |
| Estimated Dev Time | 10-11 hours |
| With 2 Developers | 8-9 hours wall-clock |
| Code Lines (estimated) | ~1,150 |

---

## 🎯 Next Steps

1. ✅ **Review this summary** (you are here)
2. ✅ **Open [tasks.md](tasks.md)** for detailed task descriptions
3. 📋 **Start Phase 1 Setup** - 6 simple initialization tasks
4. 🔨 **Do Phase 2 Foundational** - Core infrastructure (BLOCKING)
5. ⚙️ **Execute Phases 3-6** - User stories in parallel
6. 🎓 **Do Phase 7 Release** - Testing, docs, cleanup

**All tasks are in [tasks.md](tasks.md) - just follow the checklist and mark items complete as you go!**
