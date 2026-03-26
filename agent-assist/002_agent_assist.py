'''
If this stream was coming in from 10,000 agents simultaneously, how would you change your Python code to ensure the AgentAssistant class is thread-safe? (Hint: Think about threading.Lock or using a stateless approach with Redis).

Would you like to try implementing the thread-safe version?

Why this is a "Senior" Answer:Stateful Memory: By using self.previous_word, you solve the "Twist." If "stolen" arrives in one data packet and "card" arrives in the next, your code correctly links them. In a real system, you might use an N-gram buffer (like a collections.deque with a max length) to support 3 or 4-word phrases.Efficiency ($O(1)$ Complexity): I used a set for keywords and a dict for phrases. In Python, checking if x in my_set is $O(1)$ (constant time), whereas if x in my_list is $O(n)$. At JPMC scale, $O(n)$ lookups per word across thousands of concurrent calls would crash the server.Data Sanitization: Real-world audio transcripts are messy. Adding .lower().strip() and removing punctuation shows you understand that raw data is never "clean."Decoupling: Using a private method _trigger_alert demonstrates that you understand how to separate the detection logic from the downstream action (like calling a Salesforce API).JPMC Technical Follow-up: Scaling to 10,000 AgentsIn a live interview, the follow-up will be: "This works for one agent, but what if 10,000 agents are calling this script at once on a single server?"The Problem: Your AgentAssistant instance stores state in self.previous_word. If you use one global instance for all calls, the words from Agent A will mix with Agent B, causing "hallucinated" alerts.The Solution: You need a Session-Based State.In-Memory (Fast): Use a Python dict where the key is the call_id and the value is the AgentAssistant object.Distributed (Scalable): Use Redis. Store the previous_word in Redis with a TTL (Time To Live). This way, if your FastAPI server restarts, the state isn't lost.
'''

import collections

class AgentAssistant:
    def __init__(self):
        # 1. Single-word triggers for O(1) lookup
        self.urgent_keywords = {"fraud", "cancel", "supervisor", "unauthorized"}
        
        # 2. Multi-word triggers
        self.multi_word_intents = {
            "stolen card": "URGENT: Possible Theft",
            "close account": "RETENTION: Customer Churn Risk"
        }
        
        # 3. State management: Store the previous word to catch multi-word intents
        self.previous_word = ""

    def process_stream(self, current_word: str):
        # Clean the input (remove punctuation/lowercase)
        word = current_word.lower().strip().replace(".", "").replace(",", "")
        
        if not word:
            return

        # Check 1: Simple single-word trigger
        if word in self.urgent_keywords:
            self._trigger_alert(f"Keyword Detected: {word}")

        # Check 2: Multi-word trigger (checking current + previous)
        if self.previous_word:
            phrase = f"{self.previous_word} {word}"
            if phrase in self.multi_word_intents:
                self._trigger_alert(f"Phrase Detected: {phrase}")

        # Update state for the next call
        self.previous_word = word

    def _trigger_alert(self, message: str):
        # In a real JPMC system, this would push to a WebSocket, 
        # an SQS queue, or a Salesforce Platform Event.
        print(f"[ALERT] {message}")

# --- Simulation of a live stream ---
assistant = AgentAssistant()
stream = ["Hello", "I", "think", "I", "have", "a", "stolen", "card", "please", "cancel"]

for w in stream:
    assistant.process_stream(w)