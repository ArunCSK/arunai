"""
Self-evolving agent loop with Google's Agent Development Kit (ADK).

pip install google-adk
export GOOGLE_API_KEY=...          # or configure Vertex AI credentials

Unlike the Claude Agent SDK example, ADK has this generator -> critic -> refine
cycle as a first-class building block: LoopAgent. It runs its sub-agents in
order, repeatedly, until either a sub-agent signals `escalate` (our "DONE")
or `max_iterations` (the safety cap) is reached.
"""

from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.tools.tool_context import ToolContext

GEMINI_MODEL = "gemini-2.5-flash"
GOAL = "Write a Python function `is_palindrome(s)` that ignores case, spaces, and punctuation."
COMPLETION_PHRASE = "APPROVED"

# --- Shared state keys (read/written via {current_solution} / {critique} templating) ---
STATE_SOLUTION = "current_solution"
STATE_CRITIQUE = "critique"


# --- EVOLVE signal: a tool the critic calls to stop the loop ---
def exit_loop(tool_context: ToolContext):
    """Call this ONLY when the critique says the solution is fully correct and complete."""
    tool_context.actions.escalate = True          # tells LoopAgent to stop
    tool_context.actions.skip_summarization = True
    return {}


# --- ACT (first pass): produce an initial draft ---
initial_writer = LlmAgent(
    name="InitialWriter",
    model=GEMINI_MODEL,
    instruction=f"Goal:\n{GOAL}\n\nWrite a first-draft solution. Output only the code.",
    output_key=STATE_SOLUTION,   # writes into session state as {current_solution}
)

# --- EVALUATE: critique the current solution against the goal ---
critic = LlmAgent(
    name="Critic",
    model=GEMINI_MODEL,
    instruction=(
        f"Goal:\n{GOAL}\n\n"
        "Solution to review:\n{current_solution}\n\n"
        f"If it fully satisfies the goal, respond with exactly '{COMPLETION_PHRASE}'. "
        "Otherwise, list concrete, actionable fixes."
    ),
    output_key=STATE_CRITIQUE,   # writes into session state as {critique}
)

# --- ACT (revise) or EVOLVE-exit: refine, or call exit_loop if the critic approved ---
refiner = LlmAgent(
    name="Refiner",
    model=GEMINI_MODEL,
    instruction=(
        "Critique:\n{critique}\n\n"
        f"If the critique is exactly '{COMPLETION_PHRASE}', call the exit_loop tool "
        "and output nothing else. Otherwise, apply the fixes to:\n{current_solution}\n"
        "and output only the improved code."
    ),
    tools=[exit_loop],
    output_key=STATE_SOLUTION,   # overwrites {current_solution} with the improved version
)

# --- The self-evolving loop itself ---
refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[critic, refiner],   # order matters: evaluate, then evolve
    max_iterations=5,               # hard safety cap
)

# --- Full pipeline: draft once, then evolve it ---
root_agent = SequentialAgent(
    name="SelfEvolvingSolver",
    sub_agents=[initial_writer, refinement_loop],
    description="Drafts a solution, then iteratively critiques and refines it until approved.",
)

# Run with the ADK CLI/dev UI, e.g.:
#   adk run self_evolving_agent   (if this file is saved as agent.py in that package)
# or invoke root_agent programmatically via a Runner + SessionService.