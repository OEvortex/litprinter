#!/usr/bin/env python3
"""
LitPrinter - The Debug Printer That Replaces print(), logging and icecream

A single, opinionated tool for terminal output:

- ``ic(...)``        - debug print with automatic source expressions
- ``ic.print(...)``  - drop-in replacement for ``print()`` with markup
- ``ic.info(...)``   - logging without importing ``logging``
- ``traceback``      - syntax highlighted tracebacks

Everything is available as a builtin after ``pip install litprinter``:

    x = 42
    ic(x)                                  # ic| x: 42
    ic.print("[bold green]done[/]")         # done
    ic.info("server ready")                 # INFO  server ready

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
"""

# ============================================================================
# Debug Printing / Printing / Logging
# ============================================================================

from .litprint import (
    ic,  # Main debug printer
    LIT,  # Alias
    litprint,  # Alias
    lit,  # Alias
    print,  # Drop-in replacement for builtin print()
    log,  # Logging-style output
    configureOutput,
    enable,
    disable,
    format,
    set_style,
    get_style,
    argumentToString,
    IceCreamDebugger,
)

# Legacy alias
from .core import LITPrintDebugger

from .builtins import DEFAULT_NAMES, install, uninstall

from .markup import render_markup, strip_markup, supports_color

# ============================================================================
# Themes (used by ic output and tracebacks)
# ============================================================================

from .coloring import (
    TokyoNight,
    LitStyle,
    SolarizedDark,
    CyberpunkStyle,
    MonokaiStyle,
    DEFAULT_STYLE,
)
from .colors import Colors

# ============================================================================
# Traceback Formatting
# ============================================================================

from . import traceback
from .traceback import (
    PrettyTraceback,
    Traceback,
    install as install_traceback,
    uninstall as uninstall_traceback,
)

# ============================================================================
# Builtins Installation
# ============================================================================

# Auto-register ic in builtins on import, so `ic` works in every script after
# `pip install litprinter` without an explicit import. setattr() is used
# because static type checkers model builtins from typeshed, not from runtime.
import builtins as _builtins

for _name, _value in (
    ('ic', ic),
    ('LIT', LIT),
    ('litprint', litprint),
    ('lit', lit),
):
    setattr(_builtins, _name, _value)

# ============================================================================
# Version
# ============================================================================

__version__ = '0.4.0'


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    # Main IceCream-compatible API
    'ic',
    'LIT',
    'litprint',
    'lit',
    # Printing
    'print',
    'log',
    # Configuration
    'configureOutput',
    'enable',
    'disable',
    'format',
    'set_style',
    'get_style',
    'argumentToString',
    'IceCreamDebugger',
    'LITPrintDebugger',
    # Builtins
    'install',
    'uninstall',
    'DEFAULT_NAMES',
    # Markup
    'render_markup',
    'strip_markup',
    'supports_color',
    # Themes
    'TokyoNight',
    'SolarizedDark',
    'LitStyle',
    'CyberpunkStyle',
    'MonokaiStyle',
    'DEFAULT_STYLE',
    'Colors',
    # Traceback
    'traceback',
    'PrettyTraceback',
    'Traceback',
    'install_traceback',
    'uninstall_traceback',
    # Version
    '__version__',
]
