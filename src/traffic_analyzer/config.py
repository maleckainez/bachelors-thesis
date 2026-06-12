"""Configuration loading for pipeline runs.

Todo:
- load YAML configuration,
- validate required fields,
- expose one config object used by scripts and benchmarks.
"""

from pathlib import Path

import yaml


def load_config(config_path: str | Path) -> dict:
    """Load a YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration file is empty or misses required sections.

    Returns:
        Parsed configuration dictionary.
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
    """Validate top-level sections in a configuration dictionary.

    Args:
        config: Parsed configuration dictionary.

    Raises:
        ValueError: If any required top-level section is missing.
    """
    required_sections = {"video", "detection", "tracking", "output"}
    missing = required_sections - set(config)

    if missing:
        raise ValueError(f"Config file is missing sections: {sorted(missing)}")
