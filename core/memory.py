"""
JHOSAI REX V2 - Memory
Manages conversation history.
"""


class REXMemory:

    def __init__(self, max_messages=20):
        self.max_messages = max_messages
        self.messages = []

    def add_user_message(self, content: str):
        self.messages.append({
            "role": "user",
            "content": content,
        })
        self._limit_memory()

    def add_assistant_message(self, content: str):
        self.messages.append({
            "role": "assistant",
            "content": content,
        })
        self._limit_memory()

    def get_history(self):
        return self.messages.copy()

    def clear(self):
        self.messages.clear()

    def _limit_memory(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def count(self):
        return len(self.messages)