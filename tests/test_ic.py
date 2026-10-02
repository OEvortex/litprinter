"""Tests for ic() debugging output."""

import pytest

from litprinter import IceCreamDebugger, ic


@pytest.fixture
def out():
    """Capture ic output through a custom outputFunction."""
    lines = []
    ic.configureOutput(outputFunction=lines.append)
    yield lines
    ic.configureOutput(outputFunction=None, prefix='ic| ')


def test_simple_name_has_no_context(out):
    x = 42
    ic(x)
    assert out[-1] == 'ic| x: 42'


def test_expression_adds_context(out):
    x = 42
    ic(x + 1)
    assert '[test_ic.py:' in out[-1]
    assert '>>> x + 1: 43' in out[-1]


def test_call_adds_context(out):
    items = [1, 2, 3]
    ic(len(items))
    assert '[test_ic.py:' in out[-1]


def test_literal_is_not_repeated(out):
    ic(5)
    assert out[-1] == 'ic| 5'


def test_context_mode_always(out):
    ic.configureOutput(contextMode='always')
    x = 1
    ic(x)
    assert '[test_ic.py:' in out[-1]
    ic.configureOutput(contextMode='auto')


def test_context_mode_never(out):
    ic.configureOutput(contextMode='never')
    x = 1
    ic(x + 1)
    assert '[' not in out[-1]
    ic.configureOutput(contextMode='auto')


def test_per_call_override(out):
    x = 1
    ic(x, includeContext=True)
    assert '[test_ic.py:' in out[-1]


def test_returns_value(out):
    assert ic(7) == 7
    assert ic(1, 2) == (1, 2)
    assert ic() is None


def test_disable_enable(out):
    ic.disable()
    ic(99)
    assert not out
    ic.enable()
    ic(99)
    assert out


def test_format_without_printing():
    x = 5
    assert 'x: 5' in ic.format(x)


def test_pair_delimiter(out):
    ic.configureOutput(pairDelimiter=' | ')
    a, b = 1, 2
    ic(a, b)
    assert out[-1] == 'ic| a: 1 | b: 2'
    ic.configureOutput(pairDelimiter=', ')


def test_invalid_context_mode():
    with pytest.raises(ValueError):
        ic.configureOutput(contextMode='nope')


def test_debugger_prefix_callable():
    lines = []
    dbg = IceCreamDebugger(prefix=lambda: 'cb| ', outputFunction=lines.append)
    dbg.configureOutput(contextMode='never')
    x = 3
    dbg(x)
    assert lines[-1] == 'cb| x: 3'
