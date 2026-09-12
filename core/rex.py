"""
JHOSAI REX V2 - REX Engine
Connects Core, Router, Model Manager, Tools and Memory.
"""

from .core import REXCore
from .models import ModelManager
from .tools import ToolRegistry
from .memory import REXMemory


class REXEngine:

    def __init__(self):
        self.core = REXCore()
        self.models = ModelManager()
        self.tools = ToolRegistry()
        self.memory = REXMemory()

    def process(
        self,
        message: str,
        has_file: bool = False,
        has_image: bool = False,
    ) -> dict:
        """
        Main REX execution pipeline.
        """

        # 1. REX Core + Router
        route = self.core.process(
            message=message,
            has_file=has_file,
            has_image=has_image,
        )

        # 2. Store user message
        self.memory.add_user_message(message)

        # 3. Return routing information
        return {
            "message": message,
            "task": route["task"],
            "has_file": has_file,
            "has_image": has_image,
            "memory_count": self.memory.count(),
        }