# Tasks: Stock Agent Chat Application

**Branch**: `001-stock-agent-chat`  
**Input**: Design documents from `/specs/001-stock-agent-chat/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅  

**Status**: Ready for execution  
**Estimated Total Time**: 10-11 hours  
**Team Size**: 1-2 developers (parallelizable tasks for 2 people)

---

## Format Reference

- `[P]` = Task can run in parallel (independent file/module)
- `[US#]` = User story this belongs to (US1, US2, US3, US4)
- File paths are exact locations for changes

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize project structure and configure dependencies

**Estimated Time**: 1 hour

- [x] T001 Create project directory structure per plan.md in repo root
- [x] T002 Create requirements.txt with minimal dependencies (streamlit, copilot-sdk, python-dotenv, pytest)
- [x] T003 [P] Create .env.example template with configuration variables
- [x] T004 [P] Initialize pytest configuration in conftest.py at root tests/ directory
- [x] T005 Create .gitignore with venv/, __pycache__/, /.streamlit/
- [x] T006 Create GitHub issue template and development contribution guidelines

**Checkpoint**: Project structure ready, dependencies defined, CI/testing infrastructure initialized

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for agent + data that ALL user stories depend on

**⚠️ CRITICAL**: No user story work begins until this phase completes

**Estimated Time**: 2.5 hours

### Core Data Services

- [x] T007 Implement mock stock data generator in src/stock_data.py
  - Define COMPANIES list with 5+ companies (AAPL, MSFT, GOOGL, AMZN, TSLA)
  - Implement get_stock_prices(symbol: str) → list[StockPrice]
  - Implement generate_mock_prices(seed: int) for reproducible test data
  - Return 5 days of OHLC prices
  - Include validation (high >= open/close, low <= open/close)
  - Handle invalid symbol errors with friendly message

- [x] T008 Create dataclass models in src/__init__.py (or separate src/models.py)
  - Implement StockPrice dataclass with: date, open, close, high, low
  - Implement Company dataclass with: symbol, name
  - Implement ChatMessage dataclass with: sender, content, timestamp, tool_calls
  - Implement ToolResult dataclass with: name, success, data, error
  - Add __repr__ for debugging

### Agent Infrastructure

- [x] T009 Initialize Copilot SDK agent in src/agent.py
  - Implement initialize_agent(model: str) → CopilotAgent
  - Read model from environment variable DEFAULT_MODEL
  - Load tool definitions (TBD in Phase 2, Task T010)
  - Implement send_message(message: str, context: dict) → dict
  - Parse response to extract message + tool_calls
  - Include error handling for model unavailability
  - Return response in standardized format (see contracts/api-messages.md)

- [x] T010 [P] Define and register tools in src/tools.py
  - Create ToolDefinition for get_stock_data with schema (symbol parameter)
  - Create ToolDefinition for analyze_stock_data with schema (symbol + question)
  - Implement handlers that will be completed in Phase 3
  - Register both tools for agent initialization
  - Include tool parameter validation

### Reusable UI Components

- [x] T011 [P] Create Streamlit components in src/ui/components.py
  - Implement display_company_selector() → selected_company str
  - Implement display_price_table(prices: list[StockPrice]) → None
  - Implement display_chat_message(message: ChatMessage) → None
  - Implement get_chat_input() → str or None
  - Include Streamlit session state initialization helpers
  - Use type hints for all functions

**Checkpoint**: Agent initialized, tools defined, data generator working, UI components ready - user stories can now proceed in parallel

---

## Phase 3: User Story 1 - View Stock Prices by Company (Priority: P1)

**Goal**: Users can select a company from dropdown and see 5 days of stock price data

**Independent Test**: User can select any company and see correctly formatted price table with no errors

**Estimated Time**: 2 hours (tests + implementation)

### Tests for User Story 1

> **WRITE THESE FIRST - They should FAIL before implementation**

- [x] T012 [P] [US1] Unit test: test stock data retrieval in tests/test_stock_data.py
  - Test get_stock_prices("AAPL") returns exactly 5 prices
  - Test prices are sorted by date ascending
  - Test invalid symbol returns error dict
  - Test price validation (high >= open/close, low <= open/close)
  - Test all prices are positive floats

- [x] T013 [P] [US1] Component test: price table display in tests/test_ui_components.py
  - Mock StockPrice data
  - Test display_price_table() renders without errors
  - Test Streamlit dataframe displays all columns

### Implementation for User Story 1

- [x] T014 [P] [US1] Implement stock data retrieval handler for Streamlit in stock_app.py
  - On app load, initialize st.session_state["selected_company"] = COMPANIES[0]
  - On app load, initialize st.session_state["stock_prices"] = []
  - Add company dropdown using display_company_selector() component
  - Fetch prices when company selection changes
  - Store prices in session_state["stock_prices"]

- [x] T015 [US1] Implement price table display in stock_app.py
  - Display prices in table format using display_price_table() component
  - Show columns: Date, Open, Close, High, Low
  - Format prices to 2 decimal places
  - Display error message if prices unavailable
  - Table updates immediately on company change (Streamlit rerun)

- [x] T016 [US1] Add error handling and validation
  - Handle network errors (if using real API) or data generation errors
  - Validate stock prices before display (all positive, valid dates)
  - Show user-friendly error messages
  - Gracefully degrade (show old data or placeholder)

**Checkpoint**: User Story 1 complete - users can select companies and view stock prices independently

**Acceptance Criteria Met**:
- ✅ Dropdown displays company list
- ✅ Selecting company shows 5 days of prices
- ✅ Table has proper column format
- ✅ Data updates without page refresh
- ✅ Invalid company shows error message

---

## Phase 4: User Story 2 - Ask Agent Questions About Stock Data (Priority: P1)

**Goal**: Users can ask natural language questions about displayed stock prices via chat

**Independent Test**: User can type a question, agent responds with analysis based on current prices

**Estimated Time**: 2 hours (tests + implementation)

### Tests for User Story 2

> **WRITE THESE FIRST - They should FAIL before implementation**

- [x] T017 [P] [US2] Integration test: agent interaction in tests/test_agent.py
  - Mock CopilotAgent initialization
  - Test send_message() receives message and context
  - Test response parsing extracts message + tool_calls
  - Test agent handles missing context gracefully
  - Mock various agent responses (with/without tools)

- [x] T018 [P] [US2] Component test: chat display in tests/test_ui_components.py
  - Test display_chat_message() formats user messages
  - Test display_chat_message() formats agent messages
  - Test get_chat_input() returns text from input
  - Test chat history displays in order

### Implementation for User Story 2

- [x] T019 [P] [US2] Initialize chat session state in stock_app.py
  - On app load, initialize st.session_state["chat_history"] = []
  - On app load, initialize st.session_state["agent_session"] = initialize_agent()
  - Implement session state persistence helpers

- [x] T020 [US2] Implement chat input and message handling in stock_app.py
  - Create chat input area using get_chat_input() component
  - On submit: add user message to chat_history
  - Call agent.send_message() with user message + context (current prices, company)
  - Parse agent response and add to chat_history
  - Display chat history in order (show previous messages first, newest last)

- [x] T021 [US2] Implement chat message display in stock_app.py
  - Display all messages in chat_history using display_chat_message()
  - Differentiate user vs agent messages (color, alignment, badge)
  - Show timestamps for each message
  - Handle long messages gracefully (scrollable or truncated)
  - Show loading indicator while waiting for agent response

- [x] T022 [US2] Add context awareness to agent calls
  - Build context dict with:
    - selected_company: current company info
    - current_prices: current stock prices in display
    - chat_history: previous messages for context
  - Pass context to agent.send_message()
  - Show context used (for debugging/transparency)

**Checkpoint**: User Story 2 complete - chat interface works, agent responds to questions about displayed prices

**Acceptance Criteria Met**:
- ✅ Chat input accepts user text
- ✅ Agent responds with answer
- ✅ Agent references displayed data
- ✅ Conversation context maintained
- ✅ Follow-up questions understand previous context

---

## Phase 5: User Story 3 - Agent Calls Custom Tools (Priority: P1)

**Goal**: Agent automatically calls custom tools to retrieve and analyze stock data when answering questions

**Independent Test**: Agent receiving question calls appropriate tool(s), incorporates results in response

**Estimated Time**: 2 hours (tests + implementation)

### Tests for User Story 3

> **WRITE THESE FIRST - They should FAIL before implementation**

- [x] T023 [P] [US3] Unit test: tool implementation in tests/test_tools.py
  - Test get_stock_data handler returns correct data for known symbols
  - Test get_stock_data handler returns error for invalid symbol
  - Test analyze_stock_data handler with "average price" question
  - Test analyze_stock_data handler with "trend" question
  - Test analyze_stock_data handler with "high/low" question
  - Test tool response format matches contract

- [x] T024 [P] [US3] Integration test: tool calling flow in tests/test_integration.py
  - Test agent calls get_stock_data when asked about prices
  - Test agent calls analyze_stock_data for analysis questions
  - Test agent correctly processes tool results
  - Test multi-tool sequences (e.g., comparing two companies)
  - Test tool error handling

### Implementation for User Story 3

- [x] T025 [P] [US3] Implement get_stock_data tool handler in src/tools.py
  - Handler receives symbol parameter
  - Calls stock_data.get_stock_prices(symbol)
  - Returns prices in tool result format
  - Returns error dict if symbol invalid
  - Map tool response to ToolResult dataclass

- [x] T026 [P] [US3] Implement analyze_stock_data tool handler in src/tools.py
  - Handler receives symbol + question parameters
  - Calls get_stock_data internally to get prices
  - Parse question type (detect: average, trend, high/low, volatility, etc.)
  - Perform analysis:
    - Average: Calculate mean of closing prices
    - Trend: Compare first vs last day
    - High/Low: Find max/min with dates
    - Volatility: Calculate price range
  - Return analysis in standardized JSON format
  - Include reasoning in response

- [x] T027 [US3] Register and wire tools to agent in src/agent.py
  - Update tool definitions with actual handler functions
  - Register tools with agent on initialization
  - Test tool invocation triggers handler
  - Verify tool results are passed back to agent

- [x] T028 [US3] Display tool call information in chat in stock_app.py
  - In ChatMessage display, show which tools were called
  - Display tool input parameters (what was requested)
  - Show tool results or "Tool displayed data X"
  - Highlight tool invocations for clarity (demo value)
  - Include error details if tool fails

- [x] T029 [US3] Add tool call validation and error handling
  - Validate tool parameters before calling
  - Catch tool execution errors
  - Return user-friendly error messages
  - Log tool calls for debugging (print for now, structured logging later)

**Checkpoint**: User Story 3 complete - agent has tools and can call them automatically

**Acceptance Criteria Met**:
- ✅ Agent calls get_stock_data for price queries
- ✅ Agent calls analyze_stock_data for analysis
- ✅ Tool results used in agent response
- ✅ Multi-tool calls work correctly
- ✅ Tool errors handled gracefully
- ✅ Tool invocations visible in chat

---

## Phase 6: User Story 4 - Clean UI Design (Priority: P2)

**Goal**: Application presents clean, professional, minimalist interface that clearly demonstrates Copilot SDK

**Independent Test**: App UI is visually organized, easy to use, and demonstrates tool-calling transparently

**Estimated Time**: 1.5 hours (after US1-3 are functional)

### Implementation for User Story 4

- [ ] T030 [P] [US4] Design main app layout in stock_app.py
  - Set page config with title "Stock Agent Chat" and layout="wide"
  - Create clear sections: company selector, price table, chat area
  - Use columns for side-by-side layout (data | chat) or stack vertically
  - Add header with app title and brief description
  - Set professional color scheme (Streamlit default or custom theme)

- [ ] T031 [P] [US4] Style company selector and price table
  - Use Streamlit column layout for company selector
  - Add helpful label: "Select a company to view stock data"
  - Format price table with proper alignment and formatting
  - Add table caption showing selected company and date range
  - Highlight high/low prices with conditional formatting
  - Use metric badges for key stats (avg, change, etc.)

- [ ] T032 [P] [US4] Style chat interface similar to GitHub Copilot chat
  - Use Streamlit columns for message layout
  - User messages: align right, light blue background
  - Agent messages: align left, light gray background
  - Add sender badges ("You", "Agent")
  - Show timestamps in subtle gray
  - Highlight tool calls with special formatting (e.g., badge: "🔧 Used: get_stock_data")

- [ ] T033 [P] [US4] Add visual feedback and polish
  - Loading spinner while agent responds ("Agent is thinking...")
  - Success indicators for tool execution ("✓ Fetched data")
  - Error displays in red with clear messages
  - Smooth message scrolling (auto-scroll to latest)
  - Responsive design for different screen sizes

- [ ] T034 [US4] Add instructional text and examples
  - Brief description of app purpose above chat
  - Example questions in placeholder text
  - Tooltips on key components
  - Help text: "The agent can analyze stock prices and answer questions about trends"

**Checkpoint**: User Story 4 complete - UI is clean, professional, and demo-ready

**Acceptance Criteria Met**:
- ✅ Layout clearly organized (data | chat sections)
- ✅ Chat resembles GitHub Copilot UI style
- ✅ Tool invocations clearly visible
- ✅ Professional appearance with proper spacing
- ✅ Easy for audience to understand what's happening
- ✅ Responsive and readable on different sizes

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, documentation, and quality improvements

**Estimated Time**: 1.5 hours

### Testing & Quality

- [ ] T035 [P] Write comprehensive integration test in tests/test_integration.py
  - Test complete user workflow: select company → ask question → agent responds with tools
  - Test US1 + US2 + US3 working together
  - Test multiple questions in sequence
  - Test tool error scenarios
  - Test invalid inputs
  - Verify no Python warnings or errors in logs

- [ ] T036 [P] Complete unit tests for all modules
  - Extend test_stock_data.py with edge cases
  - Extend test_agent.py with error scenarios
  - Extend test_tools.py with analysis cases
  - Extend test_ui_components.py with rendering tests
  - Aim for >80% code coverage on src/

- [ ] T037 [P] Performance validation
  - Verify agent response time <3 seconds
  - Verify price refresh <2 seconds
  - Verify no memory leaks in session_state
  - Test chat history with 20+ messages (no slowdown)

### Documentation & Examples

- [ ] T038 Update README.md with Stock Agent Chat feature
  - Add feature overview and screenshot descriptions
  - Update installation section with stock-agent-chat specific instructions
  - Add usage examples section (example questions)
  - Update project structure section to mention stock_app.py
  - Add "How It Works" explaining Copilot SDK integration
  - Link to quickstart.md for developers

- [ ] T039 Verify and complete quickstart.md
  - Test all installation steps work end-to-end
  - Verify example questions work as described
  - Update any outdated file paths or commands
  - Test troubleshooting section solutions
  - Add a "First Run" section with expected behavior

- [ ] T040 Code cleanup and refactoring
  - Remove or comment out debug logging
  - Ensure all type hints are present
  - Verify docstrings on all public functions
  - Clean up any unused imports or variables
  - Consistent code style (Black formatting)

### Final Integration

- [ ] T041 Test app with different models
  - Test with Claude Haiku 4.5 (default)
  - Test with GPT-4o if available
  - Verify model switching works via .env
  - Document any model-specific behavior in README

- [ ] T042 Create demo walkthrough script or notes
  - Document expected demo flow
  - List 5-7 good example questions to ask
  - Note any quirks or limitations to mention to audience
  - Prepare talking points about Copilot SDK value

- [ ] T043 Final validation checklist
  - Run all tests: `pytest tests/` - should pass
  - Run app: `streamlit run stock_app.py` - should start without errors
  - Test all user stories work:
    - US1: Select company, see prices ✓
    - US2: Ask question, agent responds ✓
    - US3: Agent calls tools ✓
    - US4: UI clean and organized ✓
  - Verify no Python warnings in logs
  - Check that Constitution principles are met

**Checkpoint**: Application ready for production demo and code review

### Git & Release

- [ ] T044 Commit all changes to feature branch
  - Commit message: "Complete Stock Agent Chat feature (001-stock-agent-chat)"
  - Include all spec, code, and test files
  - Verify branch is clean: `git status` shows nothing

- [ ] T045 Create pull request with summary
  - Link to spec.md in PR description
  - List test results (all passing)
  - Note any assumptions or limitations
  - Request code review

---

## Dependency Graph & Execution Order

### Flow Diagram

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKING - must complete first)
    ├── T007-T008: Data services
    ├── T009-T010: Agent infrastructure
    └── T011: UI components
    
    After Phase 2 completes, can proceed in parallel:
    
    ├─→ Phase 3: User Story 1 (View Prices)
    │   ├─→ T012-T013: Tests
    │   └─→ T014-T016: Implementation
    │
    ├─→ Phase 4: User Story 2 (Chat Interface)
    │   ├─→ T017-T018: Tests
    │   └─→ T019-T022: Implementation
    │
    └─→ Phase 5: User Story 3 (Agent Tools)
        ├─→ T023-T024: Tests
        └─→ T025-T029: Implementation
        
    Phase 6: User Story 4 (UI Polish) - can start after US1-3 functional
        └─→ T030-T034: UI improvements
    
    Phase 7: Polish & Release
        └─→ T035-T045: Testing, docs, release
