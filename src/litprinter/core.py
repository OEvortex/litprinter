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

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
"""

from datetime import datetime
from contextlib import contextmanager
from os.path import basename, realpath
from textwrap import dedent
import ast
import inspect
import executing
import os
import pprint
import re
import sys
import warnings
import functools
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.python import Python3Lexer

from .markup import supports_color
from .render import render_record
from typing import Any, Callable, List, Optional, Union

try:
    import colorama
except ImportError:  # pragma: no cover - colorama is a declared dependency
    colorama = None  # ty: ignore[invalid-assignment]

# Sentinel for absent values
_ABSENT = object()

# Expressions that are self-describing enough to not need file/line context.
_SIMPLE_EXPR_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
_FSTRING_PREFIXES = (
    'f"',
    "f'",
    'F"',
    "F'",
    'fr"',
    "fr'",
    'rf"',
    "rf'",
    'Fr"',
    "Fr'",
    'fR"',
    "fR'",
    'FR"',
    "FR'",
    'rF"',
    "rF'",
    'Rf"',
    "Rf'",
    'RF"',
    "RF'",
)

# Default configuration
DEFAULT_PREFIX = 'ic| '
DEFAULT_ARG_TO_STRING_FUNCTION = pprint.pformat
DEFAULT_CONTEXT_DELIMITER = ' - '

NO_SOURCE_WARNING = (
    'Failed to access source code for analysis. '
    'Was ic() called in a REPL or frozen application?'
)


# ============================================================================
# Colorization Utilities
# ============================================================================

# Cached Pygments formatter/lexer for the single built-in theme.
_formatter = None
_lexer = Python3Lexer(ensurenl=False)


def _get_formatter():
    """Return a cached Terminal256 formatter for the built-in theme."""
    global _formatter
    if _formatter is None:
        from .theme import LitPrinterStyle

        _formatter = Terminal256Formatter(style=LitPrinterStyle)
    return _formatter


@contextmanager
def _windows_color_support():
    """Enable ANSI color support on legacy Windows terminals.

    colorama is only needed on Windows. Calling ``init()`` elsewhere wraps
    sys.stdout/sys.stderr and *strips* ANSI codes from non-tty streams, which
    would silently drop all highlighting when output is piped to a file.
    """
    if colorama is None or os.name != 'nt':
        yield
        return

    colorama.init()
    try:
        yield
    finally:
        colorama.deinit()


def _colorize(text: str) -> str:
    """Syntax highlight ``text`` as Python, falling back to plain text."""
    try:
        return highlight(text, _lexer, _get_formatter()).rstrip('\n')
    except Exception:
        return text


def _colorized_stderr_print(text: str) -> None:
    """Print a pre-rendered (possibly colored) line to stderr."""
    with _windows_color_support():
        print(text, file=sys.stderr)


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


def _is_literal(s: object) -> bool:
    """Check if a string represents a Python literal."""
    if not isinstance(s, str):
        return False
    try:
        ast.literal_eval(s)
        return True
    except Exception:
        return False


def _is_fstring(expr: object) -> bool:
    """Check if an expression is an f-string (its value is self-describing)."""
    return isinstance(expr, str) and expr.startswith(_FSTRING_PREFIXES)


def _is_simple_expr(expr: object) -> bool:
    """Check if an expression is a bare name, literal or f-string.

    ``ic(x)`` is self-explanatory, ``ic(x + 1)`` is not.
    """
    if expr is _ABSENT:
        return False
    if not isinstance(expr, str):
        return False
    if _is_fstring(expr) or _is_literal(expr):
        return True
    return bool(_SIMPLE_EXPR_RE.match(expr))


def _needs_context(exprs: List[object], has_args: bool) -> bool:
    """Decide whether file/line context is useful for this call.

    Context is added automatically for calls, attribute access, subscripts,
    operators, comprehensions, and when the source expression is unavailable
    (REPL, frozen apps), because the printed value alone is ambiguous there.
    """
    if not has_args:
        return True
    return not all(_is_simple_expr(expr) for expr in exprs)


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
    return f'<{obj.__class__.__name__}: {str(obj)}>'


@argumentToString.register(bytes)
def _format_bytes(obj: bytes) -> str:
    """Format bytes objects."""
    if len(obj) > 50:
        return f'<bytes len={len(obj)}>'
    return repr(obj)


@argumentToString.register(dict)
def _format_dict(obj: dict) -> str:
    """Format dictionary objects."""
    if len(obj) > 50:
        return f'<dict with {len(obj)} items>'

    if not obj:
        return '{}'

    # Small dicts with simple values on one line
    if len(obj) <= 3:
        simple = all(
            isinstance(k, (str, int, float, bool))
            and isinstance(v, (str, int, float, bool, type(None)))
            for k, v in obj.items()
        )
        if simple:
            items = [f'{k!r}: {v!r}' for k, v in obj.items()]
            return '{' + ', '.join(items) + '}'

    # Larger dicts with indentation
    lines = []
    for k, v in obj.items():
        formatted_val = argumentToString(v)
        if '\n' in formatted_val:
            indented = formatted_val.replace('\n', '\n    ')
            lines.append(f'  {k!r}: {indented}')
        else:
            lines.append(f'  {k!r}: {formatted_val}')

    return '{\n' + ',\n'.join(lines) + '\n}'


@argumentToString.register(list)
def _format_list(obj: list) -> str:
    """Format list objects."""
    if len(obj) > 50:
        return f'<list with {len(obj)} items>'

    if not obj:
        return '[]'

    # Small lists with simple values on one line
    if len(obj) <= 5:
        simple = all(isinstance(x, (str, int, float, bool, type(None))) for x in obj)
        if simple:
            return repr(obj)

    # Larger lists with indentation
    items = [argumentToString(x) for x in obj]
    if all('\n' not in item for item in items):
        joined = ', '.join(items)
        if len(joined) < 60:
            return '[' + joined + ']'

    formatted = ',\n  '.join(items)
    return '[\n  ' + formatted + '\n]'


@argumentToString.register(tuple)
def _format_tuple(obj: tuple) -> str:
    """Format tuple objects."""
    if len(obj) > 50:
        return f'<tuple with {len(obj)} items>'

    if not obj:
        return '()'

    if len(obj) == 1:
        return f'({argumentToString(obj[0])},)'

    # Small tuples with simple values on one line
    if len(obj) <= 5:
        simple = all(isinstance(x, (str, int, float, bool, type(None))) for x in obj)
        if simple:
            return repr(obj)

    items = [argumentToString(x) for x in obj]
    if all('\n' not in item for item in items):
        joined = ', '.join(items)
        if len(joined) < 60:
            return '(' + joined + ')'

    formatted = ',\n  '.join(items)
    return '(\n  ' + formatted + '\n)'


@argumentToString.register(set)
@argumentToString.register(frozenset)
def _format_set(obj: Union[set, frozenset]) -> str:
    """Format set and frozenset objects."""
    if len(obj) > 20:
        return f'<{type(obj).__name__} with {len(obj)} items>'

    if not obj:
        return 'set()' if isinstance(obj, set) else 'frozenset()'

    try:
        sorted_items = sorted(obj, key=str)
        items = [argumentToString(x) for x in sorted_items]

        if len(obj) <= 5:
            return '{' + ', '.join(items) + '}'

        return '{\n  ' + ',\n  '.join(items) + '\n}'
    except Exception:
        return f'<{type(obj).__name__} with {len(obj)} items>'


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
        includeContext: Optional[bool] = None,
        contextAbsPath: bool = False,
        contextMode: str = 'auto',
    ):
        """Initialize the IceCream debugger.

        Args:
            prefix: Prefix string or callable returning prefix.
            outputFunction: Function to output formatted text.
            argToStringFunction: Function to convert args to strings.
            includeContext: ``True``/``False`` to force context on/off.
                ``None`` (default) respects ``contextMode``.
            contextAbsPath: Whether to use absolute paths in context.
            contextMode: ``'auto'`` (default), ``'always'`` or ``'never'``.
        """
        self._enabled = True
        self._prefix = prefix
        self._outputFunction = outputFunction
        self._argToStringFunction = argToStringFunction
        self._includeContext = includeContext
        self._contextAbsPath = contextAbsPath
        self._contextMode = contextMode

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
        contextMode: Optional[str] = None,
        pairDelimiter: Optional[str] = None,
    ) -> None:
        """Configure output settings.

        Args:
            prefix: New prefix string or callable.
            outputFunction: New output function.
            argToStringFunction: New argument formatting function.
            includeContext: Force context on/off (``None`` respects
                ``contextMode``).
            contextAbsPath: Whether to use absolute paths.
            contextMode: ``'auto'``, ``'always'`` or ``'never'``.
            pairDelimiter: Separator between debugged values.

        Raises:
            TypeError: If no arguments are provided.
            ValueError: If ``contextMode`` is not a known mode.
        """
        if all(
            arg is None
            for arg in [
                prefix,
                outputFunction,
                argToStringFunction,
                includeContext,
                contextAbsPath,
                contextMode,
                pairDelimiter,
            ]
        ):
            raise TypeError('configureOutput() requires at least one argument')

        if contextMode is not None:
            mode = contextMode.lower()
            if mode not in ('auto', 'always', 'never'):
                raise ValueError("contextMode must be 'auto', 'always' or 'never'")
            self._contextMode = mode
            if includeContext is None:
                self._includeContext = None

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
        if pairDelimiter is not None:
            self._pair_delimiter = pairDelimiter

    def __call__(self, *args) -> Any:
        """Debug print the arguments and return them.

        Args:
            *args: Values to debug print.

        Returns:
            None if no args, single arg if one arg, tuple if multiple.
        """
        if self._enabled:
            current_frame = inspect.currentframe()
            call_frame = current_frame.f_back if current_frame else None
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
        current_frame = inspect.currentframe()
        call_frame = current_frame.f_back if current_frame else None
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
        arg_strs = self._extract_expressions(call_frame, args)
        context = self._resolve_context(call_frame, arg_strs, bool(args))

        if not args:
            # No args - show where we are and when
            time_str = self._format_time()
            if context:
                return f'{prefix}{context}{DEFAULT_CONTEXT_DELIMITER}{time_str}'
            return f'{prefix}{time_str}'

        return self._render(arg_strs, prefix, context, args)

    def _render(self, arg_strs, prefix, context, args) -> str:
        """Render the argument pairs into a styled, aligned line."""
        pairs = [
            (None if self._is_bare(expr) else expr, self._argToStringFunction(val))
            for expr, val in zip(arg_strs, args)
        ]
        return render_record(
            prefix,
            context,
            pairs,
            color=supports_color(sys.stderr),
            highlight=_colorize,
            delimiter=self._pair_delimiter,
        )

    @staticmethod
    def _is_bare(expr: object) -> bool:
        """True when the value should print without its expression.

        Literals, f-strings and unknown sources are self-describing.
        """
        return expr is _ABSENT or _is_literal(expr) or _is_fstring(expr)

    def _extract_expressions(self, call_frame, args: tuple) -> List[object]:
        """Recover the source text of each argument, or ``_ABSENT``."""
        if call_frame is None:
            return [_ABSENT] * len(args)

        call_node = Source.executing(call_frame).node
        if call_node is None:
            warnings.warn(NO_SOURCE_WARNING, RuntimeWarning, stacklevel=5)
            return [_ABSENT] * len(args)

        source = Source.for_frame(call_frame)
        return [source.get_text_with_indentation(arg) for arg in call_node.args]

    def _resolve_context(self, call_frame, arg_strs, has_args: bool) -> str:
        """Return the context string, honouring auto/always/never modes."""
        if self._contextMode == 'never':
            return ''
        if self._contextMode == 'always':
            return self._format_context(call_frame)
        # auto
        if self._includeContext is True:
            return self._format_context(call_frame)
        if self._includeContext is False:
            return ''
        if _needs_context(arg_strs, has_args):
            return self._format_context(call_frame)
        return ''

    def _get_prefix(self) -> str:
        """Get the current prefix string."""
        if isinstance(self._prefix, str):
            return self._prefix
        return self._prefix()

    def _format_context(self, call_frame) -> str:
        """Format the call context.

        Module-level code has no enclosing function, so the ``in <module>``
        suffix is dropped and only ``file:line`` is shown.
        """
        if call_frame is None:
            return '<unknown>:0'

        frame_info = inspect.getframeinfo(call_frame)

        if self._contextAbsPath:
            filename = realpath(frame_info.filename)
        else:
            filename = basename(frame_info.filename)

        location = f'{filename}:{frame_info.lineno}'
        func_name = frame_info.function

        if func_name in ('<module>', '<string>', '<stdin>', '<exec>'):
            return location

        return f'{location} in {func_name}()'

    def _format_time(self) -> str:
        """Format current time."""
        now = datetime.now()
        return now.strftime('%H:%M:%S.%f')[:-3]

    def __repr__(self) -> str:
        return f'<IceCreamDebugger prefix={self._prefix!r} enabled={self._enabled}>'


# ============================================================================
# Legacy Compatibility - LITPrintDebugger alias
# ============================================================================

# Alias for backward compatibility
LITPrintDebugger = IceCreamDebugger
