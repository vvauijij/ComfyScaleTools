import itertools
from pathlib import Path

from generators.json_generator import JSONTemplatePromptGenerator


class SimplePromptGenerator(JSONTemplatePromptGenerator):
    WORKFLOW_TYPE = "simple"
    TEMPLATE_PATH = Path("templates/simple.json")

    def __init__(self, requests_per_host: int):
        super().__init__(requests_per_host)

        self.adjectives = [
            "vibrant",
            "serene",
            "dramatic",
            "ethereal",
            "hyper-realistic",
        ]
        self.subjects = [
            "sunset over the mountains",
            "forest stream",
            "desert dunes",
            "city skyline at night",
            "ocean waves crashing",
        ]
        self.styles = [
            "oil painting",
            "digital illustration",
            "photograph",
            "watercolor",
            "3D render",
        ]
        self._grid = list(
            itertools.product(
                range(len(self.adjectives)),
                range(len(self.subjects)),
                range(len(self.styles)),
            )
        )

        self.neg_pool = [
            "text",
            "watermark",
            "lowres",
            "blurry",
            "artifact",
            "oversaturated",
            "pixelated",
            "underexposed",
            "bad anatomy",
            "deformed",
        ]

    def make_text(self, var_name: str) -> str:
        idx = self._counter % len(self._grid)
        a_idx, s_idx, st_idx = self._grid[idx]

        if var_name == "positive_simple":
            adj = self.adjectives[a_idx]
            subj = self.subjects[s_idx]
            style = self.styles[st_idx]
            text = f"A {adj} {subj}, rendered as a {style}."

        elif var_name == "negative_simple":
            negs = [self.neg_pool[(idx + i) % len(self.neg_pool)] for i in range(4)]
            text = ", ".join(negs)

        else:
            raise ValueError(f"Unknown placeholder: {var_name}")

        self._counter += 1
        return text
