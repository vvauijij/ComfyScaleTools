import json
import re
from pathlib import Path
from typing import Any, Dict, Set


class JSONTemplatePromptGenerator:
    """
    Base for file‐backed workflows. Subclasses define:
      - TEMPLATE_PATH: Path to JSON with {{vars}} in each CLIPTextEncode/NetworkRequestMocker node's inputs.text
      - WORKFLOW_TYPE: string to go into extra_data.workflow
      - make_text(var_name: str) -> str
    """

    client_id = "531fd600fe1043cfb6640a6d005fe8a6"
    _placeholder_re = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    TEMPLATE_PATH: Path
    WORKFLOW_TYPE: str

    def __init__(self, requests_per_host: int):
        self.requests_per_host = requests_per_host
        self._counter = 0
        if not hasattr(self, "TEMPLATE_PATH") or not hasattr(self, "WORKFLOW_TYPE"):
            raise ValueError("Subclasses must define TEMPLATE_PATH and WORKFLOW_TYPE")

        self._skeleton = json.loads(self.TEMPLATE_PATH.read_text())

    def make_text(self, var_name: str) -> str:
        """
        Fill in a placeholder variable.
        Subclasses override with logic for positive/negative, etc.
        """
        raise NotImplementedError

    def generate(self) -> Dict[str, Any]:
        prompt = json.loads(self.TEMPLATE_PATH.read_text())

        vars_needed: Set[str] = set()
        for node in prompt.values():
            if (
                node.get("class_type") == "CLIPTextEncode"
                or node.get("class_type") == "NetworkRequestMocker"
            ):
                txt = node["inputs"].get("text", "")
                for m in self._placeholder_re.finditer(txt):
                    vars_needed.add(m.group(1))

        mapping: Dict[str, str] = {}
        for var in vars_needed:
            mapping[var] = self.make_text(var)

        for node in prompt.values():

            def repl(m):
                name = m.group(1)
                return mapping.get(name, m.group(0))

            if (
                node.get("class_type") == "CLIPTextEncode"
                or node.get("class_type") == "NetworkRequestMocker"
            ):
                orig = node["inputs"].get("text", "")
                node["inputs"]["text"] = self._placeholder_re.sub(repl, orig)

        payload = {
            "client_id": self.client_id,
            "prompt": prompt,
            "extra_data": {"workflow": self.WORKFLOW_TYPE},
        }

        self._counter += 1
        return payload
