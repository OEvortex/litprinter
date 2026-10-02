"""Tests for ic.print, ic.log and markup rendering."""

import io

import pytest

from litprinter import ic
from litprinter.markup import render_markup, strip_markup


def test_print_is_drop_in():
    buf = io.StringIO()
    ic.print('a', 'b', sep='|', end='!', file=buf)
    assert buf.getvalue() == 'a|b!'


def test_print_non_string_values():
    buf = io.StringIO()
    ic.print(1, 2.5, True, None, file=buf)
    assert buf.getvalue() == '1 2.5 True None\n'


def test_print_respects_disable():
    ic.disable()
    try:
        buf = io.StringIO()
        ic.print('still prints', file=buf)
        assert buf.getvalue() == 'still prints\n'
    finally:
        ic.enable()


def test_print_markup_stripped_when_not_tty():
    buf = io.StringIO()
    ic.print('[bold red]danger[/]', file=buf)
    assert buf.getvalue() == 'danger\n'


def test_print_markup_forced_color():
    buf = io.StringIO()
    ic.print('[bold]x[/]', file=buf, color=True)
    assert '\033[' in buf.getvalue()
    assert 'x' in buf.getvalue()


def test_print_markup_opt_out():
    buf = io.StringIO()
    ic.print('[bold]x[/]', file=buf, color=True, markup=False)
    assert buf.getvalue() == '[bold]x[/]\n'


def test_print_flush():
    flushed = []

    class Stream(io.StringIO):
        def flush(self):
            flushed.append(True)

    ic.print('x', file=Stream(), flush=True)
    assert flushed


def test_render_markup_colors():
    out = render_markup('[red]a[/red]', color=True)
    assert out.startswith('\033[31m')
    assert out.endswith('\033[0m')


def test_render_markup_nesting():
    out = render_markup('[bold][red]x[/red][/bold]', color=True)
    assert out.count('\033[0m') >= 1
    assert 'x' in out


def test_render_markup_unknown_tag_is_literal():
    out = render_markup('[unknowntag]x', color=True)
    assert '[unknowntag]x' == out


def test_render_markup_hex_and_rgb():
    assert render_markup('[#ff0000]x', color=True) != '[#ff0000]x'
    assert render_markup('[rgb(1,2,3)]x', color=True) != '[rgb(1,2,3)]x'


def test_render_markup_bold_default_style():
    out = render_markup('x', style='bold', color=True)
    assert out.startswith('\033[1m')


def test_strip_markup():
    assert strip_markup('[bold][red]x[/red][/bold]') == 'x'
    assert strip_markup('[weird]x') == '[weird]x'


def test_log_levels():
    buf = io.StringIO()
    ic.info('hello', file=buf)
    assert 'INFO' in buf.getvalue()
    assert 'hello' in buf.getvalue()


def test_log_color():
    buf = io.StringIO()
    ic.error('bad', file=buf, color=True)
    assert '\033[31m' in buf.getvalue()


def test_log_timestamp():
    buf = io.StringIO()
    ic.log('x', level='info', file=buf, timestamp=True)
    assert len(buf.getvalue().split(' ')[0]) == 8  # HH:MM:SS


def test_log_sep():
    buf = io.StringIO()
    ic.info('a', 'b', file=buf, sep='-')
    assert 'a-b' in buf.getvalue()


def test_log_unknown_level():
    with pytest.raises(ValueError):
        ic.log('x', level='nope', file=io.StringIO())


def test_log_shortcuts_exist():
    for name in ('debug', 'info', 'success', 'warning', 'warn', 'error', 'critical'):
        assert callable(getattr(ic, name))


def test_module_level_print_alias():
    from litprinter import print as litprint_print

    assert litprint_print.__func__ is ic.print.__func__


@pytest.mark.parametrize(
    'tag',
    [
        'on_gray',
        'on_grey',
        'bright_gray',
        'bright_grey',
        'on_red',
        'on_bright_red',
        'bright_red',
        'gray',
        'grey',
    ],
)
def test_every_documented_color_tag_resolves(tag):
    """Regression: these tags used to raise KeyError inside _codes_for()."""
    out = render_markup(f'[{tag}]x[/]', color=True)
    assert '\033[' in out
    assert 'x' in out


def test_unknown_tag_is_left_alone():
    assert render_markup('[on_purple]x[/]', color=True) == '[on_purple]x[/]'


def test_unclosed_tag_resets():
    out = render_markup('[bold]x', color=True)
    assert out.endswith('\033[0m')


def test_empty_tag_is_noop():
    assert render_markup('[]x', color=True) == '[]x'
