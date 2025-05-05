import itertools
from pathlib import Path

from generators.json_generator import JSONTemplatePromptGenerator


class VideoPromptGenerator(JSONTemplatePromptGenerator):
    WORKFLOW_TYPE = "video"
    TEMPLATE_PATH = Path("templates/video.json")

    def __init__(self, requests_per_host: int):
        super().__init__(requests_per_host)

        self.subjects = [
            "red fox",
            "arctic hare",
            "mountain goat",
            "snowy owl",
            "silver wolf",
        ]
        self.actions = [
            "darting",
            "leaping",
            "slicing",
            "gliding",
            "bounding",
        ]
        self.environments = [
            "winter forest",
            "frozen lake",
            "snowy tundra",
            "icy canyon",
            "frosty meadow",
        ]
        self._grid = list(
            itertools.product(
                range(len(self.subjects)),
                range(len(self.actions)),
                range(len(self.environments)),
            )
        )

        self.neg_pool = [
            "low quality",
            "worst quality",
            "deformed",
            "distorted",
            "disfigured",
            "motion smear",
            "motion artifacts",
            "fused fingers",
            "bad anatomy",
            "weird hand",
            "ugly",
        ]

    def make_text(self, var_name: str) -> str:
        idx = self._counter % len(self._grid)
        s, a, e = self._grid[idx]
        if var_name == "positive_video":
            subj = self.subjects[s]
            act = self.actions[a]
            env = self.environments[e]
            text = (
                f"A {subj} {act} through the {env}, "
                "steam rising from its breath in the crisp air."
            )
        elif var_name == "negative_video":
            text = ", ".join(
                self.neg_pool[(idx + i) % len(self.neg_pool)] for i in range(4)
            )
        else:
            raise ValueError(f"Unknown placeholder: {var_name}")

        self._counter += 1
        return text
