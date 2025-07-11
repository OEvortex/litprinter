"""
>>> from litprinter import litprint
>>> from litprinter import lit
>>> from litprinter import install, uninstall
>>>
>>> litprint("Hello, world!")
LIT -> [__main__.py:1] in () >>> Hello, world!
>>>
>>> def my_function():
...    lit(1, 2, 3)
>>> my_function()
LIT -> [__main__.py:4] in my_function() >>> 1, 2, 3
>>> install()
>>> ic("This is now the builtins.ic()")
LIT -> [__main__.py:7] in () >>> This is now the builtins.ic()
>>> uninstall()

This module provides enhanced print and logging functionalities for Python,
allowing developers to debug their code with style and precision. It
includes the litprint and lit functions for debugging, log for logging, and
install/uninstall functions for integration into the builtins module.
It also handles colorizing output and provides different styles and customizable
options.

LITPRINTER is inspired by the icecream package and provides similar functionality
with additional features:
- Variable inspection with expression display
- Return value handling for inline usage
- Support for custom formatters for specific data types
- Execution context tracking
- Rich-like colorized output with multiple themes (JARVIS, RICH, MODERN, NEON, CYBERPUNK)
- Better JSON formatting with indent=2 by default
- Advanced pretty printing for complex data structures with smart truncation
- Clickable file paths in supported terminals and editors (VSCode compatible)
- Enhanced visual formatting with better spacing and separators
- Special formatters for common types (Exception, bytes, set, frozenset, etc.)
- Smart object introspection for custom classes
- Logging capabilities with timestamp and log levels
"""
from .litprint import litprint
from .lit import lit
from .core import LitPrintDebugger, argumentToString
from .builtins import install, uninstall
from .coloring import SolarizedDark
# from . import traceback  # Removed complex traceback module
# from .console import *  # Removed complex console module
# Panel functionality removed - not part of icecream-like interface
# try:
#     from .panel import (
#         Panel, BorderStyle, Padding, Shadow, Background, TextOverflow,
#         BorderChars, RenderableType, Segment, BoxModel, PanelGroup,
#         panel, info_panel, warning_panel, error_panel, success_panel,
#         debug_panel, quote_panel, code_panel, highlight_panel, shadow_panel,
#         themed_panel, PANEL_THEMES
#     )
# except ImportError:
#     # Panel module may not be available in all environments
#     pass

__version__ = '0.2.0'

# For compatibility with icecream
enable = LitPrintDebugger.enable if hasattr(LitPrintDebugger, 'enable') else None
disable = LitPrintDebugger.disable if hasattr(LitPrintDebugger, 'disable') else None
