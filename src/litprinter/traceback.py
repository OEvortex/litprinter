#!/usr/bin/env python3
"""
LitPrinter Traceback Module

Readable, syntax-highlighted tracebacks with local variable inspection.

The hook is installed automatically when litprinter is installed, so you
normally get this output with no setup at all. To change it:

    from litprinter import traceback

    traceback.install(
        show_locals=True,
        extra_lines=3,
        suppress=["site-packages"],
    )

Opt out entirely (before Python starts) with ``LITPRINTER_NO_TRACEBACK=1``,
and restore the default handler at runtime with ``traceback.uninstall()``.

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
"""

import sys
import traceback
import linecache
import os
import pprint
import shutil
import datetime
from dataclasses import dataclass, field
from types import (
    TracebackType,
    FrameType,
    ModuleType,
    FunctionType,
    BuiltinFunctionType,
    MethodType,
)
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
)

# --- Pygments Requirement & Style Imports ---
# Pygments is a hard dependency (see pyproject.toml), so these are plain
# imports rather than guarded ones.
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.python import PythonLexer
from pygments.lexers.special import TextLexer
from pygments.formatters.terminal256 import (
    Terminal256Formatter as _Terminal256Formatter,
)
from pygments.util import ClassNotFound

from .colors import Colors
from .render import visible_width
from .theme import LitPrinterStyle

# Type alias for the frame-suppression patterns
SuppressType = Iterable[str]


# --- Configuration ---
# Maximum number of variables to display in locals
MAX_VARIABLES = 15
# Maximum length for variable representation
MAX_VARIABLE_LENGTH = 100
# Maximum depth for nested structures in locals
LOCALS_MAX_DEPTH = 2
# Number of extra lines to show around the error line
DEFAULT_EXTRA_LINES = 5
# Default terminal width if detection fails
DEFAULT_WIDTH = 100
# Separator for stack traces
STACK_SEPARATOR = '─'
# Marker for the error line
ERROR_LINE_MARKER = '❱'
# Marker for code line numbers
LINE_SEPARATOR = '│'
# Module-level names hidden from show_locals (this module's own machinery)
_MODULE_LEVEL_NOISE = frozenset(
    {
        'PrettyTraceback',
        'FrameInfo',
        '_SyntaxError',
        'Stack',
        'Trace',
        'Styles',
        'install',
        'uninstall',
        'Traceback',
        'LitPrinterStyle',
        'DEFAULT_EXTRA_LINES',
        'DEFAULT_WIDTH',
        'MAX_VARIABLES',
        'MAX_VARIABLE_LENGTH',
        'LOCALS_MAX_DEPTH',
        'STACK_SEPARATOR',
        'ERROR_LINE_MARKER',
        'LINE_SEPARATOR',
    }
)


