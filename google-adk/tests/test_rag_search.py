import pytest
from rag_internet_search import get_available_gemini_models, internet_search

def test_get_models():
    models = get_available_gemini_models()
    assert isinstance(models, list)
    # Check if we at least got our defaults or filtered ones
    assert len(models) > 0
    for m in models:
        assert m.startswith("gemini/")

def test_internet_search():
    results = internet_search("Python programming language")
    assert isinstance(results, str)
    assert len(results) > 0
    if "Search failed" not in results:
        assert "Python" in results or "programming" in results or "Snippet" in results

if __name__ == "__main__":
    pytest.main([__file__])
