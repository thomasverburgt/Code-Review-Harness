"""Package command entry points."""

from __future__ import annotations

from ._legacy import load


def check_repository() -> int:
    return int(load("check_repository_structure").main())


def validate_vertical() -> int:
    return int(load("validate_vertical_slice").main())
