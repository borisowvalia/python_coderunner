import os
import yaml


def load(module: str, task: str):
    path = os.path.join(
        os.path.dirname(__file__),
        "exercises",
        "modules",
        f"module_{module}",
        "tasks",
        f"task_{task}.yaml")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
