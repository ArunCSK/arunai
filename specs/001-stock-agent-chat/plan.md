# Implementation Plan: Stock Agent Chat Application

**Branch**: `001-stock-agent-chat` | **Date**: February 26, 2026 | **Spec**: [spec.md](spec.md)

## Summary

Build a minimalist Streamlit web application demonstrating Copilot SDK capabilities. The app displays 5 days of stock price data for selected companies and uses an AI agent with custom tools to answer user questions about the data through a chat interface. This is a teaching application—not a production trading platform—designed to clearly show how developers can integrate local AI models with Streamlit using the Copilot SDK's tool-calling mechanism.

## Technical Context

**Language/Version**: Python 3.9+  
**Primary Dependencies**: Streamlit, Copilot SDK (local), local LLM models  
**Storage**: In-memory (no persistence required)  
**Testing**: pytest with integration tests for agent interactions  
**Target Platform**: Local development machine (Linux/macOS/Windows)  
**Project Type**: Web application (Streamlit single-page app)  
**Performance Goals**: <3 seconds for agent responses, <2 seconds for data refresh  
**Constraints**: Local models only, no cloud APIs, minimal dependencies  
**Scale/Scope**: Single-feature demo app, ~500-800 lines of production code, ~300-400 lines of tests  

## Constitution Check

✅ **All gates pass** for this feature:

| Principle | Compliance | Details |
|-----------|-----------|---------|
| **I. Streamlit-First UI** | ✅ PASS | Single Streamlit app with company dropdown, price table, and chat interface |
| **II. Local Model Priority** | ✅ PASS | Agent uses only local models (Claude Haiku 4.5, GPT-4o, etc.) from config |
| **III. Copilot SDK Integration** | ✅ PASS | Agent initialization and tool registration using Copilot SDK only |
| **IV. Documentation-First** | ✅ PASS | Feature documented in main README.md only (no separate feature docs created) |
| **V. Test-First Development** | ✅ PASS | Test suite covers agent interactions, tool calls, and stock data retrieval |
| **VI. Composable Architecture** | ✅ PASS | Modular design: stock data service, tool definitions, agent orchestration, UI components |

No deviations required. All principles align with minimalist design goal.

## Project Structure

### Documentation Structure

```text
specs/001-stock-agent-chat/
├── spec.md                 # Feature specification (COMPLETED)
├── plan.md                 # This file (IN PROGRESS)
├── research.md             # Phase 0 research findings (TO DO)
├── data-model.md           # Phase 1 data design (TO DO)
├── quickstart.md           # Phase 1 dev quickstart (TO DO)
├── contracts/              # Phase 1 tool contracts (TO DO)
│   ├── tool-definitions.md # Tool schema and contracts
│   └── api-messages.md     # Agent message format contracts
├── checklists/
│   └── requirements.md     # Requirements validation (COMPLETED)
└── tasks.md                # Phase 2 development tasks (TO DO)
```

### Source Code Structure

```text
.                          # Repository root
├── stock_app.py            # Main Streamlit entry point (~150 lines)
├── requirements.txt        # Python dependencies
├── README.md               # Complete documentation (already exists)
│
├── src/                    # Source code (minimalist)
│   ├── __init__.py
│   ├── stock_data.py       # Stock data service (~100 lines)
│   ├── agent.py            # Copilot SDK agent setup (~150 lines)
│   ├── tools.py            # Custom tool definitions (~120 lines)
│   └── ui/
│       ├── __init__.py
│       └── components.py   # Streamlit UI components (~180 lines)
│
└── tests/                  # Test suite (minimalist)
    ├── __init__.py
    ├── test_stock_data.py  (~80 lines)
    ├── test_agent.py       (~100 lines)
    ├── test_tools.py       (~90 lines)
    └── test_integration.py (~120 lines)
```

**Structure Decision**: Single Streamlit app with modular `src/` structure and test-first test suite. This minimalist structure:
- Keeps entry point (`stock_app.py`) clean and focused
- Separates concerns: data (stock_data.py), AI (agent.py, tools.py), UI (components.py)
- Maintains composability: each module can be tested independently
- Reduces cognitive load: developer can understand each file in <5 minutes
- Enables rapid feature addition without restructuring

## Implementation Approach

### Principles for Minimalist Code

1. **Separation of Concerns**: Each module has one clear responsibility
   - `stock_data.py`: Fetch and format stock data
   - `agent.py`: Initialize and manage Copilot SDK agent session
   - `tools.py`: Define custom tools (tool registry)
   - `components.py`: Streamlit UI components