# --- ANSI Color Codes & Styles ---
class Styles:
    """Styling utilities for traceback formatting.

    This class provides methods for styling different parts of the traceback output
    using ANSI color codes from the Colors class. Each method applies specific styling
    to different elements of the traceback for better visual distinction.
    """

    # Use Colors class from colors.py for ANSI codes
    RESET = Colors.RESET
    BOLD = Colors.BOLD
    DIM = Colors.DIM
    ITALIC = Colors.ITALIC
    RED = Colors.RED
    GREEN = Colors.GREEN
    YELLOW = Colors.YELLOW
    BLUE = Colors.BLUE
    MAGENTA = Colors.MAGENTA
    CYAN = Colors.CYAN
    WHITE = Colors.WHITE
    GREY = Colors.GRAY  # Note: Colors uses GRAY, not GREY

    # Additional combined styles for convenience
    ERROR_STYLE = RED + BOLD
    WARNING_STYLE = YELLOW + BOLD
    INFO_STYLE = BLUE + BOLD
    SUCCESS_STYLE = GREEN + BOLD

    @staticmethod
    def Muted(text: str) -> str:
        """Style for muted/less important text."""
        return Styles.GREY + str(text) + Styles.RESET

    @staticmethod
    def FilePath(text: str) -> str:
        """Style for file paths in tracebacks."""
        return Styles.BLUE + str(text) + Styles.RESET

    @staticmethod
    def LineNo(text: str) -> str:
        """Style for line numbers in tracebacks."""
        return Styles.YELLOW + str(text) + Styles.RESET

    @staticmethod
    def FunctionName(text: str) -> str:
        """Style for function names in tracebacks."""
        return Styles.CYAN + str(text) + Styles.RESET

    @staticmethod
    def LibraryIndicator(text: str) -> str:
        """Style for library indicators in tracebacks."""
        return Styles.Muted(f'[{str(text)}]')

    @staticmethod
    def ModuleName(text: str) -> str:
        """Style for module names in tracebacks."""
        return Styles.Muted(f'{str(text)}')

    @staticmethod
    def Error(text: str) -> str:
        """Style for error messages."""
        return Styles.RED + str(text) + Styles.RESET

    @staticmethod
    def ErrorBold(text: str) -> str:
        """Style for important error messages."""
        return Styles.ERROR_STYLE + str(text) + Styles.RESET

    @staticmethod
    def ErrorMarker(text: str) -> str:
        """Style for error line markers."""
        return Styles.ErrorBold(str(text))

    @staticmethod
    def LocalsHeader(text: str) -> str:
        """Style for local variables section header."""
        return Styles.BOLD + Styles.WHITE + str(text) + Styles.RESET

    @staticmethod
    def LocalsKey(text: str) -> str:
        """Style for local variable names."""
        return Styles.MAGENTA + str(text) + Styles.RESET

    @staticmethod
    def LocalsEquals(text: str) -> str:
        """Style for equals sign in local variable display."""
        return Styles.GREY + str(text) + Styles.RESET

    @staticmethod
    def LocalsValue(text: str) -> str:
        """Style for generic local variable values."""
        return Styles.WHITE + str(text) + Styles.RESET

    @staticmethod
    def ValueNone(text: str) -> str:
        """Style for None values."""
        return Styles.ITALIC + Styles.GREY + str(text) + Styles.RESET

    @staticmethod
    def ValueBool(text: str) -> str:
        """Style for boolean values."""
        return Styles.GREEN + str(text) + Styles.RESET

    @staticmethod
    def ValueStr(text: str) -> str:
        """Style for string values."""
        return Styles.YELLOW + str(text) + Styles.RESET

    @staticmethod
    def ValueNum(text: str) -> str:
        """Style for numeric values."""
        return Styles.BLUE + str(text) + Styles.RESET

    @staticmethod
    def ValueType(text: str) -> str:
        """Style for type objects."""
        return Styles.CYAN + str(text) + Styles.RESET

    @staticmethod
    def ValueContainer(text: str) -> str:
        """Style for container objects (lists, dicts, etc)."""
        return Styles.MAGENTA + str(text) + Styles.RESET

    @staticmethod
    def Bold(text: str) -> str:
        """Apply bold style to text."""
        return Styles.BOLD + str(text) + Styles.RESET

    @staticmethod
    def Dim(text: str) -> str:
        """Apply dim style to text."""
        return Styles.DIM + str(text) + Styles.RESET

    @staticmethod
    def strip_styles(text: str) -> str:
        """Remove all ANSI escape sequences from text."""
        return Colors.strip_ansi(text)


# --- Data Classes ---
@dataclass
class FrameInfo:
    """Information about a single frame in the traceback."""

    frame_obj: Optional[FrameType]  # The actual frame object
    filename: str  # File where the frame is located
    lineno: int  # Line number in the file
    name: str  # Function name
    line: str = ''  # Source code line
    locals: Optional[Dict[str, Any]] = None  # Local variables
    is_module_frame: bool = False  # Whether this is a module-level frame
    is_library_file: bool = False  # Whether this is from a library file


@dataclass
class _SyntaxError:
    """Information about a syntax error."""

    offset: Optional[int]  # Character offset where the error occurred
    filename: str  # File where the error occurred
    line: str  # Source code line with the error
    lineno: int  # Line number in the file
    msg: str  # Error message


@dataclass
class Stack:
    """Information about an exception stack."""

    exc_type: str  # Exception type name
    exc_value: str  # Exception value as string
    exc_type_full: str  # Full exception type
    syntax_error: Optional[_SyntaxError] = None  # Syntax error info if applicable
    is_cause: bool = False  # Whether this is a cause of another exception
    is_context: bool = False  # Whether this is a context of another exception
    frames: List[FrameInfo] = field(default_factory=list)  # Stack frames
    omitted_frames: int = 0  # How many frames max_frames dropped


@dataclass
class Trace:
    """Complete trace information with all exception stacks."""

    stacks: List[Stack]  # List of exception stacks


