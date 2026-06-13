"""Helpers for loading and validating pipeline configuration files."""

from pathlib import Path

import yaml


def load_config(config_path: str | Path) -> dict:
    """Load and validate a YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or misses required sections.

    Returns:
        Parsed configuration mapping.
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError("Config file not fount at %s", config_path)

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError("Config file is empty!")
    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    """Validate required top-level sections in a configuration mapping.

    Args:
        config: Parsed configuration mapping.

    Raises:
        ValueError: If any required top-level section is missing.
    """
    required_sections = {"video", "detection", "tracking", "output"}
    missing = required_sections - set(config)

    if missing:
        raise ValueError(f"Config file is missing sections: {sorted(missing)}")