2. **No Over-Engineering**: Only include code that directly supports the spec. No:
   - Dependency injection frameworks
   - ORM layers
   - Configuration management libraries (use simple `.env` file)
   - Abstract base classes for simple implementations

3. **Clear Naming & Comments**: Function and variable names explain themselves:
   ```python
   # Good
   def get_last_five_days_prices(company_symbol: str) -> list[StockPrice]:
   
   # Avoid
   def fetch_data(symbol):
   ```

4. **Test-First Driving Design**: Tests define the API contract before implementation

5. **Composability**: Modules pass simple Python objects (dicts, dataclasses), not complex wrappers

### Minimalist Dependencies

```
streamlit>=1.28.0          # Web UI
copilot-sdk>=0.1.0         # Agent framework (local)
python-dotenv>=1.0.0       # Environment config
pytest>=7.0.0              # Testing
pytest-asyncio>=0.21.0     # Async test support (if needed)
```

No unnecessary additions. Avoid:
- pydantic (use dataclasses instead for type hints)
- sqlalchemy (use in-memory data)
- fastapi (not needed for single Streamlit app)
- logging framework (use print for simplicity, upgrade later if needed)

## Implementation Phases

### Phase 0: Research (Parallel Tasks)

**Objective**: Resolve technical unknowns and validate approach

Research tasks:
- [ ] Copilot SDK local model initialization patterns
- [ ] Streamlit session state management for chat history
- [ ] Stock data API/simulation options (free or mock data)
- [ ] Agent tool-calling patterns with Copilot SDK
- [ ] Type hints best practices for Python 3.9+

**Output**: `research.md` with findings and implementation patterns

### Phase 1: Design & Contracts

**Objective**: Define data models, tool schemas, and component APIs before coding

Tasks:
1. **Data Model Design** (`data-model.md`)
   - Company: {symbol, name}
   - StockPrice: {date, open, close, high, low}
   - ChatMessage: {sender, content, timestamp}
   - ToolResult: {name, status, data}

2. **Tool Contracts** (`contracts/`)
   - Tool 1: `get_stock_data(symbol: str)` → StockPrice[]
   - Tool 2: `analyze_stock_data(prices: StockPrice[], question: str)` → str
   - Message format: Agent input/output schema

3. **Quickstart Guide** (`quickstart.md`)
   - How to start the app: `streamlit run stock_app.py`
   - How to select model in UI
   - Example questions for the agent

4. **Agent Context Update**
   - Run `.specify/scripts/powershell/update-agent-context.ps1`

**Output**: Completes design phase with all contracts and models defined

### Phase 2: Implementation Tasks

**Objective**: Implement code driven by tests (test-first approach)

Tasks breakdown (see `tasks.md` for full detail):
1. **Stock Data Service** (~2 hours)
   - Get/mock 5-day stock data
   - Support multiple companies
   - Return consistent format

2. **Agent Setup** (~2 hours)
   - Initialize Copilot SDK with local model
   - Register custom tools
   - Handle tool-calling responses

3. **Tool Registration** (~1.5 hours)
   - Implement get_stock_data tool
   - Implement analyze_stock_data tool
   - Tool parameter validation

4. **Streamlit UI** (~3 hours)
   - Company dropdown + data table
   - Chat message history display
   - Chat input + submit
   - Agent response display with tool info

5. **Integration & Testing** (~2 hours)
   - End-to-end flow test
   - Error handling
   - Session state management

**Total Estimate**: ~10-11 hours development

### Phase 3: Validation

- All tests passing
- Manual QA against spec acceptance scenarios
- README updated with usage examples
- Code review against Constitution

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Copilot SDK docs unclear | High | Research phase documents patterns; code to tests |
| Stock data API unavailable | Medium | Use mock/simulated data generator |
| Agent tool-calling failures | High | Comprehensive integration tests |
| Streamlit session state issues | Medium | Test session persistence patterns early |
| Local model inference slow | Low | Set realistic timeouts; document in README |

## Success Criteria

✅ Implementation plan is "ready to execute" when:
- All Phase 0 research tasks completed and documented
- All Phase 1 design contracts finalized
- Phase 2 task list created (`tasks.md`)
- First test written (test-first setup)
- README updated with development section

## Notes

**Minimalism Philosophy**: This plan intentionally avoids:
- Complex patterns for a simple problem
- Over-abstraction in early phases
- "Enterprise-ready" architectures for a demo app
- Multiple tiers or layers not required by spec

Each module stays focused and single-responsibility. Total codebase grows by ~800 lines, tests by ~400 lines. This is intentional—simplicity enables learning (the app's purpose).

**Next Step**: Execute `/speckit.clarify` if any research needed, then `/speckit.tasks` to generate detailed task breakdown.