# --- Core Traceback Logic ---
class PrettyTraceback:
    """Enhanced traceback formatter with syntax highlighting and improved readability.

    This class provides a more user-friendly traceback display with:
    - Syntax highlighting using Pygments (if available)
    - Local variable inspection
    - Better visual formatting of error information
    - Support for exception chaining
    - Frame suppression for cleaner output

    Args:
        exc_type: The exception type
        exc_value: The exception value
        tb: The traceback object
        extra_lines: Number of extra lines to show around the error line
        show_locals: Whether to show local variables
        locals_max_string: Maximum length for string variables
        locals_max_depth: Maximum depth for nested structures
        locals_hide_dunder: Whether to hide dunder variables
        locals_hide_sunder: Whether to hide single-underscore variables
        width: Terminal width (auto-detected if None)
        suppress: Paths/modules to suppress from traceback
        max_frames: Maximum number of frames to show
    """

    def __init__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        tb: Optional[TracebackType],
        *,
        extra_lines: int = DEFAULT_EXTRA_LINES,
        show_locals: bool = False,
        locals_max_string: int = MAX_VARIABLE_LENGTH,
        locals_max_depth: int = LOCALS_MAX_DEPTH,
        locals_hide_dunder: bool = True,
        locals_hide_sunder: bool = False,
        width: Optional[int] = None,
        suppress: SuppressType = (),
        max_frames: int = 100,
    ):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.tb = tb
        self.extra_lines = extra_lines
        self.show_locals = show_locals
        self.locals_max_string = locals_max_string
        self.locals_max_depth = locals_max_depth
        self.locals_hide_dunder = locals_hide_dunder
        self.locals_hide_sunder = locals_hide_sunder
        self.terminal_width = width or self._get_terminal_width()
        self.suppress = set(suppress)
        self.max_frames = max_frames
        self._pp = pprint.PrettyPrinter(
            depth=self.locals_max_depth,
            width=max(20, self.terminal_width - 20),
            compact=True,
        )

        # One style for the whole package; fall back to plain text if the
        # formatter cannot be built.
        self.style_cls = LitPrinterStyle
        try:
            self.formatter = _Terminal256Formatter(style=self.style_cls)
        except Exception:
            self.formatter = None

        self.trace = self._extract_trace()

    # --- Helper methods ---
    @staticmethod
    def _get_terminal_width() -> int:
        try:
            width = shutil.get_terminal_size(fallback=(DEFAULT_WIDTH, 20)).columns
            return max(40, width)
        except Exception:
            return DEFAULT_WIDTH

    @staticmethod
    def _safe_str(obj: Any) -> str:
        try:
            return str(obj)
        except Exception:
            return '<exception str() failed>'

    @staticmethod
    def _is_library_file(filename: str) -> bool:
        """True when a frame belongs to the stdlib or an installed package."""
        if not filename or '<' in filename or '>' in filename:
            return False
        try:
            abs_path = os.path.abspath(filename)
            stdlib_dir = os.path.dirname(os.__file__)
            if stdlib_dir and abs_path.startswith(stdlib_dir):
                return True
            site_packages_dirs = [
                p for p in sys.path if 'site-packages' in p or 'dist-packages' in p
            ]
            return any(abs_path.startswith(p) for p in site_packages_dirs)
        except Exception:
            return False

    @staticmethod
    def _is_skippable_local(
        key: str,
        value: Any,
        frame_is_module: bool,
        hide_dunder: bool,
        hide_sunder: bool,
    ) -> bool:
        """Decide whether a local variable should be hidden from show_locals."""
        if hide_dunder and key.startswith('__') and key.endswith('__'):
            return True
        if hide_sunder and key.startswith('_') and not key.startswith('__'):
            return True
        if frame_is_module:
            if isinstance(
                value, (ModuleType, FunctionType, type, BuiltinFunctionType, MethodType)
            ):
                return True
            # Module-level noise: this module's own machinery.
            if key in _MODULE_LEVEL_NOISE:
                return True
        return False

    # --- Trace Extraction (_extract_trace, _extract_single_frame - remain the same) ---
    def _extract_trace(self) -> Trace:
        """Extract the complete exception trace including all chained exceptions.

        This method walks through the exception chain, handling both __cause__ (from raise ... from)
        and __context__ (from exceptions during exception handling) relationships.

        Returns:
            A Trace object containing all exception stacks in the chain.
        """
        stacks: List[Stack] = []
        current_exc_type = self.exc_type
        current_exc_value = self.exc_value
        current_tb = self.tb
        processed_exceptions = set()

        # Process the exception chain
        while current_exc_type is not None and current_exc_value is not None:
            # Detect cycles in the exception chain to prevent infinite loops
            exception_id = id(current_exc_value)
            if exception_id in processed_exceptions:
                print(
                    Styles.WARNING_STYLE
                    + 'WARNING: Detected cycle in exception chain.'
                    + Styles.RESET,
                    file=sys.stderr,
                )
                break
            processed_exceptions.add(exception_id)

            # Determine the relationship between this exception and the previous one
            is_cause = bool(
                stacks
                and getattr(stacks[-1].exc_value, '__cause__', None)
                is current_exc_value
            )
            suppress_ctx = (
                getattr(stacks[-1].exc_value, '__suppress_context__', False)
                if stacks
                else False
            )
            is_context = bool(
                stacks
                and getattr(stacks[-1].exc_value, '__context__', None)
                is current_exc_value
                and not suppress_ctx
            )

            # Create a Stack object for this exception
            stack = Stack(
                exc_type=self._safe_str(current_exc_type.__name__),
                exc_value=self._safe_str(current_exc_value),
                exc_type_full=str(current_exc_type),
                is_cause=is_cause,
                is_context=is_context,
            )

            # Handle SyntaxError specially
            if isinstance(current_exc_value, SyntaxError):
                stack.syntax_error = _SyntaxError(
                    offset=current_exc_value.offset,
                    filename=current_exc_value.filename or '?',
                    lineno=current_exc_value.lineno or 0,
                    line=current_exc_value.text or '',
                    msg=current_exc_value.msg,
                )

            # Extract frames from the traceback
            extracted_frames: List[FrameInfo] = []
            if current_tb is not None:
                try:
                    is_first = True
                    for frame_obj, lineno in traceback.walk_tb(current_tb):
                        filename = frame_obj.f_code.co_filename
                        if self.is_suppressed(filename):
                            is_first = False
                            continue
                        is_module = is_first and (not frame_obj.f_back)
                        extracted_frames.append(
                            self._extract_single_frame(frame_obj, lineno, is_module)
                        )
                        is_first = False
                    if len(extracted_frames) > self.max_frames:
                        # Keep the frames closest to the error.
                        omitted = len(extracted_frames) - self.max_frames
                        extracted_frames = extracted_frames[-self.max_frames :]
                        stack.frames = extracted_frames
                        stack.omitted_frames = omitted
                    else:
                        stack.frames = extracted_frames
                except Exception as e:
                    error_msg = f'ERROR: Could not extract frames using walk_tb: {e}'
                    print(
                        Styles.ERROR_STYLE + error_msg + Styles.RESET, file=sys.stderr
                    )

            # Clear the linecache to ensure we get fresh source lines
            linecache.clearcache()
            stacks.append(stack)

            # Find the next exception in the chain
            next_cause = getattr(current_exc_value, '__cause__', None)
            next_context = getattr(current_exc_value, '__context__', None)
            next_suppress_context = getattr(
                current_exc_value, '__suppress_context__', False
            )

            # Prioritize explicit causes over implicit contexts
            if next_cause is not None:
                next_exc_value = next_cause
            elif next_context is not None and not next_suppress_context:
                next_exc_value = next_context
            else:
                next_exc_value = None

            # Update current exception info for the next iteration
            if next_exc_value is not None:
                current_exc_value = next_exc_value
                current_exc_type = type(current_exc_value)
                current_tb = current_exc_value.__traceback__
            else:
                current_exc_type, current_exc_value, current_tb = None, None, None

        # Return the trace with stacks in chronological order (reversed)
        return Trace(stacks=list(reversed(stacks)))

    def _extract_single_frame(
        self, frame_obj: FrameType, lineno: int, is_module: bool
    ) -> FrameInfo:
        """Extract information from a single frame in the traceback.

        Args:
            frame_obj: The frame object to extract information from
            lineno: The line number in the frame
            is_module: Whether this is a module-level frame

        Returns:
            A FrameInfo object containing the extracted frame information
        """
        # Extract basic frame information
        f_code = frame_obj.f_code
        filename = f_code.co_filename or '?'
        func_name = f_code.co_name or '?'
        is_lib = self._is_library_file(filename)

        # Get the source line from the cache
        try:
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, frame_obj.f_globals).strip()
        except Exception:
            # Handle any errors in line retrieval
            line = '<error retrieving source line>'

        # Extract and filter local variables if requested
        frame_locals_filtered = None
        if self.show_locals:
            try:
                frame_locals_unfiltered = frame_obj.f_locals
                frame_locals_filtered = {
                    k: v
                    for k, v in frame_locals_unfiltered.items()
                    if not self._is_skippable_local(
                        k,
                        v,
                        is_module,
                        self.locals_hide_dunder,
                        self.locals_hide_sunder,
                    )
                }
            except Exception:
                # If we can't access locals, provide a placeholder
                frame_locals_filtered = {'<error>': '<error accessing local variables>'}

        # Create and return the FrameInfo object
        return FrameInfo(
            frame_obj=frame_obj,
            filename=filename,
            lineno=lineno,
            name=func_name,
            line=line,
            locals=frame_locals_filtered,
            is_module_frame=is_module,
            is_library_file=is_lib,
        )

    # --- Formatting Helpers ---
    def _color_code_value(self, value_repr: str) -> str:
        """Colour a repr() string according to the kind of value it holds."""
        val = value_repr.strip()

        if val in ('None', 'True', 'False'):
            return Styles.ValueNone(val) if val == 'None' else Styles.ValueBool(val)

        if len(val) >= 2 and val[0] == val[-1] and val[0] in '\'"':
            return Styles.ValueStr(val)

        if val.lstrip('-').replace('.', '', 1).isdigit():
            return Styles.ValueNum(val)

        if val.startswith(('<class ', '<function ', '<module ', '<bound method ')):
            return Styles.ValueType(val)

        if val.startswith(('{', '[', '(')) or (
            val.startswith('<') and val.endswith('>')
        ):
            return Styles.ValueContainer(val)

        return Styles.LocalsValue(val)

    def _format_locals(self, locals_dict: Dict[str, Any]) -> List[str]:
        """Format local variables for display in the traceback, with type info and better truncation."""
        if not locals_dict:
            return []

        formatted_vars = []
        sorted_items = sorted(locals_dict.items())
        count = 0
        for name, value in sorted_items:
            if count >= MAX_VARIABLES:
                remaining = len(sorted_items) - count
                formatted_vars.append(
                    (Styles.Dim('...'), Styles.Dim(f'<{remaining} more variables>'))
                )
                break
            try:
                value_repr = self._pp.pformat(value)
                if len(value_repr) > self.locals_max_string:
                    value_repr = value_repr[: self.locals_max_string - 1] + '…'
                type_str = (
                    f'  {Styles.Dim("[" + type(value).__name__ + "]")}'
                    if not isinstance(value, (int, float, str, bool, type(None)))
                    else ''
                )
            except Exception:
                value_repr = Styles.Error('<exception repr() failed>')
                type_str = ''
            colored_value = self._color_code_value(value_repr) + type_str
            formatted_vars.append((Styles.LocalsKey(name), colored_value))
            count += 1
        lines = []
        num_vars = len(formatted_vars)
        mid_point = (num_vars + 1) // 2
        col1_width = 0
        if num_vars > 0:
            try:
                col1_width = (
                    max(
                        len(Styles.strip_styles(k))
                        for k, _ in formatted_vars[:mid_point]
                    )
                    + 3
                )
            except ValueError:
                col1_width = 3
        for i in range(mid_point):
            key1, val1 = formatted_vars[i]
            key1_clean_len = len(Styles.strip_styles(key1))
            key1_padded = key1 + ' ' * max(0, col1_width - key1_clean_len - 3)
            line = f'  {key1_padded} {Styles.LocalsEquals("=")} {val1}'
            j = i + mid_point
            if j < num_vars:
                key2, val2 = formatted_vars[j]
                line += (
                    f'    {Styles.LocalsKey(key2)} {Styles.LocalsEquals("=")} {val2}'
                )
            lines.append(line)
        return lines

    def _format_syntax_error(self, error: _SyntaxError) -> Iterable[str]:
        """Format a syntax error for display.

        This method creates a visually clear representation of a syntax error,
        including the error location marker and message.

        Args:
            error: The syntax error information

        Yields:
            Formatted lines for the syntax error display
        """
        # Add a blank line before the error header
        yield ''

        # Display the error header with filename and line number
        yield Styles.ErrorBold(
            f'Syntax Error in {Styles.FilePath(error.filename)} at line {Styles.LineNo(str(error.lineno))}:'
        )

        # Add a blank line after the header
        yield ''

        # Show the line with the syntax error
        if error.line:
            yield f'  {error.line.rstrip()}'

            # Add the error marker (^) pointing to the exact position of the error
            if error.offset is not None and error.offset > 0:
                marker_pos = error.offset - 1
                yield f'  {" " * marker_pos}{Styles.ErrorBold("^")}'
        else:
            yield Styles.Muted('  [Source line not available]')

        # Add a blank line before the error message
        yield ''

        # Show the error message
        yield Styles.Error(error.msg)

    def _format_exception_message(self, stack: Stack) -> str:
        """Format the main exception message.

        Args:
            stack: The exception stack information

        Returns:
            A formatted string with the exception type and message
        """
        return f'{Styles.ErrorBold(stack.exc_type)}: {Styles.Error(stack.exc_value)}'

    # --- Main Rendering Logic ---
    def _format_header(self, term_width: int, timestamp: str) -> str:
        """Render the top banner, e.g. ``--- Traceback (most recent call last) ---``."""
        label = Styles.ErrorBold('Traceback (most recent call last)')
        stamp = Styles.Muted(timestamp)
        fill = max(0, term_width - visible_width(label) - visible_width(stamp) - 6)
        return (
            f'{Styles.Error("─" * 2)} {label} '
            f'{Styles.Error("─" * max(0, fill // 2))} {stamp} '
            f'{Styles.Error("─" * (fill - fill // 2))}'
        )

    def _format_frame_header(self, frame_info: FrameInfo) -> str:
        """Format the header line for a stack frame.

        Library frames are dimmed end to end so the frames in the user's own
        code stand out, and are tagged ``[library]`` instead of carrying the
        module name twice.
        """
        func_info = Styles.FunctionName(frame_info.name)
        line_info = Styles.LineNo(str(frame_info.lineno))

        if frame_info.is_library_file:
            return (
                f'  {Styles.Muted(os.path.basename(frame_info.filename))}'
                f'{Styles.LineNo(f":{frame_info.lineno}")} {func_info}'
                f' {Styles.LibraryIndicator("library")}'
            )

        module_name = ''
        if frame_info.frame_obj:
            module_name = frame_info.frame_obj.f_globals.get('__name__', '') or ''
        location = Styles.FilePath(frame_info.filename)
        parts = [f'  File "{location}", line {line_info}, in {func_info}']
        if module_name and module_name != '__main__':
            parts.append(f' {Styles.ModuleName(module_name)}')
        return ''.join(parts)

    def _format_code_context(self, frame_info: FrameInfo) -> List[str]:
        """Format the code context for a stack frame with syntax highlighting.

        This method extracts the source code around the error line, applies syntax
        highlighting if Pygments is available, and formats the code with line numbers
        and error markers.

        Args:
            frame_info: The frame information object containing file and line details

        Returns:
            A list of formatted code context lines ready for display
        """
        code_context_lines = []
        lines_available = False

        # Only try to get source code if we have a valid filename and line number
        if frame_info.filename != '?' and frame_info.lineno > 0:
            try:
                # Get all lines from the file
                lines_for_snippet = linecache.getlines(frame_info.filename)

                if lines_for_snippet:
                    lines_available = True

                    # Calculate the range of lines to show
                    start_line_idx = max(0, frame_info.lineno - 1 - self.extra_lines)
                    end_line_idx = min(
                        len(lines_for_snippet), frame_info.lineno + self.extra_lines
                    )

                    # Join the lines into a single string for highlighting
                    code_snippet = ''.join(
                        lines_for_snippet[start_line_idx:end_line_idx]
                    )
                    highlighted_code = code_snippet

                    # Apply syntax highlighting if Pygments is available
                    if self.formatter:
                        # Default to plain text lexer
                        lexer = TextLexer()

                        # Try to guess the appropriate lexer based on the filename
                        if (
                            frame_info.filename != '<string>'
                            and not frame_info.filename.startswith('<')
                        ):
                            try:
                                lexer = guess_lexer_for_filename(
                                    frame_info.filename, code_snippet
                                )
                            except ClassNotFound:
                                # If we can't guess the lexer, default to Python for .py files
                                if frame_info.filename.endswith('.py'):
                                    lexer = PythonLexer()
                        else:
                            # For string-based execution, assume Python
                            lexer = PythonLexer()

                        try:
                            # Apply the highlighting
                            highlighted_code = highlight(
                                code_snippet, lexer, self.formatter
                            ).strip()
                        except Exception:
                            # Fall back to non-highlighted code on any error
                            pass

                    # Format each line with line numbers and markers
                    current_line_no = start_line_idx + 1
                    for line_content in highlighted_code.splitlines():
                        line_content = line_content.rstrip()
                        is_error_line = current_line_no == frame_info.lineno

                        # Use error marker for the error line, space for others
                        marker = (
                            Styles.ErrorMarker(ERROR_LINE_MARKER)
                            if is_error_line
                            else ' '
                        )

                        # Format line number with consistent width
                        line_num_str = f'{current_line_no:>{4}}'

                        # Highlight the line number for the error line
                        line_num_styled = (
                            Styles.LineNo(line_num_str)
                            if is_error_line
                            else Styles.Muted(line_num_str)
                        )

                        # Make the error line bold
                        styled_line_content = (
                            Styles.Bold(line_content) if is_error_line else line_content
                        )

                        # Assemble the final line
                        code_context_lines.append(
                            f'  {marker} {line_num_styled} {LINE_SEPARATOR} {styled_line_content}'
                        )
                        current_line_no += 1
            except Exception:
                # If anything goes wrong, we'll fall back to the basic display below
                lines_available = False

        # Fallback if we couldn't get the source lines
        if not lines_available:
            if frame_info.line:
                # If we at least have the error line, show it
                # Format the line number first to ensure padding is applied
                # before adding ANSI styles so alignment isn't affected
                line_num_str = f'{frame_info.lineno:>4}'
                styled_line_num = Styles.LineNo(line_num_str)
                code_context_lines.append(
                    f'  {Styles.ErrorMarker(ERROR_LINE_MARKER)} {styled_line_num} {LINE_SEPARATOR} {Styles.Bold(frame_info.line)}'
                )
            else:
                # Otherwise show a message
                code_context_lines.append(
                    f'  {Styles.Muted("[Source code not available]")}'
                )

        return code_context_lines

    def _format_stack_transition(self, stack: Stack, term_width: int) -> List[str]:
        """Format the transition between exception stacks."""
        lines = []
        lines.append('')
        lines.append(Styles.Error(STACK_SEPARATOR * term_width))
        lines.append('')

        if stack.is_cause:
            lines.append(
                Styles.ErrorBold(
                    'The above exception was the direct cause of the following exception:'
                )
            )
        elif stack.is_context:
            lines.append(
                Styles.ErrorBold(
                    'During handling of the above exception, another exception occurred:'
                )
            )

        lines.append('')
        return lines

    def _render_traceback(self) -> Iterable[str]:
        """Render the complete traceback with all formatting and styling.

        This method orchestrates the rendering of the entire traceback, including
        all exception stacks, frames, code contexts, and local variables.

        Yields:
            Formatted lines for the complete traceback display
        """
        term_width = self.terminal_width
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield self._format_header(term_width, timestamp)
        yield ''

        # Process each exception stack in the trace
        for i, stack in enumerate(self.trace.stacks):
            # Handle transitions between exception stacks (for chained exceptions)
            if i > 0:
                for line in self._format_stack_transition(stack, term_width):
                    yield line

            # Show the exception message or syntax error
            if stack.syntax_error:
                # Special handling for syntax errors
                yield from self._format_syntax_error(stack.syntax_error)
            else:
                # Regular exception message
                yield self._format_exception_message(stack)

            # Add a blank line before frames if there are any
            if stack.frames:
                yield ''

            # Let the user know when max_frames dropped part of the stack.
            if stack.omitted_frames:
                yield ''
                yield Styles.Muted(
                    f'  ... {stack.omitted_frames} earlier frame(s) omitted '
                    f'(max_frames={self.max_frames})'
                )

            # Process each frame in the stack (in reverse order - most recent first)
            for frame_index, frame_info in enumerate(reversed(stack.frames)):
                # Frame header with file, line, and function information
                yield self._format_frame_header(frame_info)

                # Code context showing the source code around the error
                for line in self._format_code_context(frame_info):
                    yield line

                # Show local variables if requested and available
                if self.show_locals and frame_info.locals:
                    locals_lines = self._format_locals(frame_info.locals)
                    if locals_lines:
                        yield ''
                        yield f'  {Styles.LocalsHeader("Variables:")}'
                        yield from locals_lines

                # Add a separator between frames (except after the last frame)
                if frame_index < len(stack.frames) - 1:
                    yield ''
                    # Use a horizontal line as a separator
                    separator = Styles.Muted('  ' + '─' * (term_width - 4))
                    yield separator
                    yield ''

    # --- Output Methods ---
    def print(self, file: Any = None) -> None:
        """Print the formatted traceback to the specified file.

        This method renders the traceback and prints it to the specified file,
        with fallback to the original traceback if an error occurs.

        Args:
            file: The file object to print to (defaults to sys.stderr)
        """
        if file is None:
            file = sys.stderr

        try:
            # Print each line of the rendered traceback
            for line in self._render_traceback():
                print(line, file=file)
        except Exception as e:
            # If our formatter fails, fall back to the original traceback
            print(
                '\n'
                + Styles.ERROR_STYLE
                + '--- ERROR IN PRETTY TRACEBACK ---'
                + Styles.RESET,
                file=sys.stderr,
            )
            print(f'Formatter failed: {e}', file=sys.stderr)
            print('--- ORIGINAL TRACEBACK ---', file=sys.stderr)
            traceback.print_exception(
                self.exc_type, self.exc_value, self.tb, file=sys.stderr
            )

    @classmethod
    def from_exception(
        cls,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback_obj: Optional[TracebackType],
        **kwargs,
    ) -> 'PrettyTraceback':
        """Create a PrettyTraceback from exception info.

        This is a convenience classmethod for creating a PrettyTraceback
        from exception information, similar to sys.exc_info().

        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            traceback_obj: The traceback object.
            **kwargs: Additional arguments for PrettyTraceback.

        Returns:
            A new PrettyTraceback instance.

        Example:
            >>> try:
            ...     raise ValueError("example")
            ... except:
            ...     tb = PrettyTraceback.from_exception(*sys.exc_info())
            ...     tb.print()
        """
        return cls(exc_type, exc_value, traceback_obj, **kwargs)

    def is_suppressed(self, path: str) -> bool:
        """Check if a path should be suppressed from the traceback.

        Args:
            path: The file path to check.

        Returns:
            True if the path should be suppressed.
        """
        if not self.suppress:
            return False

        path_lower = path.lower()
        for suppress_path in self.suppress:
            if suppress_path.lower() in path_lower:
                return True
        return False

    def __str__(self) -> str:
        """Return rendered traceback as string."""
        return '\n'.join(self._render_traceback())

    def __repr__(self) -> str:
        """Return traceback representation."""
        exc_name = getattr(self.exc_type, '__name__', str(self.exc_type))
        return f'PrettyTraceback({exc_name}, show_locals={self.show_locals})'


