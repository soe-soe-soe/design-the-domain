"""Registry of the test plugins; each module covers one concern."""

pytest_plugins = [
    "tests.plugins.levels",
    "tests.fixtures.database",
    "tests.fixtures.wiring",
]
