import itertools
from pathlib import Path

from generators.json_generator import JSONTemplatePromptGenerator


class DesignPromptGenerator(JSONTemplatePromptGenerator):
    WORKFLOW_TYPE = "design"
    TEMPLATE_PATH = Path("templates/design.json")

    def __init__(self, requests_per_host: int):
        super().__init__(requests_per_host)

        self.adjectives = ["luxurious", "cozy", "spacious", "bright", "elegant"]
        self.styles = ["modern", "minimalist", "industrial", "Scandinavian", "bohemian"]
        self.rooms = ["living room", "bedroom", "kitchen", "home office", "bathroom"]

        self.designers = [
            "Kelly Hoppen",
            "Joanna Gaines",
            "Philippe Starck",
            "Zaha Hadid",
            "Frank Lloyd Wright",
        ]

        self._grid = list(
            itertools.product(
                range(len(self.adjectives)),
                range(len(self.styles)),
                range(len(self.rooms)),
            )
        )

        self.neg_pool = [
            "unclear",
            "low resolution",
            "distorted",
            "tacky",
            "oversaturated",
            "out of frame",
            "poor drawing",
            "incomplete",
            "poor art",
            "poor quality",
            "watermark",
            "signature",
            "artifact",
            "blurry",
        ]

    def make_text(self, var_name: str) -> str:
        idx = self._counter % len(self._grid)
        adj_idx, style_idx, room_idx = self._grid[idx]

        if var_name == "positive_design":
            adj = self.adjectives[adj_idx]
            style = self.styles[style_idx]
            room = self.rooms[room_idx]
            text = (
                f"A {adj} {style} interior of a {room}, "
                "featuring high-end materials, natural light, 8K resolution, ultra-realistic."
            )

        elif var_name == "negative_design":
            bads = [self.neg_pool[(idx + i) % len(self.neg_pool)] for i in range(4)]
            text = ", ".join(bads)

        elif var_name == "positive_design2":
            designer = self.designers[idx % len(self.designers)]
            style = self.styles[style_idx]
            room = self.rooms[room_idx]
            text = (
                f"An interior design concept by {designer}, "
                f"{style} style {room}, luxurious finishes, cinematic lighting, photo-realistic."
            )

        elif var_name == "negative_design2":
            bads = [self.neg_pool[(idx + i) % len(self.neg_pool)] for i in range(4)]
            text = ", ".join(bads)

        else:
            raise ValueError(f"Unknown placeholder: {var_name}")

        self._counter += 1
        return text
