#!/usr/bin/env python3
"""
LitPrinter Colors

ANSI escape sequences used by :mod:`litprinter.markup` and the traceback
renderer, plus small helpers for building and stripping them.

Only what the package actually needs lives here. ``litprinter.print`` exposes
named colors (``[red]``, ``[bright_red]``, ``[on_blue]``, ...) plus ``#hex``
and ``rgb(r,g,b)`` values, all of which resolve to the codes below.
"""

import re

__all__ = ['Colors']


class Colors:
    """ANSI escape sequences and helpers for terminal styling."""

    # Standard 8 colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

    # Bright (high intensity) colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Bright background colors
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    STRIKE = '\033[9m'

    RESET = '\033[0m'

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Build a 24-bit true-color escape sequence."""
        red, green, blue = (max(0, min(255, v)) for v in (r, g, b))
        return f'\033[38;2;{red};{green};{blue}m'

    @staticmethod
    def from_hex(hex_color: str) -> str:
        """Build a true-color escape sequence from ``#rgb`` or ``#rrggbb``."""
        value = hex_color.lstrip('#')
        if len(value) == 3:
            value = ''.join(c * 2 for c in value)
        if len(value) != 6:
            raise ValueError(f'Invalid hex color: {hex_color}')
        try:
            r, g, b = (int(value[i : i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            raise ValueError(f'Invalid hex color: {hex_color}') from None
        return Colors.rgb(r, g, b)

    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove every ANSI escape sequence from ``text``."""
        return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)
