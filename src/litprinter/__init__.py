#!/usr/bin/env python3
"""
LitPrinter - The Most Sophisticated Debug Printing Library for Python

A comprehensive terminal output library combining IceCream debugging
with Rich-style formatting:

- IceCream-compatible ic() function with configureOutput(), enable/disable
- Styled console output with markup support
- Beautiful bordered panels with multiple styles  
- Pretty tracebacks with syntax highlighting
- Colors, styles, and text formatting utilities

Usage:
    from litprinter import ic
    
    x = 42
    ic(x)  # Output: ic| x: 42
    
    # Configure output
    ic.configureOutput(prefix='DEBUG| ')
    ic.configureOutput(includeContext=True)
    
    # Enable/disable
    ic.disable()
    ic.enable()
    
    # Format without printing  
    s = ic.format(x)
    
    # Rich-style console
    from litprinter import Console, Panel
    console = Console()
    console.print("[bold red]Error:[/bold red] Something went wrong!")
    print(Panel("Hello!", title="Greeting"))

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

# ============================================================================
# IceCream-compatible Debug Printing (Main Feature)
# ============================================================================

from .litprint import (
    ic,           # Main debug function
    LIT,          # Alias
    litprint,     # Alias  
    lit,          # Alias
    configureOutput,  # Configure ic output
    enable,       # Enable ic output
    disable,      # Disable ic output
    format,       # Format without printing
    set_style,    # Set color style
    get_style,    # Get current style
    argumentToString,  # Custom formatters
    IceCreamDebugger,  # Core class
)

# Legacy alias
from .core import LITPrintDebugger

# ============================================================================
# Builtins Installation
# ============================================================================

from .builtins import install, uninstall

# Auto-install ic to builtins when litprinter is imported
# This makes ic() available globally after `pip install litprinter`
_builtins = __import__('builtins')
_builtins.ic = ic
_builtins.LIT = LIT
_builtins.litprint = litprint

# ============================================================================
# Colors and Styling
# ============================================================================

from .coloring import (
    TokyoNight,       # Tokyo Night theme (NEW DEFAULT)
    LitStyle,         # Catppuccin-inspired (brighter)
    SolarizedDark,    # IceCream-compatible
    CyberpunkStyle,   # Neon cyberpunk
    MonokaiStyle,     # Classic Monokai
    DEFAULT_STYLE,    # Current default
)
from .colors import Colors

# ============================================================================
# Rich-style Infrastructure Modules
# ============================================================================

try:
    from .segment import Segment, ControlType, ControlCode, render_segments
except ImportError:
    Segment = None
    ControlType = None
    ControlCode = None
    render_segments = None

try:
    from .style import Style, NULL_STYLE, style, BOLD, DIM, ITALIC, UNDERLINE
except ImportError:
    Style = None
    NULL_STYLE = None

try:
    from .text import Text, Span
except ImportError:
    Text = None
    Span = None

try:
    from .box import (
        Box, ROUNDED, HEAVY, DOUBLE, SQUARE, ASCII, DASHED, DOTTED,
        NONE as BOX_NONE, get_box, render_box
    )
except ImportError:
    Box = None
    ROUNDED = None

# ============================================================================
# Console with Rich-like Features
# ============================================================================

from .console import Console, console, cprint
from .console import print as console_print

# ============================================================================
# Panel Rendering
# ============================================================================

try:
    from .panel import Panel, BorderStyle, Padding, Shadow, Background, PanelGroup, panel
except ImportError:
    Panel = None
    BorderStyle = None

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
# Styles/Themes
# ============================================================================

try:
    from .styles import (
        JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI,
        SOLARIZED, NORD, GITHUB, VSCODE, MATERIAL, RETRO, OCEAN,
        AUTUMN, SYNTHWAVE, FOREST, MONOCHROME, SUNSET,
        create_custom_style,
    )
except ImportError:
    # Styles package not available
    pass

# ============================================================================
# Version
# ============================================================================

__version__ = '0.3.3'

# ============================================================================
# Public API
# ============================================================================

__all__ = [
    # Main IceCream-compatible API
    "ic",
    "LIT", 
    "litprint",
    "lit",
    "configureOutput",
    "enable",
    "disable",
    "format",
    "set_style",
    "get_style",
    "argumentToString",
    "IceCreamDebugger",
    "LITPrintDebugger",
    # Builtins (like IceCream)
    "install",
    "uninstall",
    # Color Styles
    "TokyoNight",
    "SolarizedDark",
    "LitStyle",
    "CyberpunkStyle",
    "MonokaiStyle",
    "DEFAULT_STYLE",
    "Colors",
    # Segment
    "Segment",
    "ControlType",
    "ControlCode",
    "render_segments",
    # Style
    "Style",
    "NULL_STYLE",
    "style",
    "BOLD",
    "DIM",
    "ITALIC",
    "UNDERLINE",
    # Text
    "Text",
    "Span",
    # Box
    "Box",
    "ROUNDED",
    "HEAVY",
    "DOUBLE",
    "SQUARE",
    "ASCII",
    "DASHED",
    "DOTTED",
    "BOX_NONE",
    "get_box",
    "render_box",
    # Console
    "Console",
    "console",
    "cprint",
    "console_print",
    # Panel
    "Panel",
    "BorderStyle",
    "Padding",
    "Shadow",
    "Background",
    "PanelGroup",
    "panel",
    # Traceback
    "traceback",
    "PrettyTraceback",
    "Traceback",
    "install_traceback",
    "uninstall_traceback",
    # Styles
    "JARVIS",
    "RICH",
    "MODERN", 
    "NEON",
    "CYBERPUNK",
    "DRACULA",
    "MONOKAI",
    "SOLARIZED",
    "NORD",
    "GITHUB",
    "VSCODE",
    "MATERIAL",
    "RETRO",
    "OCEAN",
    "AUTUMN",
    "SYNTHWAVE",
    "FOREST",
    "MONOCHROME",
    "SUNSET",
    "create_custom_style",
    # Version
    "__version__",
]
