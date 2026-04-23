'''
Let’s do a "Live Coding" task. This simulates the Streaming Data problem often seen at JPMC.

The Prompt:
Imagine you are receiving a stream of words from the amazon-transcribe library. Your task is to write a Python class, AgentAssistant, that monitors this stream for "Urgent Intent" keywords.

Constraints:

The keywords are: ["fraud", "cancel", "supervisor", "unauthorized"].

The input is a continuous stream of strings (one word at a time).

When a keyword is detected, you must trigger an internal alert (a print statement is fine for now).

The Senior Twist: Some "intents" are two words, like "stolen card". Your code must be able to detect "stolen card" even if "stolen" is the last word of one chunk and "card" is the first word of the next.

Why this is a "Senior" Answer:Stateful Memory: By using self.previous_word, you solve the "Twist." If "stolen" arrives at 10:00:01 AM and "card" arrives at 10:00:02 AM, your code correctly links them.Efficiency: I used a set for urgent_keywords. In Python, checking if x in my_set is $O(1)$, whereas if x in my_list is $O(n)$. At the scale of millions of banking calls, this matters.Data Cleaning: Real-world audio transcripts are messy. Adding .lower().strip() and removing punctuation shows you understand that raw data is never perfect.Encapsulation: Using a private method _trigger_alert demonstrates that you understand how to separate the detection logic from the notification logic.

How to explain this in the interview:
"I implemented a stateful stream processor. I used a dictionary/set for constant-time lookups to keep latency low. To handle multi-word phrases across stream chunks, I maintained a small buffer of the previous state. For a more complex set of thousands of phrases, I might upgrade this to an Aho-Corasick automaton to scan the text in a single pass."

'''

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
        # In a real JPMC system, this would push to a WebSocket or SQS
        print(f"[ALERT] {message}")

# --- Simulation ---
assistant = AgentAssistant()
stream = ["Hello", "I", "think", "I", "have", "a", "stolen", "card", "please", "cancel"]

for w in stream:
    assistant.process_stream(w)