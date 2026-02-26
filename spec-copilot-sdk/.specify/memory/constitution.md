# Spec Copilot SDK Constitution

## Core Principles

### I. Streamlit-First UI
Build all user-facing interfaces using Streamlit. The web application must be the primary interaction surface, providing interactive spec management and AI-assisted workflows. All features must be accessible through the Streamlit dashboard before consider alternative platforms.

**Rationale**: Streamlit enables rapid development and deployment of web interfaces without complex backend infrastructure. The framework prioritizes developer experience and allows focus on AI integration rather than UI framework complexity.

### II. Local Model Priority
Exclusively use locally available models (Claude Haiku 4.5, GPT 4.1, GPT-4o, GPT-5 mini, Raptor mini). No premium or cloud-only model subscriptions are used. Model selection must be optimized for available computational resources and inference speed.

**Rationale**: Local models ensure independence from cloud subscription limitations, reduce latency, and maintain data privacy. This constraint drives pragmatic architecture decisions and ensures the SDK remains accessible to developers with standard hardware.

### III. Copilot SDK Integration
All AI capabilities must be implemented using the Copilot SDK. The SDK provides the abstraction layer for model invocation, prompt management, and response handling. Direct API calls to models are prohibited except through Copilot SDK's official interfaces.

**Rationale**: Standardizing on Copilot SDK ensures consistency, maintainability, and compatibility across the codebase. It provides a unified abstraction that accommodates future model changes without requiring scattered code updates.

### IV. Documentation-First (README Only)
All project documentation must be contained in a single README.md file. No additional documentation files (guides, API docs, architecture docs) are created. The README covers setup, usage examples, configuration, and architectural overview.

**Rationale**: Single-file documentation enforces clarity and eliminates documentation fragmentation. Developers must find everything in one place, reducing cognitive load and improving product accessibility. This constraint supports the pragmatic nature of the project.

### V. Test-First Development
All features and bug fixes must have tests written before implementation. Integration tests are mandatory for Copilot SDK interactions, model invocations, and Streamlit component behaviors. Test code must be clear and serve as documentation.

**Rationale**: Tests ensure reliability of AI-assisted workflows and catch model behavior changes early. Tests document expected behavior and serve as safe refactoring baselines, especially critical when integrating multiple local models.

### VI. Composable Architecture
Features must be designed as composable, reusable components. Streamlit components should be modular and independent. Copilot SDK orchestration logic must be separated from UI concerns. The architecture must support adding new models and features with minimal changes to existing code.

**Rationale**: Composability enables rapid iteration and feature addition. It reduces coupling and makes the codebase maintainable as the SDK evolves and supports more models.

## Technology Stack & Constraints

- **Web Framework**: Streamlit (Python)
- **AI Integration**: Copilot SDK (local)
- **Supported Models**: Claude Haiku 4.5, GPT 4.1, GPT-4o, GPT-5 mini, Raptor mini (local inference only)
- **Python Version**: 3.9+
- **Package Management**: pip or Poetry
- **Documentation**: README.md only (no separate docs)

## Development Workflow

1. **Feature Planning**: All features must be described in an Issue or Discussion with acceptance criteria
2. **Test Writing**: Write tests first, define expected behavior
3. **Implementation**: Code to pass tests, integrate with Copilot SDK
4. **Streamlit Showcase**: Add Streamlit page or component demonstrating the feature
5. **README Update**: Document the feature in README with usage examples
6. **Code Review**: Verify Copilot SDK compliance, test coverage, and documentation

All pull requests must verify:
- Tests are written and passing
- Copilot SDK integration is correct
- Streamlit components are properly integrated
- README is updated if user-facing behavior changed
- Local models only (no premium APIs)

## Governance

Amendments to this constitution require:
1. Documented proposal with rationale
2. Impact assessment on current implementation
3. Migration plan if breaking changes required
4. Community consensus (pull request review)

**Version**: 1.0.0 | **Ratified**: 2026-02-26 | **Last Amended**: 2026-02-26

