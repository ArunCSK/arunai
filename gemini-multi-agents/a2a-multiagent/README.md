# A2A Protocol Multi-Agent System (with Gemini)

This project is a simple multi-agent system designed to help you learn the core concepts of the **Agent-to-Agent (A2A) Protocol** using Python, Google's Gemini API (`google-genai`), and standard web APIs.

## Core Concepts

The A2A protocol standardizes how agents talk to *each other* (unlike MCP, which is how agents talk to tools). It consists of a Client-Server model.

1.  **Agent Card (Discovery):** A machine-readable JSON endpoint (`/.well-known/agent-card.json`) that exposes an agent's capabilities to the world.
2.  **Task-Based Messaging:** Agents send specific "instructions" and "data" payloads to one another, rather than unstructured prompts.

## Project Structure

*   `worker_agent.py`: Acts as the **A2A Server**. It hosts an Agent Card using FastAPI and has a `/tasks` endpoint. It uses Gemini to analyze data based on incoming instructions.
*   `manager_agent.py`: Acts as the **A2A Client**. It uses Gemini to plan a task, discovers the worker agent by reading its Agent Card, delegates a specific instruction, and synthesizes the final result.
*   `.env.example`: Template for your environment variables.

## Getting Started

1.  **Environment Setup:** Ensure you have activated your virtual environment.
    ```powershell
    # Windows
    .\venv\Scripts\Activate.ps1
    ```

2.  **API Key:** 
    *   Copy `.env.example` to `.env`.
    *   Add your Gemini API Key to the `.env` file (`GEMINI_API_KEY=your_key_here`).

3.  **Run the System:**
    You will need two terminal windows (both with the virtual environment activated).

    *   **Terminal 1 (Start the Worker Agent):**
        ```powershell
        python worker_agent.py
        ```
        *This will start a local server on port 8000.*

    *   **Terminal 2 (Run the Manager Agent):**
        ```powershell
        python manager_agent.py
        ```

## What Happens When You Run It?
1.  The `manager_agent` starts and requests `/.well-known/agent-card.json` from the `worker_agent`.
2.  The `manager_agent` uses Gemini to look at the user's goal and the worker's capabilities, then crafts a specific instruction.
3.  The `manager_agent` sends a POST request to the worker's `/tasks` endpoint with the instruction and raw data.
4.  The `worker_agent` receives the task, uses Gemini to analyze the data, and returns the result.
5.  The `manager_agent` receives the result, synthesizes a final response using Gemini, and prints it.