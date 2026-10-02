"""Tests for ic.print, ic(..., level=) and markup rendering."""

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


def test_level_tags_the_line(out):
    ic('hello', level='info')
    assert out[-1].startswith('INFO')
    assert "'hello'" in out[-1]


@pytest.mark.parametrize(
    ('level', 'tag'),
    [
        ('debug', 'DEBUG'),
        ('info', 'INFO'),
        ('success', 'OK'),
        ('ok', 'OK'),
        ('warning', 'WARN'),
        ('warn', 'WARN'),
        ('error', 'ERROR'),
        ('critical', 'CRIT'),
    ],
)
def test_every_level_renders_its_tag(level, tag, out):
    ic('msg', level=level)
    assert out[-1].split()[0] == tag


def test_level_replaces_the_ic_prefix(out):
    ic('msg')
    assert out[-1].startswith('ic| ')
    ic('msg', level='error')
    assert not out[-1].startswith('ic| ')


def test_level_drops_the_context_arrow(out):
    items = [1, 2, 3]
    ic(items[0], level='warning')
    assert '>>>' not in out[-1]
    ic(items[0])
    assert '>>>' in out[-1]


def test_level_shows_context_when_needed(out):
    ic(len([1, 2, 3]), level='error')
    assert '[test_print_log.py' in out[-1]


def test_level_is_colored_when_enabled():
    from litprinter.core import render_level_prefix

    colored = render_level_prefix('error', color=True)
    assert '\033[31m' in colored
    assert render_level_prefix('error', color=False) == 'ERROR  '
    assert 'ERROR' in ic.format('boom', level='error')


def test_level_without_args_is_a_breadcrumb(out):
    ic(level='info')
    assert out[-1].startswith('INFO')


def test_fields_are_named_pairs(out):
    ic('cache miss', key='session:9f2', level='debug')
    assert out[-1].endswith("'cache miss', key: 'session:9f2'")


def test_fields_work_without_a_level(out):
    ic('cache miss', key='session:9f2')
    assert out[-1] == "ic| 'cache miss', key: 'session:9f2'"


def test_fields_only_no_positional(out):
    ic(attempt=2, level='info')
    assert out[-1].endswith('attempt: 2')


def test_fields_follow_positional_pairs(out):
    x = 1
    ic(x, extra='v')
    assert out[-1] == "ic| x: 1, extra: 'v'"


def test_fields_use_the_custom_formatter(out):
    from litprinter import argumentToString

    class Thing:
        pass

    before = argumentToString.dispatch(Thing)
    argumentToString.register(Thing, lambda self: '<thing>')
    try:
        ic('obj', t=Thing())
        assert 't: <thing>' in out[-1]
    finally:
        argumentToString.register(Thing, before)


def test_fields_respect_the_pair_delimiter(out):
    ic.configureOutput(pairDelimiter=' | ')
    try:
        ic('msg', a=1, b=2)
        assert out[-1] == "ic| 'msg' | a: 1 | b: 2"
    finally:
        ic.configureOutput(pairDelimiter=', ')


def test_reserved_keywords_are_not_fields(out):
    x = 1
    ic(x, includeContext=True, contextAbsPath=False, level='info')
    line = out[-1]
    assert 'includeContext' not in line
    assert 'contextAbsPath' not in line
    assert line.startswith('INFO')


def test_fields_are_auto_aligned(out):
    ic('cfg', host='0.0.0.0', port=8080, level='info')
    assert '\n' not in out[-1] or all(
        line.startswith(' ') for line in out[-1].split('\n')[1:]
    )


def test_fields_do_not_change_the_return_value(out):
    """Fields are context, not the value: ic(calc(), step=i) still returns calc()."""
    x = 5
    assert ic(x, tag='t') == 5
    assert ic(x, y=2) == 5
    assert ic(x, 2, y=3) == (x, 2)
    assert ic(tag='t') is None


def test_format_accepts_fields():
    assert ic.format('msg', a=1, level='error').endswith("'msg', a: 1")


def test_level_unknown_raises(out):
    with pytest.raises(ValueError, match='Unknown level'):
        ic('x', level='nope')
    # A bad level must not corrupt the debugger's state.
    ic('still works')


def test_level_respects_disable(out):
    ic.disable()
    try:
        ic('hidden', level='error')
        assert out == []
    finally:
        ic.enable()


def test_level_passes_values_through(out):
    assert ic(7, level='debug') == 7
    assert ic(1, 2, level='info') == (1, 2)
    assert ic(level='info') is None


def test_format_honors_level():
    assert ic.format('x', level='error').startswith('ERROR')


def test_level_methods_are_gone():
    for name in (
        'log',
        'debug',
        'info',
        'success',
        'warning',
        'warn',
        'error',
        'critical',
    ):
        assert not hasattr(ic, name), name
    import litprinter

    assert not hasattr(litprinter, 'log')


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
