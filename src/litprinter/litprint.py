#!/usr/bin/env python3
"""
LitPrinter - IceCream-compatible Debug Printing

``ic`` is the single entry point for terminal output: debugging, printing and
logging all go through it, so there is one thing to learn and one thing to
disable.

Usage::

    from litprinter import ic

    x = 42
    ic(x)                       # ic| x: 42
    ic(x * 2)                   # ic| [app.py:5] >>> x * 2: 84
    ic.print("hello", "world")  # hello world
    ic("connected", url)        # ERROR/INFO-free plain logging
    ic("db unreachable", level="error")

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
"""

from __future__ import annotations

import inspect
import sys
from typing import IO, Any, Callable, Optional, Union

from .core import IceCreamDebugger, argumentToString, render_level_prefix
from .markup import render_markup, supports_color


def _write(
    text: str,
    *,
    file: Optional[IO[str]] = None,
    end: str = '\n',
    flush: bool = False,
) -> None:
    """Write ``text`` to ``file`` (stdout by default)."""
    stream = file if file is not None else sys.stdout
    stream.write(text + end)
    if flush:
        try:
            stream.flush()
        except Exception:
            pass


class _IceCreamWrapper:
    """Callable debug printer with print() and logging helpers.

    This allows:
        ic(x)                       # Debug print
        ic(x, level="error")        # Same call, with a severity tag
        ic.print("hi")              # Like print(), with markup
        ic.configureOutput(...)     # Access methods
        ic.disable() / ic.enable()
    """

    def __init__(self) -> None:
        self._debugger = IceCreamDebugger()

    # ------------------------------------------------------------------
    # Debugging
    # ------------------------------------------------------------------
    def __call__(
        self,
        *args,
        level: Optional[str] = None,
        includeContext: Optional[bool] = None,
        contextAbsPath: Optional[bool] = None,
        **fields: Any,
    ) -> Any:
        """Print arguments with their source expressions and return them.

        This is the single entry point for debugging, printing and logging.
        Pass ``level`` to tag the line with a severity and keyword arguments to
        attach named fields.

        Args:
            *args: Values to debug print.
            level: Optional severity tag: ``debug``, ``info``, ``success``,
                ``warning``, ``error`` or ``critical``.
            includeContext: Force file/line context on or off for this call.
            contextAbsPath: Force absolute paths in context for this call.
            **fields: Named values appended as ``name: value`` pairs. Handy
                for logging, e.g. ``ic("retrying", attempt=2, level="warn")``.
                The three keywords above are reserved by the printer.

        Returns:
            ``None`` for no args, the single argument, or a tuple of args.
            ``fields`` never affect the return value.

        Raises:
            ValueError: If ``level`` is not a known severity.
        """
        debugger = self._debugger
        if not debugger.enabled:
            if not args:
                return None
            return args[0] if len(args) == 1 else args

        # Validate before touching any state so a typo fails loudly.
        prefix = None
        if level is not None:
            prefix = render_level_prefix(level, color=supports_color(sys.stderr))

        orig_context = debugger._includeContext
        orig_abs_path = debugger._contextAbsPath
        try:
            if includeContext is not None:
                debugger._includeContext = includeContext
            if contextAbsPath is not None:
                debugger._contextAbsPath = contextAbsPath

            current_frame = inspect.currentframe()
            call_frame = current_frame.f_back if current_frame else None
            output = debugger._format(
                call_frame,
                *args,
                prefix=prefix,
                context_arrow=level is None,
                fields=fields,
            )
            debugger._outputFunction(output)
        finally:
            debugger._includeContext = orig_context
            debugger._contextAbsPath = orig_abs_path

        if not args:
            return None
        if len(args) == 1:
            return args[0]
        return args

    def format(self, *args, level: Optional[str] = None, **fields: Any) -> str:
        """Format arguments without printing.

        Args:
            *args: Values to format.
            level: Optional severity tag, see :meth:`__call__`.
            **fields: Named values, see :meth:`__call__`.
        """
        prefix = (
            None
            if level is None
            else render_level_prefix(level, color=supports_color(sys.stderr))
        )
        current_frame = inspect.currentframe()
        call_frame = current_frame.f_back if current_frame else None
        return self._debugger._format(
            call_frame,
            *args,
            prefix=prefix,
            context_arrow=level is None,
            fields=fields,
        )

    # ------------------------------------------------------------------
    # Printing
    # ------------------------------------------------------------------
    def print(
        self,
        *values: Any,
        sep: str = ' ',
        end: str = '\n',
        file: Optional[IO[str]] = None,
        flush: bool = False,
        markup: bool = True,
        style: Optional[str] = None,
        color: Optional[bool] = None,
        highlight: bool = False,
    ) -> None:
        """Drop-in replacement for ``print()`` with inline markup support.

        The signature mirrors builtin ``print()`` exactly, so existing
        ``print(...)`` calls can be swapped for ``ic.print(...)`` one-to-one.
        Non-string values are stringified with the same formatter ``ic()``
        uses, and can optionally be syntax highlighted.

        Args:
            *values: Values to print.
            sep: Separator inserted between values.
            end: String appended after the last value.
            file: Output stream (defaults to ``sys.stdout``).
            flush: Flush the stream after writing.
            markup: Interpret ``[bold red]...[/]`` style tags.
            style: Default style for the whole line, e.g. ``"bold cyan"``.
            color: Force ANSI colors on/off. Defaults to auto-detection.
            highlight: Syntax highlight non-string values with Pygments.
        """
        use_color = supports_color(file) if color is None else color
        parts = []
        for value in values:
            if isinstance(value, str):
                text = render_markup(value, color=use_color) if markup else value
            else:
                text = str(self._debugger._argToStringFunction(value))
                if highlight and use_color:
                    from .core import _colorize

                    text = _colorize(text)
            parts.append(text)

        line = sep.join(parts)
        if style and use_color:
            line = render_markup(f'[{style}]{line}[/]', color=True)
        _write(line, file=file, end=end, flush=flush)

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
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
            prefix: Prefix string or callable.
            outputFunction: Function used to emit formatted output.
            argToStringFunction: Function used to stringify arguments.
            includeContext: Force context on/off (``None`` respects mode).
            contextAbsPath: Whether to use absolute paths in context.
            contextMode: ``'auto'``, ``'always'`` or ``'never'``.
            pairDelimiter: Separator between debugged values.
        """
        self._debugger.configureOutput(
            prefix=prefix,
            outputFunction=outputFunction,
            argToStringFunction=argToStringFunction,
            includeContext=includeContext,
            contextAbsPath=contextAbsPath,
            contextMode=contextMode,
            pairDelimiter=pairDelimiter,
        )

    def enable(self) -> None:
        """Enable debug output."""
        self._debugger.enable()

    def disable(self) -> None:
        """Disable debug output."""
        self._debugger.disable()

    def install(self, name: str = 'ic') -> None:
        """Install this printer into builtins under ``name``."""
        import builtins

        setattr(builtins, name, self)

    def uninstall(self, name: str = 'ic') -> None:
        """Remove this printer from builtins."""
        import builtins

        if hasattr(builtins, name):
            delattr(builtins, name)

    @property
    def enabled(self) -> bool:
        """Whether debug output is enabled."""
        return self._debugger.enabled

    def __repr__(self) -> str:
        return f'<ic enabled={self.enabled}>'


# ============================================================================
# Module-level Instances and Aliases
# ============================================================================

ic = _IceCreamWrapper()

# Aliases for compatibility
LIT = ic
litprint = ic
lit = ic

# Drop-in replacement for builtin print():  litprinter.print(...)
print = ic.print


# ============================================================================
# Module-level convenience functions
# ============================================================================


def configureOutput(
    prefix: Union[str, Callable[[], str], None] = None,
    outputFunction: Optional[Callable[[str], None]] = None,
    argToStringFunction: Optional[Callable[[Any], str]] = None,
    includeContext: Optional[bool] = None,
    contextAbsPath: Optional[bool] = None,
    contextMode: Optional[str] = None,
    pairDelimiter: Optional[str] = None,
) -> None:
    """Configure the global ic output settings."""
    ic.configureOutput(
        prefix=prefix,
        outputFunction=outputFunction,
        argToStringFunction=argToStringFunction,
        includeContext=includeContext,
        contextAbsPath=contextAbsPath,
        contextMode=contextMode,
        pairDelimiter=pairDelimiter,
    )


def enable() -> None:
    """Enable debug output globally."""
    ic.enable()


def disable() -> None:
    """Disable debug output globally."""
    ic.disable()


def format(*args, level: Optional[str] = None, **fields: Any) -> str:
    """Format arguments without printing.

    Args:
        *args: Values to format.
        level: Optional severity tag, see :meth:`_IceCreamWrapper.__call__`.
        **fields: Named values, see :meth:`_IceCreamWrapper.__call__`.
    """
    return ic.format(*args, level=level, **fields)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Main instance
    'ic',
    # Aliases
    'LIT',
    'litprint',
    'lit',
    # Functions
    'print',
    'configureOutput',
    'enable',
    'disable',
    'format',
    # Core exports
    'argumentToString',
    'IceCreamDebugger',
]
