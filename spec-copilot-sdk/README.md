# Spec Copilot SDK

A Python SDK for building AI-assisted spec management applications using Streamlit and local LLM models. This SDK provides a cohesive interface to leverage Copilot capabilities for specification generation, analysis, and management without requiring cloud model subscriptions.

## Features

- **Streamlit-Based UI**: Interactive web interface for spec management workflows
- **Local Model Support**: Works with Claude Haiku 4.5, GPT 4.1, GPT-4o, GPT-5 mini, and Raptor mini
- **Copilot SDK Integration**: Built on top of the Copilot SDK for consistent AI interactions
- **Zero Premium Dependencies**: No subscription-based model access required
- **Composable Architecture**: Modular components for easy extension and customization

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Copilot SDK (local installation)
- One or more supported local LLM models configured

### Installation

```bash
git clone https://github.com/yourusername/spec-copilot-sdk.git
cd spec-copilot-sdk
pip install -e .
```

### Running the Application

```bash
streamlit run app.py
```

The application will launch at `http://localhost:8501`

## Project Structure

```
spec-copilot-sdk/
├── .specify/              # Project specification and constitution
│   ├── memory/            # Project constitution and decisions
│   ├── templates/         # Template files for spec documents
│   └── scripts/          # Utility scripts
├── src/                   # Main source code
│   ├── components/        # Reusable Streamlit components
│   ├── models/            # Model integration and configuration
│   ├── prompts/           # Copilot SDK prompts and templates
│   └── utils/             # Helper utilities
├── tests/                 # Test suite
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Architecture

### Core Principles

The project is governed by a **Constitution** (see `.specify/memory/constitution.md`) with six core principles:

1. **Streamlit-First UI**: All user-facing features implemented via Streamlit
2. **Local Model Priority**: Exclusive use of locally available models
3. **Copilot SDK Integration**: All AI functionality through Copilot SDK abstractions
4. **Documentation-First**: Single README.md file is the canonical documentation
5. **Test-First Development**: Tests written before implementation
6. **Composable Architecture**: Modular, reusable components with clear separation of concerns

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Streamlit |
| AI Integration | Copilot SDK |
| Language | Python 3.9+ |
| Package Management | pip / Poetry |
| Testing | pytest |

### Supported Models

| Model | Provider | Notes |
|-------|----------|-------|
| Claude Haiku 4.5 | Anthropic | Lightweight, fast inference |
| GPT 4.1 | OpenAI | General purpose |
| GPT-4o | OpenAI | Optimized |
| GPT-5 mini | OpenAI | Compact version of GPT-5 |
| Raptor mini | Custom | Specialized mini model |

All models run locally with no premium subscription requirements.

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Default model to use
DEFAULT_MODEL=claude-haiku-4.5

# Model configuration
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=2048

# Streamlit configuration
STREAMLIT_LOGGER_LEVEL=info
```

### Model Selection

The application allows runtime model selection through the Streamlit UI. Currently selected model is persisted in session state.

## Usage Examples

### Basic Spec Generation

```python
from src.models.copilot_wrapper import CopilotClient
from src.components.spec_generator import SpecGeneratorComponent

# Initialize client
client = CopilotClient(model="claude-haiku-4.5")

# Generate spec
spec = client.generate_spec(
    prompt="Create a REST API spec for a user management system",
    model="claude-haiku-4.5"
)

print(spec)
```

### In Streamlit App

```python
import streamlit as st
from src.models.copilot_wrapper import CopilotClient

st.set_page_config(page_title="Spec Generator", layout="wide")

client = CopilotClient(model=st.session_state.get("selected_model", "claude-haiku-4.5"))

prompt = st.text_area("Enter your spec request:")
if st.button("Generate Spec"):
    spec = client.generate_spec(prompt)
    st.markdown(spec)
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Running Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Code Quality

The project follows these practices:
- **Black** for code formatting
- **Flake8** for linting
- **mypy** for type checking
- **Test coverage**: Minimum 80% for new code

Run quality checks:

```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

### Adding a New Feature

1. **Create an Issue** describing the feature with acceptance criteria
2. **Write Tests** that define the expected behavior
3. **Implement** the feature to pass the tests
4. **Add Streamlit Component** to expose the feature in the UI
5. **Update README** with usage documentation
6. **Submit Pull Request** with test results and documentation updates

## Dependency Management

### Requirements

- `streamlit>=1.28.0` - Web framework
- `copilot-sdk>=0.1.0` - Copilot SDK
- `python-dotenv>=1.0.0` - Environment variable management
- `pytest>=7.0.0` - Testing framework

### Development Requirements

- `black>=23.0.0` - Code formatter
- `flake8>=6.0.0` - Linter
- `mypy>=1.0.0` - Type checker
- `pytest-cov>=4.0.0` - Coverage tracking

Install all dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Testing

The project uses pytest with mandatory test-first development:

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test Copilot SDK interactions and model invocations
- **Component Tests**: Test Streamlit component behaviors

Example test:

```python
def test_copilot_client_initialization():
    client = CopilotClient(model="claude-haiku-4.5")
    assert client.model == "claude-haiku-4.5"
    assert client.is_connected()

def test_spec_generation():
    client = CopilotClient(model="claude-haiku-4.5")
    spec = client.generate_spec("Create a simple API spec")
    assert len(spec) > 0
    assert "api" in spec.lower()
```

## Troubleshooting

### Issue: Model Not Found

**Solution**: Verify that the model is installed locally and the Copilot SDK is configured correctly.

```bash
python -c "from copilot_sdk import list_available_models; print(list_available_models())"
```

### Issue: Streamlit App Not Starting

**Solution**: Check that all dependencies are installed and Python version is 3.9+.

```bash
python --version
pip list | grep streamlit
```

### Issue: Low Inference Speed

**Solution**: Switch to a faster model (e.g., Claude Haiku 4.5 or Raptor mini) or check system resources.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Write tests for your changes (test-first!)
4. Implement the feature
5. Run all tests and quality checks
6. Update README if needed
7. Submit a pull request

## Project Governance

This project is governed by a **Constitution** that ensures consistent development practices. The constitution is stored at `.specify/memory/constitution.md` and covers:

- Core principles (Streamlit-first, local models, Copilot SDK integration)
- Technology stack constraints
- Development workflow requirements
- Code review and testing standards

Any significant changes to the project's direction require updating the constitution through a documented amendment process.

## License

Specify which license applies to this project.

## Contact & Support

- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and ideas
- **Email**: Contact maintainers via GitHub

## Changelog

### v1.0.0 (February 26, 2026)
- Initial project setup with Streamlit UI and Copilot SDK integration
- Support for Claude Haiku 4.5, GPT 4.1, GPT-4o, GPT-5 mini, and Raptor mini
- Constitution and development guidelines established
- Core architecture for spec generation and management

---

**Last Updated**: February 26, 2026
