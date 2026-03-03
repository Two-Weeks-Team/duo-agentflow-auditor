"""Example safe Python script — no security findings expected."""

import json
import os
import subprocess
from pathlib import Path


def run_command(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return result.stdout


def load_config(config_path: Path) -> dict:
    resolved = config_path.expanduser().resolve()
    with open(resolved) as f:
        return json.load(f)


def get_api_key() -> str:
    return os.environ.get("API_KEY", "")


def fetch_data(url: str) -> str:
    if not url.startswith("https://"):
        raise ValueError("Only HTTPS URLs are allowed")
    result = subprocess.run(
        ["curl", "--silent", "--fail", url],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def process_input(raw: str) -> dict:
    import ast

    return ast.literal_eval(raw)
