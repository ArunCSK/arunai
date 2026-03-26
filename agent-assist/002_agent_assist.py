'''
If this stream was coming in from 10,000 agents simultaneously, how would you change your Python code to ensure the AgentAssistant class is thread-safe? (Hint: Think about threading.Lock or using a stateless approach with Redis).

Would you like to try implementing the thread-safe version?
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