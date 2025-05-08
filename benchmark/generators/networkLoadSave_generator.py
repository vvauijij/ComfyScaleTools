from pathlib import Path

from generators.simple_generator import SimplePromptGenerator


class NetworkLoadSavePromptGenerator(SimplePromptGenerator):
    WORKFLOW_TYPE = "networkLoadSave"
    TEMPLATE_PATH = Path("templates/networkLoadSave.json")

    def __init__(self, requests_per_host: int):
        super().__init__(requests_per_host)

    def make_text(self, var_name: str) -> str:
        return super().make_text(var_name)
