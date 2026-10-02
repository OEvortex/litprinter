#!/usr/bin/env python3
"""
LitPrinter - IceCream-compatible Debug Printing

This module provides ic-style debug printing with Rich-style formatting.
It's a drop-in replacement for IceCream, and a superset of builtin print().

Usage:
    # Debugging (zero-import after pip install litprinter)
    x = 42
    ic(x)              # ic| x: 42
    ic(x + 1)          # ic| [file.py:1 in <module>] >>> x + 1: 43

    # Printing (drop-in replacement for print())
    ic.print("hello", "world")                       # hello world
    ic.print("[bold red]error[/bold red]: boom")     # colored output

    # Logging without importing logging
    ic.info("server started on :8080")
    ic.error("connection refused")

    # Configure once
    ic.configureOutput(prefix="dbg| ", contextMode="never")
    ic.disable()

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
"""

from __future__ import annotations

import inspect
import sys
import time
from typing import IO, Any, Callable, Optional, Union

from .core import IceCreamDebugger, argumentToString
from .markup import render_markup, supports_color


# ============================================================================
# Log levels
# ============================================================================

_LEVELS = {
    'debug': ('\033[90m', 'DEBUG'),
    'info': ('\033[36m', 'INFO '),
    'success': ('\033[32m', 'OK   '),
    'warning': ('\033[33m', 'WARN '),
    'warn': ('\033[33m', 'WARN '),
    'error': ('\033[31m', 'ERROR'),
    'critical': ('\033[1;31m', 'CRIT '),
}


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
        ic(x)                     # Call like a function
        ic.print("hi")            # Like print(), with markup
        ic.info("event")          # Logging-style output
        ic.configureOutput(...)   # Access methods
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
        includeContext: Optional[bool] = None,
        contextAbsPath: Optional[bool] = None,
    ) -> Any:
        """Print arguments with their source expressions and return them.

        Args:
            *args: Values to debug print.
            includeContext: Force file/line context on or off for this call.
            contextAbsPath: Force absolute paths in context for this call.

        Returns:
            ``None`` for no args, the single argument, or a tuple of args.
        """
        debugger = self._debugger
        if not debugger.enabled:
            if not args:
                return None
            return args[0] if len(args) == 1 else args

        orig_context = debugger._includeContext
        orig_abs_path = debugger._contextAbsPath
        try:
            if includeContext is not None:
                debugger._includeContext = includeContext
            if contextAbsPath is not None:
                debugger._contextAbsPath = contextAbsPath

            current_frame = inspect.currentframe()
            call_frame = current_frame.f_back if current_frame else None
            output = debugger._format(call_frame, *args)
            debugger._outputFunction(output)
        finally:
            debugger._includeContext = orig_context
            debugger._contextAbsPath = orig_abs_path

        if not args:
            return None
        if len(args) == 1:
            return args[0]
        return args

    def format(self, *args) -> str:
        """Format arguments without printing."""
        current_frame = inspect.currentframe()
        call_frame = current_frame.f_back if current_frame else None
        return self._debugger._format(call_frame, *args)

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
    # Logging
    # ------------------------------------------------------------------
    def log(
        self,
        *values: Any,
        level: str = 'info',
        sep: str = ' ',
        file: Optional[IO[str]] = None,
        flush: bool = False,
        timestamp: bool = False,
        markup: bool = True,
        color: Optional[bool] = None,
    ) -> None:
        """Print a logging-style line without importing ``logging``.

        Args:
            *values: Values to log.
            level: One of debug, info, success, warning/warn, error,
                critical.
            sep: Separator inserted between values.
            file: Output stream (defaults to ``sys.stderr``).
            flush: Flush the stream after writing.
            timestamp: Prefix the line with the current time.
            markup: Interpret inline markup tags.
            color: Force ANSI colors on/off. Defaults to auto-detection.
        """
        key = level.lower()
        if key not in _LEVELS:
            raise ValueError(
                f'Unknown log level {level!r}; expected one of '
                f'{", ".join(sorted(_LEVELS))}'
            )

        stream = file if file is not None else sys.stderr
        use_color = supports_color(stream) if color is None else color

        code, label = _LEVELS[key]
        body = sep.join(
            render_markup(value, color=use_color)
            if markup and isinstance(value, str)
            else str(value)
            for value in values
        )

        if use_color:
            label = f'{code}{label}\033[0m'
        else:
            label = label.strip()

        prefix = f'{time.strftime("%H:%M:%S")} ' if timestamp else ''
        _write(f'{prefix}{label} {body}', file=stream, flush=flush)

    def debug(self, *values: Any, **kwargs: Any) -> None:
        """Log at DEBUG level."""
        self.log(*values, level='debug', **kwargs)

    def info(self, *values: Any, **kwargs: Any) -> None:
        """Log at INFO level."""
        self.log(*values, level='info', **kwargs)

    def success(self, *values: Any, **kwargs: Any) -> None:
        """Log at SUCCESS level."""
        self.log(*values, level='success', **kwargs)

    def warning(self, *values: Any, **kwargs: Any) -> None:
        """Log at WARNING level."""
        self.log(*values, level='warning', **kwargs)

    warn = warning

    def error(self, *values: Any, **kwargs: Any) -> None:
        """Log at ERROR level."""
        self.log(*values, level='error', **kwargs)

    def critical(self, *values: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level."""
        self.log(*values, level='critical', **kwargs)

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


def format(*args) -> str:
    """Format arguments without printing."""
    current_frame = inspect.currentframe()
    call_frame = current_frame.f_back if current_frame else None
    return ic._debugger._format(call_frame, *args)


def log(*values: Any, level: str = 'info', **kwargs: Any) -> None:
    """Print a logging-style line (module-level shortcut)."""
    ic.log(*values, level=level, **kwargs)


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
    'log',
    'configureOutput',
    'enable',
    'disable',
    'format',
    # Core exports
    'argumentToString',
    'IceCreamDebugger',
]
