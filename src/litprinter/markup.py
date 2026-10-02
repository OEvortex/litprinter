#!/usr/bin/env python3
"""
LitPrinter Markup

A tiny, dependency-free renderer for Rich-like inline markup used by
``ic.print()``.

Supported tags::

    [bold]text[/bold]        styles:  bold, dim, italic, underline, strike,
                                      reverse, blink
    [red]text[/red]          colors:  black red green yellow blue magenta
                                      cyan white
    [bright_red]...[/]       bright_* colors
    [on_blue]...[/]          on_<color> backgrounds
    [/]                      close the most recently opened tag

Anything that is not a recognized tag is printed verbatim, so this is safe
for arbitrary text (log lines, user data, JSON, ...).
"""

from __future__ import annotations

import os
import re
import sys
from typing import IO, Optional

from .colors import Colors

__all__ = ['render_markup', 'strip_markup', 'supports_color', 'render']


_TAG_RE = re.compile(r"\[(/)?([a-zA-Z0-9_#,\.\(\)\s]*)\]")

_STYLE_TAGS = {
    'bold': Colors.BOLD,
    'dim': Colors.DIM,
    'italic': Colors.ITALIC,
    'underline': Colors.UNDERLINE,
    'strike': Colors.STRIKE,
    'reverse': Colors.REVERSE,
    'blink': Colors.BLINK,
}

_COLOR_TAGS = {
    'black': Colors.BLACK,
    'red': Colors.RED,
    'green': Colors.GREEN,
    'yellow': Colors.YELLOW,
    'blue': Colors.BLUE,
    'magenta': Colors.MAGENTA,
    'cyan': Colors.CYAN,
    'white': Colors.WHITE,
    'gray': Colors.GRAY,
    'grey': Colors.GRAY,
    'bright_black': Colors.BRIGHT_BLACK,
    'bright_red': Colors.BRIGHT_RED,
    'bright_green': Colors.BRIGHT_GREEN,
    'bright_yellow': Colors.BRIGHT_YELLOW,
    'bright_blue': Colors.BRIGHT_BLUE,
    'bright_magenta': Colors.BRIGHT_MAGENTA,
    'bright_cyan': Colors.BRIGHT_CYAN,
    'bright_white': Colors.BRIGHT_WHITE,
}

_BACKGROUND_TAGS = {
    'on_black': Colors.BG_BLACK,
    'on_red': Colors.BG_RED,
    'on_green': Colors.BG_GREEN,
    'on_yellow': Colors.BG_YELLOW,
    'on_blue': Colors.BG_BLUE,
    'on_magenta': Colors.BG_MAGENTA,
    'on_cyan': Colors.BG_CYAN,
    'on_white': Colors.BG_WHITE,
    'on_bright_black': Colors.BG_BRIGHT_BLACK,
    'on_bright_red': Colors.BG_BRIGHT_RED,
    'on_bright_green': Colors.BG_BRIGHT_GREEN,
    'on_bright_yellow': Colors.BG_BRIGHT_YELLOW,
    'on_bright_blue': Colors.BG_BRIGHT_BLUE,
    'on_bright_magenta': Colors.BG_BRIGHT_MAGENTA,
    'on_bright_cyan': Colors.BG_BRIGHT_CYAN,
    'on_bright_white': Colors.BG_BRIGHT_WHITE,
}

_TAGS = {**_STYLE_TAGS, **_COLOR_TAGS, **_BACKGROUND_TAGS}


def supports_color(stream: Optional[IO[str]] = None) -> bool:
    """Return True when ANSI colors should be emitted for ``stream``."""
    if os.environ.get('NO_COLOR'):
        return False
    force = os.environ.get('FORCE_COLOR')
    if force and force != '0':
        return True
    if os.environ.get('TERM') == 'dumb':
        return False
    stream = stream or sys.stdout
    try:
        return bool(stream.isatty())
    except Exception:
        return False


_RGB_RE = re.compile(r"^rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$")


def _codes_for(tokens: str) -> list:
    """Translate a tag body into ANSI codes (unknown tokens are ignored)."""
    tokens = tokens.strip()
    rgb = _RGB_RE.match(tokens)
    if rgb:
        return [Colors.rgb(*(int(g) for g in rgb.groups()))]

    codes = []
    for token in tokens.replace(',', ' ').split():
        key = token.strip().lower()
        if not key:
            continue
        if key in _TAGS:
            codes.append(_TAGS[key])
        elif key.startswith('on_') and key[3:] in _COLOR_TAGS:
            codes.append(_BACKGROUND_TAGS['on_' + key[3:]])
        elif key.startswith('bright_') and key[7:] in _COLOR_TAGS:
            codes.append(_COLOR_TAGS[key])
        else:
            code = _color_value(key)
            if code:
                codes.append(code)
    return codes


def _color_value(token: str) -> Optional[str]:
    """Support ``#ff0000`` and ``rgb(255,0,0)`` color values."""
    if token.startswith('#'):
        try:
            return Colors.from_hex(token)
        except ValueError:
            return None
    if token.startswith('rgb(') and token.endswith(')'):
        parts = token[4:-1].split(',')
        if len(parts) != 3:
            return None
        try:
            r, g, b = (int(p.strip()) for p in parts)
        except ValueError:
            return None
        return Colors.rgb(r, g, b)
    return None


def render_markup(
    text: str,
    *,
    style: Optional[str] = None,
    color: Optional[bool] = None,
    stream: Optional[IO[str]] = None,
) -> str:
    """Render Rich-like inline markup into ANSI-colored text.

    Args:
        text: Text possibly containing ``[bold]``-style tags.
        style: Optional default style applied to the whole string, e.g.
            ``"bold cyan"`` or ``"#ff8800"``.
        color: Force colors on/off. Defaults to auto-detection.
        stream: Stream used for auto-detection. Defaults to stdout.

    Returns:
        The rendered string. Unrecognized tags are left untouched.
    """
    text = str(text)
    use_color = supports_color(stream) if color is None else color
    if not use_color:
        return strip_markup(text)

    out = []
    stack = []

    def active_codes() -> str:
        if not stack:
            return ''
        return ''.join(code for group in stack for code in group)

    position = 0
    for match in _TAG_RE.finditer(text):
        out.append(active_codes())
        out.append(text[position:match.start()])
        position = match.end()

        closing, body = match.group(1), match.group(2).strip()
        if closing or body in ('/', ''):
            if stack:
                stack.pop()
                out.append(Colors.RESET)
                out.append(active_codes())
            continue

        codes = _codes_for(body)
        if not codes:
            # Unknown tag: keep it verbatim.
            out.append(active_codes())
            out.append(match.group(0))
            continue

        stack.append(codes)
        out.append(''.join(codes))

    out.append(active_codes())
    out.append(text[position:])
    if stack:
        # Unclosed tag: reset so color does not bleed into the terminal.
        out.append(Colors.RESET)

    rendered = ''.join(out)
    if style:
        rendered = ''.join(_codes_for(style)) + rendered + Colors.RESET
    return rendered


def strip_markup(text: str) -> str:
    """Remove recognized markup tags from ``text``."""

    def _replace(match: re.Match) -> str:
        closing, body = match.group(1), match.group(2).strip()
        if closing or body in ('/', ''):
            return ''
        return '' if _codes_for(body) else match.group(0)

    return _TAG_RE.sub(_replace, str(text))


def render(value: object, **kwargs) -> str:
    """``str()`` a value, then render markup inside strings only."""
    if isinstance(value, str):
        return render_markup(value, **kwargs)
    return str(value)
