from pathlib import Path

from generators.json_generator import JSONTemplatePromptGenerator


class ParallelPromptGenerator(JSONTemplatePromptGenerator):
    WORKFLOW_TYPE = "parallel"
    TEMPLATE_PATH = Path("templates/parallel.json")

    def __init__(self, requests_per_host: int):
        super().__init__(requests_per_host)

        self.themes = [
            "forest glade at dawn",
            "desert canyon under midday sun",
            "mountain overlook shrouded in mist",
            "prairie sunrise with wildflowers",
            "ocean horizon at golden hour",
        ]
        self.themes2 = [
            "city skyline at night",
            "urban street market",
            "industrial port at dusk",
            "neon-lit downtown alley",
            "historic town square in winter",
        ]

        self.neg_pool = [
            "watermark",
            "text",
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
        if var_name == "positive_parallel":
            theme = self.themes[self._counter % len(self.themes)]
            text = (
                f"A photorealistic scene of {theme}, high resolution, cinematic feel."
            )

        elif var_name == "positive_parallel2":
            theme = self.themes2[self._counter % len(self.themes2)]
            text = f"A detailed render of {theme}, vibrant colors, dynamic lighting."

        elif var_name == "negative_parallel":
            bads = [self.neg_pool[(self._counter + i) % len(self.neg_pool)] for i in range(4)]
            text = ", ".join(bads)

        elif var_name == "negative_parallel2":
            bads = [self.neg_pool[(self._counter + i) % len(self.neg_pool)] for i in range(4)]
            text = ", ".join(bads)

        else:
            raise ValueError(f"Unknown placeholder: {var_name}")

        self._counter += 1
        return text
