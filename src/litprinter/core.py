#!/usr/bin/env python3
"""
LitPrinter Core Module

This module provides the IceCreamDebugger class - a powerful debugging utility
that combines the simplicity of IceCream with Rich-style formatting.

Features:
- Variable inspection with expression display
- Configurable output formatting
- Enable/disable debugging output
- Rich-style colorized output
- Context information (file, line, function)

Usage:
    from litprinter import ic
    
    x = 42
    ic(x)  # Output: ic| x: 42
    
    ic.configureOutput(prefix='DEBUG| ', includeContext=True)
    ic()   # Output: DEBUG| script.py:10 in my_function()

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

from __future__ import print_function
from datetime import datetime
from contextlib import contextmanager
from os.path import basename, realpath
from textwrap import dedent
import ast
import inspect
import pprint
import sys
import warnings
import functools
import json
from typing import Any, List, Type, Optional, Dict, Callable, Union

# Optional imports
try:
    import colorama
    HAS_COLORAMA = True
except ImportError:
    colorama = None
    HAS_COLORAMA = False

try:
    import executing
except ImportError as exc:
    raise ImportError(
        "The 'executing' package is required for litprinter. "
        "Install it with: pip install executing"
    ) from exc

try:
    from pygments import highlight
    from pygments.formatters import Terminal256Formatter
    from pygments.lexers import Python3Lexer
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False
    highlight = None
    Terminal256Formatter = None
    Python3Lexer = None

try:
    from .coloring import CyberpunkStyle
except ImportError:
    CyberpunkStyle = None

# Sentinel for absent values
_ABSENT = object()

# Default configuration
DEFAULT_PREFIX = 'ic| '
DEFAULT_OUTPUT_FUNCTION = lambda s: print(s, file=sys.stderr)
DEFAULT_ARG_TO_STRING_FUNCTION = pprint.pformat
DEFAULT_CONTEXT_DELIMITER = ' - '
DEFAULT_LINE_WRAP_WIDTH = 70

NO_SOURCE_WARNING = (
    "Failed to access source code for analysis. "
    "Was ic() called in a REPL or frozen application?"
)


# ============================================================================
# Colorization Utilities
# ============================================================================

# Current style (can be changed)
_current_style = None

def set_style(style):
    """Set the syntax highlighting style.
    
    Args:
        style: A Pygments Style class (e.g., SolarizedDark, LitStyle, CyberpunkStyle)
    """
    global _current_style
    _current_style = style


def get_style():
    """Get the current syntax highlighting style."""
    global _current_style
    if _current_style is None:
        try:
            from .coloring import DEFAULT_STYLE
            _current_style = DEFAULT_STYLE
        except ImportError:
            _current_style = None
    return _current_style


@contextmanager
def _windows_color_support():
    """Enable color support on Windows terminals."""
    if HAS_COLORAMA:
        colorama.init()
        try:
            yield
        finally:
            colorama.deinit()
    else:
        yield


def _create_formatter():
    """Create a Pygments formatter with the current style."""
    if not HAS_PYGMENTS:
        return None
    
    style = get_style()
    if style:
        return Terminal256Formatter(style=style)
    return Terminal256Formatter()


def _colorize(text: str) -> str:
    """Apply syntax highlighting to text."""
    if not HAS_PYGMENTS:
        return text
    
    try:
        formatter = _create_formatter()
        lexer = Python3Lexer(ensurenl=False)
        return highlight(text, lexer, formatter).rstrip()
    except Exception:
        return text


def _colorized_stderr_print(text: str) -> None:
    """Print colorized text to stderr."""
    colored = _colorize(text)
    with _windows_color_support():
        print(colored, file=sys.stderr)


# ============================================================================
# Source Code Analysis
# ============================================================================

class Source(executing.Source):
    """Extended Source class for extracting expression text."""
    
    def get_text_with_indentation(self, node) -> str:
        """Get the source text of a node, handling indentation."""
        result = self.asttokens().get_text(node)
        if '\n' in result:
            result = ' ' * node.first_token.start[1] + result
            result = dedent(result)
        return result.strip()


def _is_literal(s: str) -> bool:
    """Check if a string represents a Python literal."""
    try:
        ast.literal_eval(s)
        return True
    except Exception:
        return False


# ============================================================================
# Argument Formatting
# ============================================================================

@functools.singledispatch
def argumentToString(obj: Any) -> str:
    """Convert an argument to a string representation.
    
    This function uses singledispatch to allow registering custom
    formatters for different types.
    
    Args:
        obj: The object to format.
        
    Returns:
        String representation of the object.
    """
    s = DEFAULT_ARG_TO_STRING_FUNCTION(obj)
    return s.replace('\\n', '\n')


@argumentToString.register(str)
def _format_str(obj: str) -> str:
    """Format string objects."""
    if '\n' in obj:
        return "'''" + obj + "'''"
    return repr(obj)


@argumentToString.register(type)
def _format_type(obj: type) -> str:
    """Format type objects."""
    module = obj.__module__
    name = obj.__name__
    if module == 'builtins':
        return f"<class '{name}'>"
    return f"<class '{module}.{name}'>"


@argumentToString.register(Exception)
def _format_exception(obj: Exception) -> str:
    """Format exception objects."""
    return f"<{obj.__class__.__name__}: {str(obj)}>"


@argumentToString.register(bytes)
def _format_bytes(obj: bytes) -> str:
    """Format bytes objects."""
    if len(obj) > 50:
        return f"<bytes len={len(obj)}>"
    try:
        return repr(obj)
    except Exception:
        return f"<bytes len={len(obj)}>"


@argumentToString.register(dict)
def _format_dict(obj: dict) -> str:
    """Format dictionary objects."""
    if len(obj) > 50:
        return f"<dict with {len(obj)} items>"
    
    if not obj:
        return "{}"
    
    # Small dicts with simple values on one line
    if len(obj) <= 3:
        simple = all(
            isinstance(k, (str, int, float, bool)) and
            isinstance(v, (str, int, float, bool, type(None)))
            for k, v in obj.items()
        )
        if simple:
            items = [f"{k!r}: {v!r}" for k, v in obj.items()]
            return "{" + ", ".join(items) + "}"
    
    # Larger dicts with indentation
    lines = []
    for k, v in obj.items():
        formatted_val = argumentToString(v)
        if '\n' in formatted_val:
            indented = formatted_val.replace('\n', '\n    ')
            lines.append(f"  {k!r}: {indented}")
        else:
            lines.append(f"  {k!r}: {formatted_val}")
    
    return "{\n" + ",\n".join(lines) + "\n}"


@argumentToString.register(list)
def _format_list(obj: list) -> str:
    """Format list objects."""
    if len(obj) > 50:
        return f"<list with {len(obj)} items>"
    
    if not obj:
        return "[]"
    
    # Small lists with simple values on one line
    if len(obj) <= 5:
        simple = all(isinstance(x, (str, int, float, bool, type(None))) for x in obj)
        if simple:
            return repr(obj)
    
    # Larger lists with indentation
    items = [argumentToString(x) for x in obj]
    if all('\n' not in item for item in items):
        joined = ", ".join(items)
        if len(joined) < 60:
            return "[" + joined + "]"
    
    formatted = ",\n  ".join(items)
    return "[\n  " + formatted + "\n]"


@argumentToString.register(tuple)
def _format_tuple(obj: tuple) -> str:
    """Format tuple objects."""
    if len(obj) > 50:
        return f"<tuple with {len(obj)} items>"
    
    if not obj:
        return "()"
    
    if len(obj) == 1:
        return f"({argumentToString(obj[0])},)"
    
    # Small tuples with simple values on one line
    if len(obj) <= 5:
        simple = all(isinstance(x, (str, int, float, bool, type(None))) for x in obj)
        if simple:
            return repr(obj)
    
    items = [argumentToString(x) for x in obj]
    if all('\n' not in item for item in items):
        joined = ", ".join(items)
        if len(joined) < 60:
            return "(" + joined + ")"
    
    formatted = ",\n  ".join(items)
    return "(\n  " + formatted + "\n)"


@argumentToString.register(set)
@argumentToString.register(frozenset)
def _format_set(obj: Union[set, frozenset]) -> str:
    """Format set and frozenset objects."""
    if len(obj) > 20:
        return f"<{type(obj).__name__} with {len(obj)} items>"
    
    if not obj:
        return "set()" if isinstance(obj, set) else "frozenset()"
    
    try:
        sorted_items = sorted(obj, key=str)
        items = [argumentToString(x) for x in sorted_items]
        
        if len(obj) <= 5:
            return "{" + ", ".join(items) + "}"
        
        return "{\n  " + ",\n  ".join(items) + "\n}"
    except Exception:
        return f"<{type(obj).__name__} with {len(obj)} items>"


# ============================================================================
# IceCream Debugger Class
# ============================================================================

class IceCreamDebugger:
    """IceCream-compatible debugging class with Rich-style output.
    
    This class provides the core debugging functionality with support for:
    - Variable inspection with expression display
    - Configurable output (prefix, output function, formatting)
    - Enable/disable toggle
    - Context information (file, line, function)
    
    Example:
        >>> ic = IceCreamDebugger()
        >>> x = 42
        >>> ic(x)
        ic| x: 42
        
        >>> ic.configureOutput(prefix='DEBUG| ')
        >>> ic(x)
        DEBUG| x: 42
    """
    
    _pair_delimiter = ', '
    
    def __init__(
        self,
        prefix: Union[str, Callable[[], str]] = DEFAULT_PREFIX,
        outputFunction: Callable[[str], None] = _colorized_stderr_print,
        argToStringFunction: Callable[[Any], str] = argumentToString,
        includeContext: bool = False,
        contextAbsPath: bool = False,
    ):
        """Initialize the IceCream debugger.
        
        Args:
            prefix: Prefix string or callable returning prefix.
            outputFunction: Function to output formatted text.
            argToStringFunction: Function to convert args to strings.
            includeContext: Whether to include file/line/function context.
            contextAbsPath: Whether to use absolute paths in context.
        """
        self._enabled = True
        self._prefix = prefix
        self._outputFunction = outputFunction
        self._argToStringFunction = argToStringFunction
        self._includeContext = includeContext
        self._contextAbsPath = contextAbsPath
    
    @property
    def enabled(self) -> bool:
        """Check if debugging output is enabled."""
        return self._enabled
    
    def enable(self) -> None:
        """Enable debugging output."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable debugging output."""
        self._enabled = False
    
    def configureOutput(
        self,
        prefix: Union[str, Callable[[], str], None] = None,
        outputFunction: Optional[Callable[[str], None]] = None,
        argToStringFunction: Optional[Callable[[Any], str]] = None,
        includeContext: Optional[bool] = None,
        contextAbsPath: Optional[bool] = None,
    ) -> None:
        """Configure output settings.
        
        Args:
            prefix: New prefix string or callable.
            outputFunction: New output function.
            argToStringFunction: New argument formatting function.
            includeContext: Whether to include context.
            contextAbsPath: Whether to use absolute paths.
            
        Raises:
            TypeError: If no arguments are provided.
        """
        if all(arg is None for arg in [prefix, outputFunction, argToStringFunction, 
                                        includeContext, contextAbsPath]):
            raise TypeError("configureOutput() requires at least one argument")
        
        if prefix is not None:
            self._prefix = prefix
        if outputFunction is not None:
            self._outputFunction = outputFunction
        if argToStringFunction is not None:
            self._argToStringFunction = argToStringFunction
        if includeContext is not None:
            self._includeContext = includeContext
        if contextAbsPath is not None:
            self._contextAbsPath = contextAbsPath
    
    def __call__(self, *args) -> Any:
        """Debug print the arguments and return them.
        
        Args:
            *args: Values to debug print.
            
        Returns:
            None if no args, single arg if one arg, tuple if multiple.
        """
        if self._enabled:
            call_frame = inspect.currentframe().f_back
            output = self._format(call_frame, *args)
            self._outputFunction(output)
        
        # Return passthrough
        if not args:
            return None
        elif len(args) == 1:
            return args[0]
        else:
            return args
    
    def format(self, *args) -> str:
        """Format arguments without printing.
        
        Args:
            *args: Values to format.
            
        Returns:
            Formatted string.
        """
        call_frame = inspect.currentframe().f_back
        return self._format(call_frame, *args)
    
    def _format(self, call_frame, *args) -> str:
        """Internal formatting method.
        
        Args:
            call_frame: The calling frame.
            *args: Values to format.
            
        Returns:
            Formatted string.
        """
        prefix = self._get_prefix()
        context = self._format_context(call_frame) if self._includeContext else ''
        
        if not args:
            # No args - just show context or time
            time_str = self._format_time()
            if context:
                return f"{prefix}{context}{time_str}"
            return f"{prefix}{time_str}"
        
        # Format the arguments
        return self._format_args(call_frame, prefix, context, args)
    
    def _get_prefix(self) -> str:
        """Get the current prefix string."""
        if callable(self._prefix):
            return self._prefix()
        return self._prefix
    
    def _format_context(self, call_frame) -> str:
        """Format the call context (file:line in function)."""
        frame_info = inspect.getframeinfo(call_frame)
        
        if self._contextAbsPath:
            filename = realpath(frame_info.filename)
        else:
            filename = basename(frame_info.filename)
        
        lineno = frame_info.lineno
        func_name = frame_info.function
        
        if func_name != '<module>':
            func_name = f'{func_name}()'
        
        return f"{filename}:{lineno} in {func_name}"
    
    def _format_time(self) -> str:
        """Format current time."""
        now = datetime.now()
        return now.strftime('%H:%M:%S.%f')[:-3]
    
    def _format_args(self, call_frame, prefix: str, context: str, args: tuple) -> str:
        """Format the argument values with their expressions.
        
        Args:
            call_frame: The calling frame.
            prefix: Output prefix.
            context: Context string.
            args: Argument values.
            
        Returns:
            Formatted string.
        """
        # Get the source expressions for arguments
        call_node = Source.executing(call_frame).node
        
        if call_node is not None:
            source = Source.for_frame(call_frame)
            arg_strs = [
                source.get_text_with_indentation(arg)
                for arg in call_node.args
            ]
        else:
            warnings.warn(NO_SOURCE_WARNING, RuntimeWarning, stacklevel=4)
            arg_strs = [_ABSENT] * len(args)
        
        # Build pairs of (expression, value)
        pairs = list(zip(arg_strs, args))
        
        # Format each pair
        formatted_pairs = []
        for expr, val in pairs:
            val_str = self._argToStringFunction(val)
            
            if expr is _ABSENT or _is_literal(expr):
                # Just the value
                formatted_pairs.append(val_str)
            else:
                # Expression: value
                formatted_pairs.append(f"{expr}: {val_str}")
        
        # Join pairs
        args_str = self._pair_delimiter.join(formatted_pairs)
        
        # Build the output
        if context:
            return f"{prefix}[{context}] >>> {args_str}"
        else:
            return f"{prefix}{args_str}"
    
    def __repr__(self) -> str:
        return f"<IceCreamDebugger prefix={self._prefix!r} enabled={self._enabled}>"


# ============================================================================
# Legacy Compatibility - LITPrintDebugger alias
# ============================================================================

# Alias for backward compatibility
LITPrintDebugger = IceCreamDebugger


# ============================================================================
# Module-level Utilities
# ============================================================================

def clearStyleCache() -> None:
    """Clear the style formatter cache (placeholder for compatibility)."""
    pass


def getStyleCacheInfo() -> Dict[str, Any]:
    """Get style cache information."""
    return {"cache_size": 0, "cached_styles": []}


def isTerminalCapable() -> bool:
    """Check if the terminal supports colors."""
    import os
    
    # Respect NO_COLOR environment variable
    if os.environ.get('NO_COLOR'):
        return False
    
    # Check if stdout is a TTY
    try:
        return sys.stderr.isatty()
    except Exception:
        return False
