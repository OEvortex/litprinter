#!/usr/bin/env python3
"""
LitPrinter Renderer

Turns a structured debug record into a styled terminal line.

``ic()`` builds a record (prefix, context, ``[(expr, value), ...]``) and this
module renders it the way a modern terminal UI would:

- the prefix and file/line context are dimmed so they recede
- variable names get their own colour, values are syntax highlighted
- multi-line values hang off the first line instead of restarting at column 0

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
"""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from .colors import Colors

__all__ = ['render_record', 'align_continuations', 'visible_width']

#: Continuation lines are offset by this much under the first value column.
CONTINUATION_INDENT = '  '


def visible_width(text: str) -> int:
    """Length of ``text`` ignoring ANSI escape sequences."""
    return len(Colors.strip_ansi(text))


def align_continuations(text: str, width: int) -> str:
    """Indent every line after the first so it hangs under column ``width``.

    Blank lines stay blank instead of collecting trailing whitespace.
    """
    if '\n' not in text:
        return text

    lines = text.split('\n')
    pad = ' ' * width + CONTINUATION_INDENT
    return '\n'.join(
        [lines[0]] + [(pad + line if line.strip() else '') for line in lines[1:]]
    )


def _paint(text: str, code: str, color: bool) -> str:
    """Wrap ``text`` in an ANSI code when color is enabled."""
    if not color or not text:
        return text
    return f'{code}{text}{Colors.RESET}'


def render_record(
    prefix: str,
    context: str,
    pairs: List[Tuple[Optional[str], str]],
    *,
    color: bool = True,
    highlight: Optional[Callable[[str], str]] = None,
    delimiter: str = ', ',
    context_arrow: bool = True,
) -> str:
    """Render one ``ic()`` line.

    Args:
        prefix: Leading marker, e.g. ``"ic| "``.
        context: Formatted ``file:line`` context, or ``''`` to omit it.
        pairs: ``(expression, value_text)`` pairs. A ``None`` expression means
            the value stands alone (literals, f-strings).
        color: Whether to emit ANSI colors.
        highlight: Callable that syntax highlights a value string. Defaults to
            :func:`litprinter.core._colorize`.
        delimiter: Separator placed between the rendered pairs.
        context_arrow: Whether the context is followed by ``>>>``. Leveled
            output reads as a log line and drops the arrow.

    Returns:
        The rendered line, spanning multiple lines when a value is multi-line.
    """
    if highlight is None:
        from .core import _colorize

        highlight = _colorize

    name_color = Colors.BRIGHT_CYAN
    dim = Colors.GRAY

    head = _paint(prefix, dim, color)
    if context:
        head += _paint(f'[{context}] ', dim, color)
        if context_arrow:
            head += _paint('>>> ', dim, color)

    chunks: List[str] = []
    for expr, value in pairs:
        shown = highlight(value) if color else value
        if expr:
            shown = _paint(expr, name_color, color) + _paint(': ', dim, color) + shown
        chunks.append(shown)

    body = delimiter.join(chunks)
    return head + align_continuations(body, visible_width(head))
