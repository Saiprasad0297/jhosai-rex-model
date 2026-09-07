"""
JHOSAI REX V2 - REX Router
Detects the type of task requested by the user.
"""


class REXRouter:

    def __init__(self):
        self.task_keywords = {
            "coding": [
                "code",
                "python",
                "javascript",
                "java",
                "program",
                "programming",
                "debug",
                "bug",
                "error",
                "script",
                "function",
                "api",
                "git",
            ],

            "reasoning": [
                "explain",
                "why",
                "analyze",
                "analysis",
                "compare",
                "calculate",
                "solve",
                "reasoning",
                "logic",
                "architecture",
            ],

            "fast": [
                "hello",
                "hi",
                "hey",
                "thanks",
                "thank you",
                "good morning",
                "good night",
            ],
        }

    def detect_task(self, message: str) -> str:
        """
        Detect the most appropriate task type.
        """

        if not message:
            return "auto"

        text = message.lower()

        scores = {
            "coding": 0,
            "reasoning": 0,
            "fast": 0,
        }

        for task, keywords in self.task_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[task] += 1

        best_task = max(scores, key=scores.get)

        if scores[best_task] == 0:
            return "auto"

        return best_task

    def route(self, message: str) -> dict:
        """
        Return routing information.
        """

        task = self.detect_task(message)

        return {
            "task": task,
            "message": message,
        }