#!/usr/bin/env python3
"""
LitPrinter - The Debug Printer That Replaces print(), logging and icecream

A single, opinionated tool for terminal output:

- ``ic(...)``          - debug print with automatic source expressions, and
                          the single entry point for logging via ``level=``
- ``ic.print(...)``    - drop-in replacement for ``print()`` with markup
- ``traceback``        - syntax highlighted tracebacks, installed for you

Everything is available as a builtin after ``pip install litprinter``:

    x = 42
    ic(x)                                   # ic| x: 42
    ic.print("[bold green]done[/]")          # done
    ic("server ready", level="info")        # INFO  [app.py:12] 'server ready'

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
"""

# ============================================================================
# Debug Printing / Printing / Logging
# ============================================================================

from .litprint import (
    ic,  # Main debug printer (also the logging entry point)
    LIT,  # Alias
    litprint,  # Alias
    lit,  # Alias
    print,  # Drop-in replacement for builtin print()
    configureOutput,
    enable,
    disable,
    format,
    argumentToString,
    IceCreamDebugger,
)

# Legacy alias
from .core import LITPrintDebugger

from .builtins import DEFAULT_NAMES, install, uninstall

from .markup import render_markup, strip_markup, supports_color

# ============================================================================
# Theme
# ============================================================================

from .theme import LitPrinterStyle
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

__version__ = '0.6.0'


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
    # Configuration
    'configureOutput',
    'enable',
    'disable',
    'format',
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
    # Theme
    'LitPrinterStyle',
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
