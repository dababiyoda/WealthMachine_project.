import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel


class BaseConfig(BaseModel):
    """Generic configuration loader supporting JSON and YAML."""

    class Config:
        extra = "forbid"

    @classmethod
    def from_yaml_or_json(cls, file_path: str) -> "BaseConfig":
        """Load a single YAML or JSON config file."""
        with open(file_path, "r", encoding="utf-8") as f:
            if file_path.endswith((".yaml", ".yml")):
                data: Dict[str, Any] = yaml.safe_load(f)
            else:
                data = json.load(f)
        return cls(**data)

    @classmethod
    def load(cls, path: str, name: Optional[str] = None) -> "BaseConfig":
        """
        Load a configuration file from a directory.  Supports `.json`, `.yaml`, `.yml`.

        Args:
            path: Directory containing configuration files.
            name: Optional file base name (without extension).  Defaults to the
                class name in lowercase.

        Returns:
            An instance of the configuration class populated from the file.
        """
        name = name or cls.__name__.lower()
        base_path = Path(path)
        for ext in (".yaml", ".yml", ".json"):
            file_path = base_path / f"{name}{ext}"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    if ext in (".yaml", ".yml"):
                        data: Dict[str, Any] = yaml.safe_load(f)
                    else:
                        data = json.load(f)
                return cls(**data)
        raise FileNotFoundError(f"Configuration file {name}(.yaml/.json) not found in {path}")
