#!/usr/bin/env python3
"""
LitPrinter Traceback Module

Enhanced traceback formatting with syntax highlighting and improved readability.
This module provides a more user-friendly traceback display with:
- Syntax highlighting using Pygments (if available)
- Local variable inspection
- Better visual formatting of error information
- Support for exception chaining
- Customizable themes

Usage:
    from litprinter.traceback import install
    install(show_locals=True, theme="cyberpunk")

    # Your code that might raise exceptions
    # ...

Author: OEvortex <helpingai5@gmail.com>
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
from types import TracebackType, FrameType, ModuleType, FunctionType, BuiltinFunctionType, MethodType
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    TypeAlias,
)

try:
    from types import ClassType
except ImportError:
    ClassType: TypeAlias = type

# --- Pygments Requirement & Style Imports ---
# We import all these Pygments components conditionally to support environments without Pygments
# The token imports are for custom style definitions that may be needed in the future
try:
    # pylint: disable=unused-import
    import pygments
    from pygments import highlight
    from pygments.lexers import guess_lexer_for_filename, PythonLexer, TextLexer
    from pygments.formatters import Terminal256Formatter
    from pygments.style import Style as PygmentsStyle
    from pygments.styles import get_style_by_name, get_all_styles
    from pygments.token import (
        Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
        Comment, Operator, Whitespace, Punctuation
    )
    from pygments.util import ClassNotFound
    # pylint: enable=unused-import
    HAS_PYGMENTS = True

    # Import style classes from coloring.py
    try:
        # Import all style classes and the create_custom_style function
        from .coloring import (
            JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI,
            SOLARIZED, NORD, GITHUB, VSCODE, MATERIAL, RETRO, OCEAN, AUTUMN,
            create_custom_style
        )

        # Mapping for custom style names to the imported classes
        CUSTOM_STYLES = {
            "jarvis": JARVIS,
            "rich": RICH,
            "modern": MODERN,
            "neon": NEON,
            "cyberpunk": CYBERPUNK,
            "dracula": DRACULA,
            "monokai": MONOKAI,
            "solarized": SOLARIZED,
            "nord": NORD,
            "github": GITHUB,
            "vscode": VSCODE,
            "material": MATERIAL,
            "retro": RETRO,
            "ocean": OCEAN,
            "autumn": AUTUMN,
        }
    except ImportError:
        # If coloring.py is not available, create an empty dictionary
        CUSTOM_STYLES = {}
        create_custom_style = None

except ImportError:
    # Pygments itself is not installed - create fallback stubs
    HAS_PYGMENTS = False
    PygmentsStyle = type
    Terminal256Formatter = None # type: ignore
    # pylint: disable=unused-argument
    def highlight(code, lexer, formatter): return code
    class PythonLexer: pass
    class TextLexer: pass
    class Terminal256FormatterFallback:
        def __init__(self, **kwargs): pass
    def get_style_by_name(name): return None
    def get_all_styles(): return []
    def guess_lexer_for_filename(filename, code): return TextLexer()
    # pylint: enable=unused-argument
    class ClassNotFound(Exception): pass
    CUSTOM_STYLES = {} # No pygments, no custom styles


# --- Configuration ---
# Maximum number of variables to display in locals
MAX_VARIABLES = 15
# Maximum length for variable representation
MAX_VARIABLE_LENGTH = 100
# Maximum depth for nested structures in locals
LOCALS_MAX_DEPTH = 2
# Default theme for syntax highlighting
DEFAULT_THEME = "cyberpunk"
# Number of extra lines to show around the error line
DEFAULT_EXTRA_LINES = 5
# Default terminal width if detection fails
DEFAULT_WIDTH = 100
# Separator for stack traces
STACK_SEPARATOR = "═"
# Marker for the error line
ERROR_LINE_MARKER = "❱"
# Marker for code line numbers
LINE_SEPARATOR = "│"

# --- ANSI Color Codes & Styles ---
# Handle both package import and direct script execution
try:
    # When imported as part of the package
    from .colors import Colors
except ImportError:
    # When run as a script
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    from litprinter.colors import Colors

class Styles:
    """Styling utilities for traceback formatting.

    This class provides methods for styling different parts of the traceback output
    using ANSI color codes from the Colors class.
    """
    # Use Colors class from colors.py for ANSI codes
    RESET = Colors.RESET
    BOLD = Colors.BOLD
    DIM = Colors.DIM
    ITALIC = Colors.ITALIC
    UNDERLINE = Colors.UNDERLINE
    RED = Colors.RED
    GREEN = Colors.GREEN
    YELLOW = Colors.YELLOW
    BLUE = Colors.BLUE
    MAGENTA = Colors.MAGENTA
    CYAN = Colors.CYAN
    WHITE = Colors.WHITE
    GREY = Colors.GRAY  # Note: Colors uses GRAY, not GREY

    @staticmethod
    def Muted(text: str) -> str: return Styles.GREY + str(text) + Styles.RESET
    @staticmethod
    def FilePath(text: str) -> str: return Styles.BLUE + str(text) + Styles.RESET
    @staticmethod
    def LineNo(text: str) -> str: return Styles.YELLOW + str(text) + Styles.RESET
    @staticmethod
    def FunctionName(text: str) -> str: return Styles.CYAN + str(text) + Styles.RESET
    @staticmethod
    def LibraryIndicator(text: str) -> str: return Styles.Muted(f"[{str(text)}]")
    @staticmethod
    def ModuleName(text: str) -> str: return Styles.Muted(f"{str(text)}")
    @staticmethod
    def Error(text: str) -> str: return Styles.RED + str(text) + Styles.RESET
    @staticmethod
    def ErrorBold(text: str) -> str: return Styles.BOLD + Styles.RED + str(text) + Styles.RESET
    @staticmethod
    def ErrorMarker(text: str) -> str: return Styles.ErrorBold(str(text))
    @staticmethod
    def LocalsHeader(text: str) -> str: return Styles.BOLD + Styles.WHITE + str(text) + Styles.RESET
    @staticmethod
    def LocalsKey(text: str) -> str: return Styles.MAGENTA + str(text) + Styles.RESET
    @staticmethod
    def LocalsEquals(text: str) -> str: return Styles.GREY + str(text) + Styles.RESET
    @staticmethod
    def LocalsValue(text: str) -> str: return Styles.WHITE + str(text) + Styles.RESET
    @staticmethod
    def ValueNone(text: str) -> str: return Styles.ITALIC + Styles.GREY + str(text) + Styles.RESET
    @staticmethod
    def ValueBool(text: str) -> str: return Styles.GREEN + str(text) + Styles.RESET
    @staticmethod
    def ValueStr(text: str) -> str: return Styles.YELLOW + str(text) + Styles.RESET
    @staticmethod
    def ValueNum(text: str) -> str: return Styles.BLUE + str(text) + Styles.RESET
    @staticmethod
    def ValueType(text: str) -> str: return Styles.CYAN + str(text) + Styles.RESET
    @staticmethod
    def ValueContainer(text: str) -> str: return Styles.MAGENTA + str(text) + Styles.RESET
    @staticmethod
    def Bold(text: str) -> str: return Styles.BOLD + str(text) + Styles.RESET
    @staticmethod
    def Italic(text: str) -> str: return Styles.ITALIC + str(text) + Styles.RESET
    @staticmethod
    def Dim(text: str) -> str: return Styles.DIM + str(text) + Styles.RESET
    @staticmethod
    def style(text: str, *styles_list: str) -> str:
        """Apply multiple styles to text."""
        if not text: return ""
        return "".join(styles_list) + str(text) + Styles.RESET
    @staticmethod
    def strip_styles(text: str) -> str:
        """Remove all ANSI style codes from text."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)

