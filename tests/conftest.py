"""Shared pytest fixtures for the litprinter test suite."""

import builtins

import pytest

from litprinter import DEFAULT_NAMES, ic


@pytest.fixture
def out():
    """Capture ``ic()`` output through a custom outputFunction."""
    lines = []
    ic.configureOutput(outputFunction=lines.append)
    yield lines
    ic.configureOutput(outputFunction=None, prefix='ic| ')


@pytest.fixture(autouse=True)
def restore_builtins():
    """Restore litprinter's builtins after every test.

    ``install()``/``uninstall()`` mutate the real ``builtins`` module, so
    snapshot and restore them to keep tests order-independent.
    """
    saved = {
        name: getattr(builtins, name)
        for name in DEFAULT_NAMES
        if hasattr(builtins, name)
    }
    yield
    for name, value in saved.items():
        setattr(builtins, name, value)
