"""
Self-evolving agent loop with the Claude Agent SDK.

pip install claude-agent-sdk          # requires Python 3.10+, and the Claude Code
                                       # CLI is bundled automatically
export ANTHROPIC_API_KEY=sk-...

Pattern: ACT -> EVALUATE -> EVOLVE -> repeat, driven by our own `while` loop.
query() gives us Claude's built-in tool-use loop for free on each pass; the
outer loop is what makes the agent "self-evolving" across passes.
"""

import asyncio
import json
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

GOAL = "Write a Python function `is_palindrome(s)` that ignores case, spaces, and punctuation."
MAX_ITERATIONS = 5


def extract_text(messages) -> str:
    """Pull the plain-text answer out of the SDK's streamed message objects."""
    out = []
    for m in messages:
        if isinstance(m, AssistantMessage):
            for block in m.content:
                if isinstance(block, TextBlock):
                    out.append(block.text)
    return "\n".join(out)


async def run_pass(prompt: str, allowed_tools: list[str]) -> str:
    """One ACT step: send a prompt, let Claude use tools if needed, collect the text."""
    collected = []
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=allowed_tools,
            max_turns=6,
        ),
    ):
        collected.append(message)
    return extract_text(collected)


async def evaluate(goal: str, candidate: str) -> dict:
    """
    EVALUATE step: ask Claude to self-grade the candidate against the goal,
    forcing a small structured verdict so the loop can parse it reliably.
    """
    verdict_prompt = (
        f"Goal:\n{goal}\n\nCandidate solution:\n{candidate}\n\n"
        "Grade the candidate strictly against the goal. "
        'Respond with ONLY JSON: {"status": "DONE" or "REVISE", "feedback": "<what to fix, or empty>"}'
    )
    text = await run_pass(verdict_prompt, allowed_tools=[])
    try:
        return json.loads(text.strip().strip("`"))
    except json.JSONDecodeError:
        # If parsing fails, force another revision pass rather than silently succeeding.
        return {"status": "REVISE", "feedback": "Verdict was not valid JSON; try again."}


async def self_evolving_loop(goal: str) -> str:
    candidate = ""
    feedback = ""

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n=== Iteration {iteration} ===")

        # ACT: generate (or revise) a candidate, folding in prior feedback (the "evolved" state)
        act_prompt = goal if iteration == 1 else (
            f"Goal:\n{goal}\n\n"
            f"Your previous attempt:\n{candidate}\n\n"
            f"Feedback to address:\n{feedback}\n\n"
            "Produce an improved version. Return only the final code."
        )
        candidate = await run_pass(act_prompt, allowed_tools=["Read", "Write"])
        print(candidate)

        # EVALUATE
        verdict = await evaluate(goal, candidate)
        print(f"Verdict: {verdict}")

        # DONE?
        if verdict.get("status") == "DONE":
            return candidate

        # EVOLVE: carry the critique into the next iteration's prompt
        feedback = verdict.get("feedback", "")

    print("Max iterations reached without a DONE verdict; returning last candidate.")
    return candidate


if __name__ == "__main__":
    result = asyncio.run(self_evolving_loop(GOAL))
    print("\n=== Final result ===")
    print(result)