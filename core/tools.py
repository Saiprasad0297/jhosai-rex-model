"""
JHOSAI REX V2 - Tool Registry
Central registry for tools available to REX.
"""


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, name: str, tool, description: str = ""):
        """
        Register a tool with REX.
        """
        self.tools[name] = {
            "tool": tool,
            "description": description,
        }

    def get(self, name: str):
        """
        Get a registered tool.
        """
        return self.tools.get(name)

    def available_tools(self) -> list:
        """
        Return the names of all registered tools.
        """
        return list(self.tools.keys())

    def has_tool(self, name: str) -> bool:
        """
        Check whether a tool exists.
        """
        return name in self.tools

    def execute(self, name: str, *args, **kwargs):
        """
        Execute a registered tool.
        """

        if name not in self.tools:
            raise ValueError(f"Tool not registered: {name}")

        tool = self.tools[name]["tool"]

        if not callable(tool):
            raise TypeError(f"Tool '{name}' is not callable.")

        return tool(*args, **kwargs)