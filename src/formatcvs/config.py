import os
import re
from pathlib import Path

import yaml

ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]+))?\}")


def replace_env_vars(value):
    if isinstance(value, str):
        match = ENV_PATTERN.fullmatch(value)

        if match:
            env_name = match.group(1)
            default = match.group(2)

            return os.getenv(env_name, default)

    return value


def process_dict(data):
    if isinstance(data, dict):
        return {key: process_dict(value) for key, value in data.items()}

    if isinstance(data, list):
        return [process_dict(item) for item in data]

    return replace_env_vars(data)


def read_config(path: Path) -> dict:
    with open(path) as f:
        config = yaml.safe_load(f)

    return process_dict(config)


def write_config(path: Path, config: dict):
    with open(path, "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)
