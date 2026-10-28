"""Shared configuration and environment loading."""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT_DIR / "config"
DATA_DIR = ROOT_DIR / "data"


def load_yaml(path: str | Path) -> dict:
    """Load a YAML file from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_required_env(key: str) -> str:
    """Return an environment variable or raise a clear error."""
    value = os.getenv(key)
    if not value:
        raise ValueError(
            f"Missing required environment variable: {key}. "
            f"Set it in a .env file or export it before running."
        )
    return value


def model_client_config() -> dict:
    """Return the active model client configuration."""
    model_base_url = os.getenv("MODEL_BASE_URL")
    using_nrp = not bool(model_base_url)
    return {
        "provider": os.getenv("MODEL_PROVIDER", "byom" if not using_nrp else "nrp"),
        "api_key": os.getenv("NRP_API_KEY" if using_nrp else "BYOM_API_KEY", ""),
        "base_url": model_base_url or os.getenv("NRP_BASE_URL", "https://api.openai.com/v1"),
        "model": os.getenv("MODEL_NAME", "gpt-oss"),
        "fallback_model": os.getenv("FALLBACK_MODEL", "kimi"),
        "fallback_base_url": os.getenv("FALLBACK_BASE_URL", ""),
    }
