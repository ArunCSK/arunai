# Research: Internet Search RAG & Agent Selection

## Decision: Agent Selection Logic
- **Chosen**: Filter litellm.model_list for entries starting with gemini/. Present an indexed list to the user.
- **Rationale**: litellm provides a comprehensive internal list. Filtering ensures we only show Gemini models as per constitution.
- **Alternatives**: Manually hardcoding a list (too brittle), querying Google API (requires more auth setup).

## Decision: Internet Search Tool
- **Chosen**: duckduckgo-search (DDGS) library.
- **Rationale**: No API key required, fast, and provides simple text snippets sufficient for 2-3 line answers. Fits the "Caveman approach".
- **Alternatives**: Tavily (better but needs key), Google Search API (complex setup).

## Decision: Implementation Pattern (Caveman)
- **Chosen**: Procedural script with a main loop. Use litellm.completion directly.
- **Rationale**: Fastest implementation. Minimizes boilerplate.
- **Alternatives**: Full Agentic framework (too much overhead for this simple requirement).

## Decision: Answer Length Control
- **Chosen**: System prompt instruction: "Answer in exactly 2-3 lines unless the user asks for more detail."
- **Rationale**: Simplest way to enforce the constraint without complex output parsing.
