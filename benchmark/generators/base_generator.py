from typing import Any, Dict

class PromptGenerator:
    """
    Abstract base: subclasses must implement make_text(var_name) -> str.
    """
    client_id = "531fd600fe1043cfb6640a6d005fe8a6"

    def __init__(self, requests_per_host: int):
        self.requests_per_host = requests_per_host
        self._counter = 0

    def make_text(self, var_name: str) -> str:
        """
        Given a placeholder name (e.g. "positive_video"), return the text
        to substitute. Subclasses override this.
        """
        raise NotImplementedError

    def generate(self) -> Dict[str, Any]:
        raise NotImplementedError