# --- Installation Function ---
_original_excepthook: Optional[Callable] = None
_current_hook_options: Dict[str, Any] = {}


def pretty_excepthook(
    exc_type: Type[BaseException], exc_value: BaseException, tb: Optional[TracebackType]
) -> None:
    """Custom exception hook that displays a pretty traceback.

    This function is installed as sys.excepthook by the install() function.
    It creates a PrettyTraceback instance and prints it to stderr.

    Args:
        exc_type: The exception type
        exc_value: The exception value
        tb: The traceback object
    """
    global _current_hook_options
    PrettyTraceback(exc_type, exc_value, tb, **_current_hook_options).print(
        file=sys.stderr
    )


def install(
    *,
    extra_lines: int = DEFAULT_EXTRA_LINES,
    show_locals: bool = False,
    locals_max_string: int = MAX_VARIABLE_LENGTH,
    locals_max_depth: int = LOCALS_MAX_DEPTH,
    locals_hide_dunder: bool = True,
    locals_hide_sunder: bool = False,
    suppress: SuppressType = (),
    max_frames: int = 100,
    width: Optional[int] = None,
) -> Callable:
    """Install the pretty traceback handler as the default exception hook.

    This function replaces the default sys.excepthook with a custom handler that
    displays enhanced tracebacks with syntax highlighting and improved formatting.

    Args:
        extra_lines: Number of extra lines to show around the error line
        show_locals: Whether to show local variables in the traceback
        locals_max_string: Maximum length for string variables
        locals_max_depth: Maximum depth for nested structures
        locals_hide_dunder: Whether to hide dunder variables (__x__)
        locals_hide_sunder: Whether to hide single-underscore variables (_x)
        suppress: Path fragments whose frames are hidden (e.g. ``["site-packages"]``)
        max_frames: Maximum number of frames to show; extra frames are dropped
        width: Terminal width (auto-detected if None)

    Returns:
        The previous exception hook function

    Example:
        ```python
        from litprinter.traceback import install

        # Basic usage
        install()

        # With local variables and a shorter snippet
        install(show_locals=True, extra_lines=3)
        ```
    """
    global _original_excepthook, _current_hook_options
    previous_hook = sys.excepthook

    # Store the configuration options for the traceback handler
    # Store the configuration options for the traceback handler
    _current_hook_options = {
        'extra_lines': extra_lines,
        'show_locals': show_locals,
        'locals_max_string': locals_max_string,
        'locals_max_depth': locals_max_depth,
        'locals_hide_dunder': locals_hide_dunder,
        'locals_hide_sunder': locals_hide_sunder,
        'suppress': suppress,
        'max_frames': max_frames,
        'width': width,
    }

    # Install the hook if it is not already installed, and always report the
    # hook that was in place before this call (the documented return value).
    if previous_hook is not pretty_excepthook:
        _original_excepthook = previous_hook
        sys.excepthook = pretty_excepthook
    return previous_hook


def uninstall() -> None:
    """Uninstall the pretty traceback handler and restore the original exception hook.

    This function restores the original exception hook that was in place before
    the pretty traceback handler was installed.

    Example:
        ```python
        from litprinter.traceback import install, uninstall

        # Install the handler
        install(show_locals=True)

        # Do some work...

        # Restore the original handler when done
        uninstall()
        ```
    """
    global _original_excepthook, _current_hook_options

    # Only uninstall if our hook is currently installed and we have the original hook
    if _original_excepthook is not None and sys.excepthook is pretty_excepthook:
        # Restore the original hook
        sys.excepthook = _original_excepthook

        # Reset our state
        _original_excepthook = None
        _current_hook_options = {}

        print(
            Styles.Muted('LitPrinter traceback handler uninstalled.'), file=sys.stderr
        )


# Backwards-compatible alias
Traceback = PrettyTraceback