# --- Data Classes ---
@dataclass
class FrameInfo:
    """Information about a single frame in the traceback."""
    frame_obj: Optional[FrameType]  # The actual frame object
    filename: str                   # File where the frame is located
    lineno: int                     # Line number in the file
    name: str                       # Function name
    line: str = ""                  # Source code line
    locals: Optional[Dict[str, Any]] = None  # Local variables
    is_module_frame: bool = False   # Whether this is a module-level frame
    is_library_file: bool = False   # Whether this is from a library file

@dataclass
class _SyntaxError:
    """Information about a syntax error."""
    offset: Optional[int]  # Character offset where the error occurred
    filename: str          # File where the error occurred
    line: str              # Source code line with the error
    lineno: int            # Line number in the file
    msg: str               # Error message

@dataclass
class Stack:
    """Information about an exception stack."""
    exc_type: str          # Exception type name
    exc_value: str         # Exception value as string
    exc_type_full: str     # Full exception type
    syntax_error: Optional[_SyntaxError] = None  # Syntax error info if applicable
    is_cause: bool = False  # Whether this is a cause of another exception
    is_context: bool = False  # Whether this is a context of another exception
    frames: List[FrameInfo] = field(default_factory=list)  # Stack frames

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
    - Customizable themes

    Args:
        exc_type: The exception type
        exc_value: The exception value
        tb: The traceback object
        extra_lines: Number of extra lines to show around the error line
        theme: The syntax highlighting theme to use
        show_locals: Whether to show local variables
        locals_max_length: Maximum length for variable representation
        locals_max_string: Maximum length for string variables
        locals_max_depth: Maximum depth for nested structures
        locals_hide_dunder: Whether to hide dunder variables
        width: Terminal width (auto-detected if None)
        _selected_pygments_style_cls: Pre-selected Pygments style class
    """
    def __init__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        tb: Optional[TracebackType],
        *,
        extra_lines: int = DEFAULT_EXTRA_LINES,
        theme: str = DEFAULT_THEME,
        show_locals: bool = False,
        locals_max_length: int = MAX_VARIABLE_LENGTH,
        locals_max_string: int = MAX_VARIABLE_LENGTH,
        locals_max_depth: int = LOCALS_MAX_DEPTH,
        locals_hide_dunder: bool = True,
        width: Optional[int] = None,
        _selected_pygments_style_cls: Optional[Type[PygmentsStyle]] = None, # type: ignore
    ):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.tb = tb
        self.extra_lines = extra_lines
        self.theme_name = theme
        self.show_locals = show_locals
        self.locals_max_length = locals_max_length
        self.locals_max_string = locals_max_string
        self.locals_max_depth = locals_max_depth
        self.locals_hide_dunder = locals_hide_dunder
        self.terminal_width = width or self._get_terminal_width()
        self._pp = pprint.PrettyPrinter(depth=self.locals_max_depth, width=max(20, self.terminal_width - 20), compact=True)

        self.formatter = None
        self.style_cls = None
        if HAS_PYGMENTS:
            # Use the pre-selected style class if provided by install()
            if _selected_pygments_style_cls:
                self.style_cls = _selected_pygments_style_cls
            else: # Determine style class if running standalone
                self.style_cls = CUSTOM_STYLES.get(theme.lower())
                if not self.style_cls:
                    try: self.style_cls = get_style_by_name(theme)
                    except ClassNotFound:
                        self.theme_name = DEFAULT_THEME
                        self.style_cls = CUSTOM_STYLES.get(DEFAULT_THEME.lower()) or get_style_by_name('default')

            # Pass the CLASS to the formatter
            if self.style_cls and Terminal256Formatter:
                try: self.formatter = Terminal256Formatter(style=self.style_cls)
                except Exception:
                     self.formatter = None
                     # Log error silently - we'll fall back to non-highlighted output

        self.trace = self._extract_trace()

    # --- Helper methods (_get_terminal_width, etc. - remain the same) ---
    @staticmethod
    def _get_terminal_width() -> int:
        try: width = shutil.get_terminal_size(fallback=(DEFAULT_WIDTH, 20)).columns; return max(40, width)
        except Exception: return DEFAULT_WIDTH
    @staticmethod
    def _safe_str(obj: Any) -> str:
        try: return str(obj)
        except Exception: return "<exception str() failed>"
    @staticmethod
    def _is_library_file(filename: str) -> bool:
        if not filename or '<' in filename or '>' in filename: return False
        try:
            abs_path = os.path.abspath(filename); stdlib_dir = os.path.dirname(os.__file__)
            site_packages_dirs = [p for p in sys.path if 'site-packages' in p or 'dist-packages' in p]
            if stdlib_dir and abs_path.startswith(stdlib_dir): return True
            if any(abs_path.startswith(p) for p in site_packages_dirs): return True
        except Exception: pass
        return False
    @staticmethod
    def _is_skippable_local(key: str, value: Any, frame_is_module: bool, locals_hide_dunder: bool) -> bool:
        if locals_hide_dunder and key.startswith("__") and key.endswith("__"): return True
        if frame_is_module:
            if isinstance(value, (ModuleType, FunctionType, ClassType, BuiltinFunctionType, MethodType, Type)): return True
            # Update skip list: Remove explicit style names, keep base class names
            if key in ("PrettyTraceback", "FrameInfo", "_SyntaxError", "Stack", "Trace", "Styles", "install", "uninstall",
                       "PygmentsStyle", "CUSTOM_STYLES"): return True # Remove JARVIS, RICH etc.
        return False

    # --- Trace Extraction (_extract_trace, _extract_single_frame - remain the same) ---
    def _extract_trace(self) -> Trace:
        stacks: List[Stack] = []; current_exc_type = self.exc_type; current_exc_value = self.exc_value; current_tb = self.tb
        processed_exceptions = set()
        while current_exc_type is not None and current_exc_value is not None:
            exception_id = id(current_exc_value)
            if exception_id in processed_exceptions: print("WARNING: Detected cycle in exception chain.", file=sys.stderr); break
            processed_exceptions.add(exception_id)
            is_cause = bool(stacks and getattr(stacks[-1].exc_value, '__cause__', None) is current_exc_value)
            suppress_ctx = getattr(stacks[-1].exc_value, '__suppress_context__', False) if stacks else False
            is_context = bool(stacks and getattr(stacks[-1].exc_value, '__context__', None) is current_exc_value and not suppress_ctx)
            stack = Stack(exc_type=self._safe_str(current_exc_type.__name__), exc_value=self._safe_str(current_exc_value), exc_type_full=str(current_exc_type), is_cause=is_cause, is_context=is_context)
            if isinstance(current_exc_value, SyntaxError): stack.syntax_error = _SyntaxError(offset=current_exc_value.offset, filename=current_exc_value.filename or "?", lineno=current_exc_value.lineno or 0, line=current_exc_value.text or "", msg=current_exc_value.msg)
            extracted_frames: List[FrameInfo] = []
            if current_tb is not None:
                try:
                    is_first = True
                    for frame_obj, lineno in traceback.walk_tb(current_tb):
                        is_module = is_first and (not frame_obj.f_back); extracted_frames.append(self._extract_single_frame(frame_obj, lineno, is_module)); is_first = False
                    stack.frames = extracted_frames
                except Exception as e: print(f"ERROR: Could not extract frames using walk_tb: {e}", file=sys.stderr)
            linecache.clearcache(); stacks.append(stack)
            next_cause = getattr(current_exc_value, "__cause__", None); next_context = getattr(current_exc_value, "__context__", None); next_suppress_context = getattr(current_exc_value, "__suppress_context__", False)
            if next_cause is not None: next_exc_value = next_cause
            elif next_context is not None and not next_suppress_context: next_exc_value = next_context
            else: next_exc_value = None
            if next_exc_value is not None: current_exc_value = next_exc_value; current_exc_type = type(current_exc_value); current_tb = current_exc_value.__traceback__
            else: current_exc_type, current_exc_value, current_tb = None, None, None
        return Trace(stacks=list(reversed(stacks)))

    def _extract_single_frame(self, frame_obj: FrameType, lineno: int, is_module: bool) -> FrameInfo:
         f_code = frame_obj.f_code; filename = f_code.co_filename or "?"; func_name = f_code.co_name or "?"; is_lib = self._is_library_file(filename)
         linecache.checkcache(filename); line = linecache.getline(filename, lineno, frame_obj.f_globals).strip()
         frame_locals_filtered = None
         if self.show_locals:
            frame_locals_unfiltered = frame_obj.f_locals
            frame_locals_filtered = { k: v for k, v in frame_locals_unfiltered.items() if not self._is_skippable_local(k, v, is_module, self.locals_hide_dunder) }
         return FrameInfo(frame_obj=frame_obj, filename=filename, lineno=lineno, name=func_name, line=line, locals=frame_locals_filtered, is_module_frame=is_module, is_library_file=is_lib)

    # --- Formatting Helpers (_color_code_value, etc. - remain the same) ---
    def _color_code_value(self, value_repr: str) -> str:
        val = value_repr.strip()
        if val == "None": return Styles.ValueNone(val)
        if val == "True" or val == "False": return Styles.ValueBool(val)
        if (val.startswith("'") and val.endswith("'")) or \
           (val.startswith('"') and val.endswith('"')): return Styles.ValueStr(val)
        if val.isdigit() or (val.startswith("-") and val[1:].isdigit()): return Styles.ValueNum(val)
        try: float(val); return Styles.ValueNum(val)
        except ValueError: pass
        if val.startswith("<class ") or val.startswith("<function "): return Styles.ValueType(val)
        if val.startswith("<module ") or val.startswith("<bound method "): return Styles.ValueType(val)
        if val.startswith("{") or val.startswith("[") or val.startswith("("): return Styles.ValueContainer(val)
        if val.startswith("<") and val.endswith(">"): return Styles.ValueContainer(val)
        return Styles.LocalsValue(val)
    def _format_locals(self, locals_dict: Dict[str, Any]) -> List[str]:
        if not locals_dict: return []
        formatted_vars = []; sorted_items = sorted(locals_dict.items()); count = 0
        for name, value in sorted_items:
            if count >= MAX_VARIABLES: formatted_vars.append((Styles.Dim("..."), Styles.Dim(f"<{len(sorted_items) - count} more variables>"))); break
            try:
                value_repr = self._pp.pformat(value)
                if len(value_repr) > self.locals_max_string: value_repr = value_repr[:self.locals_max_string - 1] + "…"
            except Exception: value_repr = Styles.Error("<exception repr() failed>")
            colored_value = self._color_code_value(value_repr); formatted_vars.append((Styles.LocalsKey(name), colored_value)); count += 1
        lines = []; num_vars = len(formatted_vars); mid_point = (num_vars + 1) // 2; col1_width = 0
        if num_vars > 0:
             try: col1_width = max(len(Styles.strip_styles(k)) for k, _ in formatted_vars[:mid_point]) + 3
             except ValueError: col1_width = 3
        for i in range(mid_point):
            key1, val1 = formatted_vars[i]; key1_clean_len = len(Styles.strip_styles(key1)); key1_padded = key1 + " " * max(0, col1_width - key1_clean_len - 3); line = f"  {key1_padded} {Styles.LocalsEquals('=')} {val1}"
            j = i + mid_point
            if j < num_vars: key2, val2 = formatted_vars[j]; line += f"    {Styles.LocalsKey(key2)} {Styles.LocalsEquals('=')} {val2}"
            lines.append(line)
        return lines
    def _format_syntax_error(self, error: _SyntaxError) -> Iterable[str]:
        yield ""; yield Styles.ErrorBold(f"Syntax Error in {Styles.FilePath(error.filename)} at line {Styles.LineNo(str(error.lineno))}:"); yield ""
        yield f"  {error.line.rstrip()}"
        if error.offset is not None and error.offset > 0: marker_pos = error.offset - 1; yield f"  {' ' * marker_pos}{Styles.ErrorBold('^')}"
        yield ""; yield Styles.Error(error.msg)
    def _format_exception_message(self, stack: Stack) -> str: return f"{Styles.ErrorBold(stack.exc_type)}: {Styles.Error(stack.exc_value)}"

    # --- Main Rendering Logic ---
    def _format_frame_header(self, frame_info: FrameInfo) -> str:
        """Format the header line for a stack frame."""
        file_info = Styles.FilePath(frame_info.filename)
        line_info = Styles.LineNo(str(frame_info.lineno))
        func_info = Styles.FunctionName(frame_info.name)
        module_name = frame_info.frame_obj.f_globals.get('__name__', '') if frame_info.frame_obj else ''
        module_info_styled = Styles.ModuleName(module_name) if module_name else ""
        lib_indicator = Styles.LibraryIndicator("Library") if frame_info.is_library_file else ""
        return f"  File \"{file_info}\", line {line_info}, in {func_info} {module_info_styled} {lib_indicator}"

    def _format_code_context(self, frame_info: FrameInfo) -> List[str]:
        """Format the code context for a stack frame."""
        code_context_lines = []
        lines_available = False

        if frame_info.filename != "?" and frame_info.lineno > 0:
            lines_for_snippet = linecache.getlines(frame_info.filename)
            if lines_for_snippet:
                lines_available = True
                start_line_idx = max(0, frame_info.lineno - 1 - self.extra_lines)
                end_line_idx = min(len(lines_for_snippet), frame_info.lineno + self.extra_lines)
                code_snippet = "".join(lines_for_snippet[start_line_idx:end_line_idx])
                highlighted_code = code_snippet

                if HAS_PYGMENTS and self.formatter:
                    lexer = TextLexer()
                    if frame_info.filename != "<string>" and not frame_info.filename.startswith('<'):
                        try:
                            lexer = guess_lexer_for_filename(frame_info.filename, code_snippet)
                        except ClassNotFound:
                            pass
                    else:
                        lexer = PythonLexer()

                    try:
                        highlighted_code = highlight(code_snippet, lexer, self.formatter).strip()
                    except Exception:
                        # Fall back to non-highlighted code
                        pass

                current_line_no = start_line_idx + 1
                for line_content in highlighted_code.splitlines():
                    line_content = line_content.rstrip()
                    is_error_line = (current_line_no == frame_info.lineno)
                    marker = Styles.ErrorMarker(ERROR_LINE_MARKER) if is_error_line else " "
                    line_num_str = f"{current_line_no:>{4}}"
                    line_num_styled = Styles.LineNo(line_num_str) if is_error_line else Styles.Muted(line_num_str)
                    styled_line_content = Styles.Bold(line_content) if is_error_line else line_content
                    code_context_lines.append(
                        f"  {marker} {line_num_styled} {LINE_SEPARATOR} {styled_line_content}"
                    )
                    current_line_no += 1

        if not lines_available:
            if frame_info.line:
                code_context_lines.append(
                    f"  {Styles.ErrorMarker(ERROR_LINE_MARKER)} {Styles.LineNo(str(frame_info.lineno)):>{4}} {LINE_SEPARATOR} {Styles.Bold(frame_info.line)}"
                )
            else:
                code_context_lines.append(f"  {Styles.Muted('[Source code not available]')}")

        return code_context_lines

    def _format_stack_transition(self, stack: Stack, term_width: int) -> List[str]:
        """Format the transition between exception stacks."""
        lines = []
        lines.append("")
        lines.append(Styles.Error(STACK_SEPARATOR * term_width))
        lines.append("")

        if stack.is_cause:
            lines.append(Styles.ErrorBold("The above exception was the direct cause of the following exception:"))
        elif stack.is_context:
            lines.append(Styles.ErrorBold("During handling of the above exception, another exception occurred:"))

        lines.append("")
        return lines

    def _render_traceback(self) -> Iterable[str]:
        """Render the complete traceback."""
        term_width = self.terminal_width
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield Styles.Muted(f"Traceback captured at {timestamp}")
        yield ""

        for i, stack in enumerate(self.trace.stacks):
            # Handle stack transitions
            if i > 0:
                for line in self._format_stack_transition(stack, term_width):
                    yield line

            # Show the exception message
            if stack.syntax_error:
                yield from self._format_syntax_error(stack.syntax_error)
            else:
                yield self._format_exception_message(stack)

            if stack.frames:
                yield ""

            # Process each frame in the stack
            for frame_index, frame_info in enumerate(reversed(stack.frames)):
                # Frame header
                yield self._format_frame_header(frame_info)

                # Code context
                for line in self._format_code_context(frame_info):
                    yield line

                # Local variables
                if self.show_locals and frame_info.locals:
                    locals_lines = self._format_locals(frame_info.locals)
                    if locals_lines:
                        yield ""
                        yield f"  {Styles.LocalsHeader('Variables:')}"
                        yield from locals_lines

                # Separator between frames
                if frame_index < len(stack.frames) - 1:
                    yield ""
                    yield Styles.Muted("  " + "─" * (term_width - 4))
                    yield ""

    # --- print method (remains the same) ---
    def print(self, file: Any = None) -> None:
        if file is None: file = sys.stderr
        try:
            for line in self._render_traceback(): print(line, file=file)
        except Exception as e:
            print("\n--- ERROR IN PRETTY TRACEBACK ---", file=sys.stderr); print(f"Formatter failed: {e}", file=sys.stderr)
            print("--- ORIGINAL TRACEBACK ---", file=sys.stderr); traceback.print_exception(self.exc_type, self.exc_value, self.tb, file=sys.stderr)

# --- Installation Function ---
_original_excepthook: Optional[Callable] = None
_current_hook_options: Dict[str, Any] = {}

def pretty_excepthook(exc_type: Type[BaseException], exc_value: BaseException, tb: Optional[TracebackType]) -> None:
    """Custom exception hook that displays a pretty traceback.

    This function is installed as sys.excepthook by the install() function.
    It creates a PrettyTraceback instance and prints it to stderr.

    Args:
        exc_type: The exception type
        exc_value: The exception value
        tb: The traceback object
    """
    global _current_hook_options
    PrettyTraceback(exc_type, exc_value, tb, **_current_hook_options).print(file=sys.stderr)

def install(
    *,
    extra_lines: int = DEFAULT_EXTRA_LINES,
    theme: str = DEFAULT_THEME,
    show_locals: bool = False,
    locals_max_length: int = MAX_VARIABLE_LENGTH,
    locals_max_string: int = MAX_VARIABLE_LENGTH,
    locals_max_depth: int = LOCALS_MAX_DEPTH,
    locals_hide_dunder: bool = True,
    width: Optional[int] = None,
) -> Callable:
    """Install the pretty traceback handler as the default exception hook.

    Args:
        extra_lines: Number of extra lines to show around the error line
        theme: The syntax highlighting theme to use
        show_locals: Whether to show local variables
        locals_max_length: Maximum length for variable representation
        locals_max_string: Maximum length for string variables
        locals_max_depth: Maximum depth for nested structures
        locals_hide_dunder: Whether to hide dunder variables
        width: Terminal width (auto-detected if None)

    Returns:
        The previous exception hook function
    """
    global _original_excepthook, _current_hook_options
    previous_hook = sys.excepthook

    # --- Determine Pygments Style CLASS ---
    selected_style_cls = None
    actual_theme_name = theme
    if HAS_PYGMENTS:
        theme_lower = theme.lower()
        # Use CUSTOM_STYLES dictionary which relies on imported classes
        selected_style_cls = CUSTOM_STYLES.get(theme_lower)
        if not selected_style_cls:
            try:
                # IMPORTANT: get_style_by_name returns the CLASS, not an instance
                selected_style_cls = get_style_by_name(theme)
            except ClassNotFound:
                print(f"WARNING: Pygments style '{theme}' not found. Using '{DEFAULT_THEME}'.", file=sys.stderr)
                actual_theme_name = DEFAULT_THEME
                # Fallback logic using CUSTOM_STYLES and get_style_by_name
                selected_style_cls = CUSTOM_STYLES.get(DEFAULT_THEME.lower())
                if not selected_style_cls:
                    try:
                        selected_style_cls = get_style_by_name('default')
                    except ClassNotFound:
                        # Try to create a custom style if coloring.py is available
                        if 'create_custom_style' in globals() and create_custom_style is not None:
                            # Create a simple default style with basic colors
                            from pygments.token import Text
                            selected_style_cls = create_custom_style('DefaultStyle', {Text: '#ffffff'})
                        else:
                            selected_style_cls = None  # Should not happen


    _current_hook_options = {
        "extra_lines": extra_lines, "theme": actual_theme_name, "show_locals": show_locals,
        "locals_max_length": locals_max_length, "locals_max_string": locals_max_string,
        "locals_max_depth": locals_max_depth, "locals_hide_dunder": locals_hide_dunder,
        "width": width,
        "_selected_pygments_style_cls": selected_style_cls # Pass the determined CLASS
    }

    if previous_hook is not pretty_excepthook:
         _original_excepthook = previous_hook
         sys.excepthook = pretty_excepthook
         return _original_excepthook
    else:
        return pretty_excepthook

def uninstall() -> None:
    """Uninstall the pretty traceback handler and restore the original exception hook.

    This function restores the original exception hook that was in place before
    the pretty traceback handler was installed.
    """
    global _original_excepthook, _current_hook_options
    if _original_excepthook is not None and sys.excepthook is pretty_excepthook:
        sys.excepthook = _original_excepthook
        _original_excepthook = None
        _current_hook_options = {}

# --- Example Usage ---
if __name__ == "__main__":
    # Install using the default theme ("modern" as set above)
    install(show_locals=True)
    # Or explicitly: install(show_locals=True, theme="modern")
    # Or try others: install(show_locals=True, theme="jarvis") # If coloring.py is correct

    def inner_function(a, b):
        # These variables are intentionally defined but not used
        # They're here to demonstrate the locals display in the traceback
        _ = {"key": "value", "num": 123.45, "bool": True}
        _ = "abcdefghijklmnopqrstuvwxyz" * 5
        return a / b

    def my_buggy_function(c):
        x = 10; y = 0
        # These variables are intentionally defined but not used
        # They're here to demonstrate the locals display in the traceback
        _ = "hello"
        _ = [10, 20, 30, None, list(range(8))]
        _ = {"one": 1, "two": None}
        print("About to call inner function...") # This will print
        result = inner_function(x * c, y) # This will raise ZeroDivisionError
        print(f"Result was: {result}") # This won't

    try: my_buggy_function(5)
    except ZeroDivisionError as e:
        raise ValueError("Calculation failed due to division issue") from e

    # try: eval("x = 1 +")
    # except Exception: pass