```

### Critical Path

**Minimum time sequential (1 developer)**:
1. Phase 1 Setup: 1h
2. Phase 2 Foundational: 2.5h
3. Phase 3 US1: 2h
4. Phase 4 US2: 2h
5. Phase 5 US3: 2h
6. Phase 6 US4: 1.5h
7. Phase 7 Polish: 1.5h
= **~12-13 hours total**

**Optimized with 2 developers (parallel)**:
1. Phase 1 Setup: 1h (both)
2. Phase 2 Foundational: 2.5h (both)
3. Phase 3-5 (parallel): 2h + 2h + 2h running concurrently = 2h wall-clock (2 people working)
4. Phase 6 UI Polish: 1.5h (one person while other does testing)
5. Phase 7 Polish: 1.5h (both)
= **~8-9 hours wall-clock time**

### Parallel Opportunities

**Within Phase 1**:
- T003, T004, T005 can run in parallel (independent files)

**Within Phase 2**:
- T010, T011 can run in parallel with T007-T009
- T008 can run in parallel with T007

**Within Phase 3-5 (after Phase 2)**:
- All three user stories can be implemented in parallel
- Tests [P] within each story can run in parallel
- Different story implementations don't block each other

**Within Phase 6**:
- T030, T031, T032, T033 can run in parallel

**Suggested 2-Person Team Split**:
- **Developer A**: T001-T008 (Setup + Foundational)
- **Developer B**: Wait, then take Phase 3 (US1)
- **Developer A**: Take Phase 4 (US2) while Developer B finishes Phase 3
- **Developer B**: Take Phase 5 (US3) while Developer A finishes Phase 4
- **Both**: Phase 6 (UI Polish) - one does T030-T033 while other does T035-T037
- **Both**: Phase 7 (Release) - T038-T045

---

## Task Checklist Summary

- **Setup (Phase 1)**: 6 tasks - 1 hour
- **Foundational (Phase 2)**: 5 tasks - 2.5 hours
- **User Story 1 (Phase 3)**: 5 tasks - 2 hours
- **User Story 2 (Phase 4)**: 5 tasks - 2 hours
- **User Story 3 (Phase 5)**: 7 tasks - 2 hours
- **User Story 4 (Phase 6)**: 5 tasks - 1.5 hours
- **Polish & Release (Phase 7)**: 11 tasks - 1.5 hours

**Total**: 44 tasks | **10-11 hours** individual development | **8-9 hours** with 2-person team

---

## Success Criteria for Task Completion

✅ **All Setup tasks completed**:
- Dependencies installed
- Project structure in place
- Testing infrastructure ready

✅ **All Foundational tasks completed**:
- Stock data generator working
- Agent initialization working
- Tools defined and ready
- Running `pytest tests/` should find 0 tests yet (or pass existing setup tests)

✅ **All Phase 3 tasks completed** (User Story 1):
- `streamlit run stock_app.py` shows company selector
- Selecting company displays 5-day price table
- Prices update on company change
- Tests pass: `pytest tests/test_stock_data.py tests/test_ui_components.py::test_price_table`

✅ **All Phase 4 tasks completed** (User Story 2):
- Chat input and message history visible
- User can type message and submit
- Agent responds (may be simple response without tools at this stage)
- Chat context maintained
- Tests pass: `pytest tests/test_agent.py tests/test_ui_components.py::test_chat`

✅ **All Phase 5 tasks completed** (User Story 3):
- Agent calls tools when answering questions
- Tool results appear in response
- Tool invocation highlighted in chat
- Multiple tool calls work (e.g., comparing companies)
- Tests pass: `pytest tests/test_tools.py tests/test_integration.py`

✅ **All Phase 6 tasks completed** (User Story 4):
- UI is clean and professional
- Layout is clear (data | chat sections)
- Chat resembles GitHub Copilot UI
- Tool calls are visually highlighted
- Demo-ready appearance

✅ **All Phase 7 tasks completed** (Polish):
- All tests pass: `pytest tests/` ≥80% coverage
- README updated with feature documentation
- No Python warnings or errors in logs
- Performance <3s for agent, <2s for prices
- git pull request ready for review

---

## Notes for Developers

### Test-First Development
- Write tests BEFORE implementation (tests should FAIL first)
- Use tests to define API contract
- Run tests constantly during development
- Tests document expected behavior

### Minimalist Code
- Each function should be understandable in <1 minute
- Type hints show intent
- Docstrings explain "why", not "what"
- Code should speak for itself

### Session State Management
- Always initialize session_state at app startup
- Store data that persists across reruns
- Don't store Streamlit widgets or functions in session state

### Agent Context
- Include selected_company and current_prices in agent context
- Include chat history for conversation continuity
- Agent uses context to provide informed responses

### Error Handling
- All tool handlers return (success, data) or (error dict)
- Never raise exceptions in tool handlers
- User-facing errors should be friendly and helpful
- Log errors for debugging (use print for now)

---

**Ready to execute!** Make the first commit with Phase 1 setup, then proceed with Phase 2 foundational tasks. Once Phase 2 completes, you can parallelize all user story implementations.

