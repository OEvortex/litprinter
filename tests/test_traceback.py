"""Tests for the traceback renderer."""

import sys


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


def test_single_builtin_theme():
    """There is exactly one style, shared by ic() and the traceback."""
    from litprinter import LitPrinterStyle

    assert make_tb().style_cls is LitPrinterStyle
    assert not hasattr(traceback, 'CUSTOM_STYLES')


def test_theme_argument_is_gone():
    import inspect

    assert 'theme' not in inspect.signature(traceback.install).parameters
    assert (
        'theme' not in inspect.signature(traceback.PrettyTraceback.__init__).parameters
    )


def test_install_and_uninstall_roundtrip():
    # The .pth autoloader installs the hook at interpreter startup, so
    # uninstall() must restore the interpreter's own default hook.
    assert sys.excepthook is traceback.pretty_excepthook
    try:
        traceback.install(show_locals=True)
        assert sys.excepthook is traceback.pretty_excepthook
        assert traceback._current_hook_options['show_locals'] is True
    finally:
        traceback.uninstall()
    assert sys.excepthook is sys.__excepthook__


def test_reinstall_after_uninstall():
    traceback.uninstall()
    assert sys.excepthook is sys.__excepthook__
    try:
        traceback.install()
        assert sys.excepthook is traceback.pretty_excepthook
    finally:
        traceback.uninstall()


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


def test_install_does_not_carry_a_theme():
    try:
        traceback.install()
        assert 'theme' not in traceback._current_hook_options
    finally:
        traceback.uninstall()
