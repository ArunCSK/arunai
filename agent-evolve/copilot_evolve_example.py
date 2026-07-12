"""
Self-evolving agent client that talks to the VS Code extension local chat API.

Usage:
  python copilot_evolve_example.py "Your goal prompt here"

The extension should be running and exposing `POST /chat` on http://localhost:3333
as provided by the `vscode-chat-local-api` extension in this workspace.
"""

import json
import sys
import time
from typing import Tuple

import requests

BASE_URL = "http://localhost:3333"
CHAT_PATH = "/chat"
CHAT_URL = BASE_URL + CHAT_PATH

MAX_ITERATIONS = 5
COMPLETION_TOKEN = "DONE"


def call_chat_api(message: str, timeout: int = 10) -> str:
    """POST to the local extension chat API and return its reply text.

    Expects the extension to accept JSON `{ "message": "..." }`
    and return `{ "reply": "..." }`.
    """
    payload = {"message": message}
    try:
        resp = requests.post(CHAT_URL, json=payload, timeout=timeout)
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to reach chat API at {CHAT_URL}: {e}")
    if resp.status_code != 200:
        raise RuntimeError(f"Chat API returned {resp.status_code}: {resp.text}")
    data = resp.json()
    # allow either `reply` or raw text
    if isinstance(data, dict) and "reply" in data:
        return data["reply"]
    return resp.text


def evaluate(goal: str, candidate: str) -> dict:
    """Ask the chat API to grade the candidate against the goal.

    The API is expected to run an LLM agent that will respond with a JSON
    blob like: {"status": "DONE" | "REVISE", "feedback": "..."}
    If parsing fails, return REVISE so the loop continues.
    """
    verdict_prompt = (
        f"Goal:\n{goal}\n\nCandidate solution:\n{candidate}\n\n"
        'Grade the candidate strictly against the goal. '
        'Respond with ONLY JSON: {"status": "DONE" or "REVISE", "feedback": "<what to fix, or empty>"}'
    )

    text = call_chat_api(verdict_prompt)

    # First, try a direct parse (happy path)
    try:
        return json.loads(text.strip())
    except Exception:
        pass

    # Tolerate common wrappers: leading "Echo:", markdown/code fences, or surrounding text.
    trimmed = text.strip()

    # remove a leading 'Echo:' prefix if present
    if trimmed.startswith('Echo:'):
        trimmed = trimmed[len('Echo:'):].lstrip()

    # strip surrounding backticks (```json``` or single/backtick wrappers)
    trimmed = trimmed.strip('`').strip()

    # Attempt to extract the first JSON object-looking substring
    try:
        import re

        m = re.search(r"\{[\s\S]*\}", trimmed)
        if m:
            candidate_json = m.group(0)
            return json.loads(candidate_json)
    except Exception:
        pass

    # If we reached here, parsing failed — return REVISE so the loop continues.
    return {"status": "REVISE", "feedback": "Verdict was not valid JSON; try again."}


def self_evolving_loop(goal: str) -> str:
    candidate = ""
    feedback = ""

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n=== Iteration {iteration} ===")

        # ACT: generate (or revise)
        if iteration == 1:
            act_prompt = f"Goal:\n{goal}\n\nProduce a solution. Return only the final code or answer."
        else:
            act_prompt = (
                f"Goal:\n{goal}\n\nYour previous attempt:\n{candidate}\n\n"
                f"Feedback to address:\n{feedback}\n\n"
                "Produce an improved version. Return only the final code or answer."
            )

        try:
            candidate = call_chat_api(act_prompt)
        except RuntimeError as e:
            print(f"Error calling chat API: {e}")
            print("Retrying in 2s...")
            time.sleep(2)
            candidate = call_chat_api(act_prompt)

        print("--- Candidate ---")
        print(candidate)

        # EVALUATE
        verdict = evaluate(goal, candidate)
        print(f"Verdict: {verdict}")

        if verdict.get("status") == "DONE":
            print(f"\nGoal satisfied after {iteration} iteration(s).")
            return candidate

        feedback = verdict.get("feedback", "")

    print(f"\nReached the {MAX_ITERATIONS}-iteration cap without a DONE verdict.")
    return candidate


if __name__ == "__main__":
    if len(sys.argv) > 1:
        goal_text = sys.argv[1]
    else:
        goal_text = (
            "Write a Python function `is_palindrome(s)` that ignores case, spaces, and punctuation."
        )

    try:
        result = self_evolving_loop(goal_text)
        print("\n=== Final result ===")
        print(result)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
