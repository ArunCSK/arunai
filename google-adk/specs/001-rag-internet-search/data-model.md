# Data Model: Internet Search RAG

## SessionState
Stores the current session's configuration and history.

| Field | Type | Description |
|-------|------|-------------|
| selected_agent | str | The LiteLLM model string (e.g., 'gemini/gemini-1.5-flash') |
| history | list | List of chat messages (role/content) |
| last_search_results | str | Cached results from the latest search for "explain" follow-ups |

## Constraints
- **History**: Limited to last 10 exchanges to keep context window clean.
- **Search Snippets**: Max 5 snippets per query to ensure speed.
