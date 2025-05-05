import itertools
from pathlib import Path

from generators.json_generator import JSONTemplatePromptGenerator


class TryOnPromptGenerator(JSONTemplatePromptGenerator):
    WORKFLOW_TYPE = "tryOn"
    TEMPLATE_PATH = Path("templates/tryOn.json")

    def __init__(self, requests_per_host: int):
        super().__init__(requests_per_host)

        self.clothing_items = [
            "hoodie",
            "denim jacket",
            "leather jacket",
            "t-shirt",
            "sweater",
            "summer dress",
            "jeans",
            "trench coat",
        ]
        self.poses = [
            "standing straight",
            "walking forward",
            "sitting casually",
            "turning to the side",
            "reaching out",
        ]
        self.lightings = [
            "soft studio lighting",
            "natural daylight",
            "dramatic spotlight",
            "golden hour glow",
            "high-contrast indoor light",
        ]
        self._grid = list(
            itertools.product(
                range(len(self.clothing_items)),
                range(len(self.poses)),
                range(len(self.lightings)),
            )
        )

        self.neg_pool = [
            "low quality",
            "blurry",
            "deformed",
            "poorly lit",
            "unnatural colors",
            "bad anatomy",
            "artifact",
            "oversaturated",
            "underexposed",
            "motion blur",
            "pixelated",
        ]

    def make_text(self, var_name: str) -> str:
 
        idx = self._counter % len(self._grid)
        c_idx, p_idx, l_idx = self._grid[idx]

        if var_name == "positive_tryOn":
            clothing = self.clothing_items[c_idx]
            pose = self.poses[p_idx]
            lighting = self.lightings[l_idx]
            text = (
                f"A high-resolution photo of a model {pose}, "
                f"wearing a {clothing} under {lighting}, "
                "looking natural and well-fitted."
            )

        elif var_name == "negative_tryOn":
            negatives = [
                self.neg_pool[(idx + i) % len(self.neg_pool)] for i in range(4)
            ]
            text = ", ".join(negatives)

        else:
            raise ValueError(f"Unknown placeholder: {var_name}")

        self._counter += 1
        return text
