"""Marks every test as unit or integration from its path (ADR 012, structure.md "Tests").

A test mirrors the building block it tests, and the test level follows the building block:
under `domain/`, a path through `model/` is a unit test, any other is an integration test;
`ops/` is integration, everything else unit. CI selects with `-m unit` and `-m integration`.

Transition: tests not yet moved to their mirrored path still sit under `unit/` or
`integration/`; that folder decides. Remove the rule once both folders are gone.
"""

from pathlib import Path

import pytest

TESTS_ROOT = Path(__file__).resolve().parents[1]
LEGACY_LEVEL_FOLDERS = {"unit", "integration"}


def level_of(path: Path) -> str:
    parts = path.resolve().relative_to(TESTS_ROOT).parts
    if parts[0] in LEGACY_LEVEL_FOLDERS:
        return parts[0]
    if parts[0] == "domain":
        return "unit" if "model" in parts else "integration"
    if parts[0] == "ops":
        return "integration"
    return "unit"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        item.add_marker(getattr(pytest.mark, level_of(item.path)))
