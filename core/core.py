"""
JHOSAI REX V2 - REX Core
Central processing layer between the user and REX Router.
"""

from .router import REXRouter


class REXCore:

    def __init__(self):
        self.router = REXRouter()

    def understand(
        self,
        message: str,
        has_file: bool = False,
        has_image: bool = False,
    ) -> dict:
        """Understand and normalize the incoming request."""

        if not message:
            return {
                "message": "",
                "valid": False,
                "has_file": has_file,
                "has_image": has_image,
            }

        return {
            "message": message.strip(),
            "valid": True,
            "has_file": has_file,
            "has_image": has_image,
        }

    def route(self, request: dict) -> dict:
        """Send the request to REX Router."""

        return self.router.route(
            message=request["message"],
            has_file=request["has_file"],
            has_image=request["has_image"],
        )

    def process(
        self,
        message: str,
        has_file: bool = False,
        has_image: bool = False,
    ) -> dict:
        """Main REX Core pipeline."""

        request = self.understand(
            message=message,
            has_file=has_file,
            has_image=has_image,
        )

        if not request["valid"]:
            return {
                "task": "auto",
                "message": "",
                "has_file": has_file,
                "has_image": has_image,
            }

        return self.route(request)