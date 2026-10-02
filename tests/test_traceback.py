"""Tests for the traceback renderer."""

import sys

import pytest

from litprinter import traceback
from litprinter.traceback import PrettyTraceback


def make_tb(**kwargs):
    """Build a ZeroDivisionError traceback with a real frame."""
    try:

        def inner(a, b):
            _secret = 'hidden'
            return a / b

        inner(1, 0)
    except ZeroDivisionError as exc:
        return PrettyTraceback(type(exc), exc, exc.__traceback__, **kwargs)


def test_default_renders_traceback():
    out = str(make_tb())
    assert 'ZeroDivisionError' in out
    assert 'division by zero' in out


def test_show_locals():
    out = str(make_tb(show_locals=True))
    assert 'Variables:' in out
    assert '_secret' in locals_block(out)


def locals_block(out):
    """Return only the "Variables:" block of a rendered traceback.

    The block ends at the next frame separator so later frames' source
    snippets (which contain the same variable names) are excluded.
    """
    from litprinter import Colors

    plain = Colors.strip_ansi(out)
    if 'Variables:' not in plain:
        return ''
    block = plain.split('Variables:', 1)[1]
    return block.split('\u2500', 1)[0]


def test_locals_hide_sunder_hides_single_underscore():
    out = str(make_tb(show_locals=True, locals_hide_sunder=True))
    assert '_secret' not in locals_block(out)


def test_locals_show_sunder_by_default():
    out = str(make_tb(show_locals=True))
    assert '_secret' in locals_block(out)


def test_max_frames_truncates_and_reports():
    tb = make_tb(max_frames=0)
    out = str(tb)
    assert 'omitted' in out
    assert 'max_frames=0' in out


def test_suppress_hides_frames():
    out = str(make_tb(suppress=['test_traceback']))
    assert 'in inner()' not in out


def test_is_suppressed_is_case_insensitive():
    tb = make_tb(suppress=['SITE-PACKAGES'])
    assert tb.is_suppressed('/x/SITE-packages/y.py')
    assert not tb.is_suppressed('/x/other.py')


def test_every_custom_theme_resolves():
    for name, cls in traceback.CUSTOM_STYLES.items():
        assert cls is not None, name


def test_unknown_theme_warns_and_falls_back(capsys):
    try:
        traceback.install(theme='definitely-not-a-theme')
        assert traceback._current_hook_options['theme'] == 'cyberpunk'
    finally:
        traceback.uninstall()
    assert 'not found' in capsys.readouterr().err


def test_bad_theme_type_warns(capsys):
    try:
        traceback.install(theme=42)
        assert traceback._current_hook_options['theme'] == 'cyberpunk'
    finally:
        traceback.uninstall()
    assert 'must be a string or Style class' in capsys.readouterr().err


def test_install_and_uninstall_roundtrip():
    original = sys.excepthook
    try:
        traceback.install(show_locals=True, theme='monokai')
        assert sys.excepthook is traceback.pretty_excepthook
        assert traceback._current_hook_options['show_locals'] is True
    finally:
        traceback.uninstall()
    assert sys.excepthook is original


def test_install_forwards_new_options():
    try:
        traceback.install(
            locals_hide_sunder=True,
            suppress=['nope'],
            max_frames=7,
        )
        opts = traceback._current_hook_options
        assert opts['locals_hide_sunder'] is True
        assert list(opts['suppress']) == ['nope']
        assert opts['max_frames'] == 7
    finally:
        traceback.uninstall()


def test_traceback_alias():
    assert traceback.Traceback is traceback.PrettyTraceback


def test_str_and_print(tmp_path, capsys):
    tb = make_tb()
    assert str(tb)
    tb.print()
    assert 'ZeroDivisionError' in capsys.readouterr().err


@pytest.mark.parametrize('theme', ['cyberpunk', 'dracula', 'nord', 'monokai'])
def test_install_accepts_each_theme(theme):
    try:
        traceback.install(theme=theme)
        assert traceback._current_hook_options['theme'] == theme
    finally:
        traceback.uninstall()
