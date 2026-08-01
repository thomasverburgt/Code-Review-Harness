"""Temporary resolver for implementations retained under ``tools``."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


def _tools_directory() -> Path:
    try:
        package = importlib.import_module("tools")
        if package.__file__:
            return Path(package.__file__).resolve().parent
    except ModuleNotFoundError:
        pass
    return Path(__file__).resolve().parents[2] / "tools"


TOOLS = _tools_directory()


def load(name: str) -> ModuleType:
    tools_path = str(TOOLS)
    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)
    return importlib.import_module(name)


def expose(name: str, namespace: dict[str, Any]) -> None:
    implementation = load(name)
    public = getattr(implementation, "__all__", None)
    if public is None:
        public = [item for item in vars(implementation) if not item.startswith("_")]
    namespace.update({item: getattr(implementation, item) for item in public})
    namespace["__all__"] = list(public)
    namespace["__legacy_implementation__"] = implementation.__file__
