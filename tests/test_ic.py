"""Tests for ic() debugging output."""

import pytest

from litprinter import IceCreamDebugger, ic


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
    assert 'a: 1 | b: 2' in out[-1]
    ic.configureOutput(pairDelimiter=', ')


def test_multiline_value_is_auto_aligned(out):
    """Continuation lines hang under the value column, not column 0."""
    data = {'alpha': 1, 'beta': 2, 'gamma': 3, 'delta': 4, 'epsilon': 5}
    ic(data)
    lines = out[-1].split('\n')
    assert len(lines) > 1
    assert lines[0].startswith('ic| data: {')
    # Every continuation line is indented past the first column.
    assert all(line.startswith(' ') for line in lines[1:])


def test_alignment_accounts_for_context(out):
    """The indent accounts for the prefix *and* the context column."""
    big = {'alpha': 1, 'beta': 2, 'gamma': 3, 'delta': 4, 'epsilon': 5}
    ic(big, includeContext=True)
    lines = out[-1].split('\n')
    assert len(lines) > 1
    # Indented past the prefix *and* the context column.
    assert lines[1].startswith(' ' * 25)


def test_single_theme_is_used():
    import litprinter

    assert not hasattr(litprinter, 'set_style')
    assert not hasattr(litprinter, 'get_style')
    assert litprinter.LitPrinterStyle is not None


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


def test_module_level_context_drops_in_module(out):
    """Top-level code has no function, so `in <module>` is omitted."""
    ic(len([1, 2, 3]))
    assert 'in <module>' not in out[-1]
    assert out[-1].startswith('ic| [test_ic.py:')
    assert '>>> len([1, 2, 3]): 3' in out[-1]


def test_context_keeps_function_name(out):
    """Inside a function the `in name()` suffix is kept."""

    def compute():
        return len([1, 2, 3])

    ic(compute())
    # The context reports the caller frame, i.e. this test function.
    assert 'in test_context_keeps_function_name()' in out[-1]


def test_context_never_uses_unknown_form():
    dbg = IceCreamDebugger(
        prefix='ic| ',
        outputFunction=lambda s: None,
        contextMode='always',
    )
    assert dbg._format_context(None) == '<unknown>:0'
