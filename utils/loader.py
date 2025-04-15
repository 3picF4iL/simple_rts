import os
import yaml

def load_object_definitions(config_path="assets/conf") -> dict:
    object_defs = {}
    config_path = os.path.join(os.path.dirname(__file__), "..", "assets", "conf")
    config_path = os.path.abspath(config_path)

    for filename in os.listdir(config_path):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            key = filename.split(".")[0]
            full_path = os.path.join(config_path, filename)

            with open(full_path, "r", encoding="utf-8") as f:
                object_defs[key] = yaml.safe_load(f)

    return object_defs