#!/usr/bin/env python3
"""
LitPrinter Console Module

Provides a Console class for rich terminal output with styling, markup support,
and various output methods. Inspired by Rich's Console class.

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

import builtins
import io
import os
import re
import shutil
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    TYPE_CHECKING,
)

from .colors import Colors
from .segment import Segment, ControlCode, ControlType
from .style import Style
from .text import Text

if TYPE_CHECKING:
    pass


# Regular expression to match Rich-style markup like [red]text[/red]
_MARKUP_RE = re.compile(r"\[(/)?([^\]]+)\]")

# Mapping of color/style names to ANSI codes
_STYLE_MAP = {name.lower(): getattr(Colors, name) for name in dir(Colors) if name.isupper()}


@dataclass
class ConsoleDimensions:
    """Represents console dimensions."""
    width: int
    height: int


@dataclass
class ConsoleOptions:
    """Options for console rendering."""
    max_width: int = 80
    min_width: int = 1
    height: int = 25
    encoding: str = "utf-8"
    is_terminal: bool = True
    no_color: bool = False
    legacy_windows: bool = False
    markup: bool = True
    highlight: bool = True
    justify: Optional[str] = None
    overflow: str = "fold"
    no_wrap: bool = False


class Console:
    """A class for rich terminal output with styling and markup support.
    
    The Console class provides methods for printing styled text, logging,
    and various terminal operations. It supports Rich-style markup syntax
    for easy text styling.
    
    Example:
        >>> console = Console()
        >>> console.print("[bold red]Error:[/bold red] Something went wrong!")
        >>> console.log("Processing started", log_locals=True)
        >>> console.rule("Section Header")
    
    Attributes:
        file: The file to write output to.
        force_terminal: Override terminal detection.
        no_color: Disable all color output.
        tab_size: Size of tab characters.
        record: Whether to record output.
        markup: Whether to parse markup.
        emoji: Whether to render emoji codes.
        highlight: Whether to auto-highlight content.
        log_time: Whether to show time in log.
        log_path: Whether to show path in log.
        width: Override console width.
        height: Override console height.
        style: Default style for output.
        quiet: Suppress all output.
    """
    
    def __init__(
        self,
        *,
        color_system: Optional[str] = "auto",
        force_terminal: Optional[bool] = None,
        no_color: bool = False,
        tab_size: int = 8,
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        highlight: bool = True,
        log_time: bool = True,
        log_path: bool = True,
        log_time_format: str = "[%X]",
        width: Optional[int] = None,
        height: Optional[int] = None,
        style: Optional[str] = None,
        file: Optional[IO[str]] = None,
        quiet: bool = False,
        soft_wrap: bool = False,
    ):
        """Initialize a Console.
        
        Args:
            color_system: Color system to use ("auto", "standard", "256", "truecolor", "windows", None).
            force_terminal: Force terminal mode.
            no_color: Disable all colors.
            tab_size: Tab character width.
            record: Record all output for later export.
            markup: Parse Rich-style markup.
            emoji: Render emoji codes like :smile:.
            highlight: Auto-highlight content.
            log_time: Show time in log output.
            log_path: Show file/line in log output.
            log_time_format: Time format for logging.
            width: Override console width.
            height: Override console height.
            style: Default style for output.
            file: File to write to (default: stdout).
            quiet: Suppress all output.
            soft_wrap: Enable soft wrapping.
        """
        self._file = file
        self.color_system = color_system
        self.force_terminal = force_terminal
        self.no_color = no_color or os.environ.get("NO_COLOR") is not None
        self.tab_size = tab_size
        self.record = record
        self.markup = markup
        self.emoji = emoji
        self.highlight = highlight
        self.log_time = log_time
        self.log_path = log_path
        self.log_time_format = log_time_format
        self._width = width
        self._height = height
        self.style = style
        self.quiet = quiet
        self.soft_wrap = soft_wrap
        
        # Recording buffer
        self._record_buffer: List[Segment] = []
        
        # Get terminal size
        self._terminal_size: Optional[Tuple[int, int]] = None
    
    @property
    def file(self) -> IO[str]:
        """Get the output file."""
        return self._file or sys.stdout
    
    @property
    def size(self) -> ConsoleDimensions:
        """Get the console dimensions."""
        if self._terminal_size is None:
            self._terminal_size = self._detect_size()
        width, height = self._terminal_size
        return ConsoleDimensions(
            width=self._width or width,
            height=self._height or height,
        )
    
    @property
    def width(self) -> int:
        """Get the console width."""
        return self.size.width
    
    @property
    def height(self) -> int:
        """Get the console height."""
        return self.size.height
    
    @property
    def is_terminal(self) -> bool:
        """Check if output is a terminal."""
        if self.force_terminal is not None:
            return self.force_terminal
        try:
            return self.file.isatty()
        except Exception:
            return False
    
    @property
    def encoding(self) -> str:
        """Get the output encoding."""
        try:
            return self.file.encoding or "utf-8"
        except Exception:
            return "utf-8"
    
    def _detect_size(self) -> Tuple[int, int]:
        """Detect terminal size."""
        try:
            size = shutil.get_terminal_size(fallback=(80, 25))
            return size.columns, size.lines
        except Exception:
            return 80, 25
    
    def _parse_markup(self, text: str) -> str:
        """Parse Rich-style markup in text and return ANSI formatted string.
        
        Args:
            text: Text with markup tags like [red]...[/red].
            
        Returns:
            Text with ANSI escape codes.
        """
        if not self.markup:
            return text
        
        result: List[str] = []
        stack: List[str] = []
        pos = 0
        
        for match in _MARKUP_RE.finditer(text):
            # Add text before the match
            result.append(text[pos:match.start()])
            
            closing, tag = match.groups()
            tag = tag.lower().strip() if tag else ""
            
            if closing:
                # Closing tag
                if stack and stack[-1] == tag:
                    stack.pop()
                    result.append(Colors.RESET)
                elif tag == "" and stack:
                    # [/] closes all
                    while stack:
                        stack.pop()
                        result.append(Colors.RESET)
                else:
                    # Unmatched closing tag, keep literal
                    result.append(match.group(0))
            else:
                # Opening tag
                ansi = self._get_style_code(tag)
                if ansi:
                    stack.append(tag)
                    result.append(ansi)
                else:
                    # Unknown tag, keep literal
                    result.append(match.group(0))
            
            pos = match.end()
        
        # Add remaining text
        result.append(text[pos:])
        
        # Close any remaining open tags
        while stack:
            stack.pop()
            result.append(Colors.RESET)
        
        return "".join(result)
    
    def _get_style_code(self, style: str) -> str:
        """Get ANSI code(s) for a style string.
        
        Args:
            style: Style string like "bold red" or "red on white".
            
        Returns:
            Combined ANSI codes.
        """
        parts = style.split()
        codes = []
        
        for part in parts:
            # Check direct style map
            if part in _STYLE_MAP:
                codes.append(_STYLE_MAP[part])
            # Check for "on_" prefix for background
            elif part.startswith("on_"):
                bg_color = part[3:]
                bg_key = f"bg_{bg_color}"
                if bg_key in _STYLE_MAP:
                    codes.append(_STYLE_MAP[bg_key])
            # Check for hex color
            elif part.startswith("#"):
                try:
                    codes.append(Colors.from_hex(part))
                except ValueError:
                    pass
        
        return "".join(codes)
    
    def print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[str] = None,
        justify: Optional[str] = None,
        overflow: Optional[str] = None,
        no_wrap: bool = False,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        width: Optional[int] = None,
        crop: bool = True,
        soft_wrap: bool = False,
        new_line_start: bool = False,
    ) -> None:
        """Print styled output to the console.
        
        This is the main method for outputting styled text. It supports
        Rich-style markup like [bold red]text[/bold red].
        
        Args:
            *objects: Objects to print.
            sep: Separator between objects.
            end: String to append at end.
            style: Style to apply to all output.
            justify: Text justification ("left", "center", "right", "full").
            overflow: Overflow handling ("fold", "crop", "ellipsis").
            no_wrap: Disable text wrapping.
            emoji: Override emoji handling.
            markup: Override markup parsing.
            highlight: Override highlighting.
            width: Width for output.
            crop: Crop to console width.
            soft_wrap: Enable soft wrapping.
            new_line_start: Add newline at start.
        """
        if self.quiet:
            return
        
        # Convert objects to strings
        str_objects = []
        for obj in objects:
            if isinstance(obj, (Segment, Text)):
                str_objects.append(str(obj))
            elif not isinstance(obj, str):
                str_objects.append(str(obj))
            else:
                str_objects.append(obj)
        
        text = sep.join(str_objects)
        
        # Parse markup if enabled
        should_markup = markup if markup is not None else self.markup
        if should_markup:
            text = self._parse_markup(text)
        
        # Apply style if provided
        if style:
            style_code = self._get_style_code(style)
            if style_code:
                text = f"{style_code}{text}{Colors.RESET}"
        elif self.style:
            style_code = self._get_style_code(self.style)
            if style_code:
                text = f"{style_code}{text}{Colors.RESET}"
        
        # Handle new line start
        output = ""
        if new_line_start:
            output = "\n"
        
        output += text + end
        
        # Write output
        try:
            self.file.write(output)
            self.file.flush()
        except Exception:
            pass
        
        # Record if enabled
        if self.record:
            self._record_buffer.append(Segment(text))
    
    def print_json(
        self,
        data: Any = None,
        *,
        json: Optional[str] = None,
        indent: int = 2,
        highlight: bool = True,
        skip_keys: bool = False,
        ensure_ascii: bool = False,
        sort_keys: bool = False,
        default: Optional[Callable[[Any], Any]] = None,
    ) -> None:
        """Print JSON with syntax highlighting.
        
        Args:
            data: Data to format as JSON.
            json: Pre-formatted JSON string.
            indent: Number of spaces for indentation.
            highlight: Apply syntax highlighting.
            skip_keys: Skip keys that are not basic types.
            ensure_ascii: Escape non-ASCII characters.
            sort_keys: Sort dictionary keys.
            default: Default function for non-serializable objects.
        """
        import json as json_module
        
        if json is not None:
            json_str = json
        elif data is not None:
            json_str = json_module.dumps(
                data,
                indent=indent,
                skip_keys=skip_keys,
                ensure_ascii=ensure_ascii,
                sort_keys=sort_keys,
                default=default,
            )
        else:
            raise ValueError("Either 'data' or 'json' must be provided")
        
        if highlight:
            # Simple JSON highlighting
            # Strings in quotes
            json_str = re.sub(
                r'("(?:[^"\\]|\\.)*")',
                lambda m: f"{Colors.GREEN}{m.group(0)}{Colors.RESET}",
                json_str,
            )
            # Numbers
            json_str = re.sub(
                r'\b(\d+(?:\.\d+)?)\b',
                lambda m: f"{Colors.CYAN}{m.group(0)}{Colors.RESET}",
                json_str,
            )
            # Keywords
            for keyword in ["true", "false", "null"]:
                json_str = json_str.replace(
                    keyword,
                    f"{Colors.MAGENTA}{keyword}{Colors.RESET}",
                )
        
        self.print(json_str, markup=False)
    
    def log(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[str] = None,
        justify: Optional[str] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        log_locals: bool = False,
        _stack_offset: int = 1,
    ) -> None:
        """Log output with timestamp and location.
        
        Similar to print() but adds timestamp and optionally the calling
        location and local variables.
        
        Args:
            *objects: Objects to log.
            sep: Separator between objects.
            end: String to append at end.
            style: Style to apply.
            justify: Text justification.
            emoji: Override emoji handling.
            markup: Override markup parsing.
            highlight: Override highlighting.
            log_locals: Display local variables.
            _stack_offset: Stack frame offset for location.
        """
        if self.quiet:
            return
        
        parts = []
        
        # Add timestamp
        if self.log_time:
            timestamp = datetime.now().strftime(self.log_time_format)
            parts.append(f"{Colors.DIM}{timestamp}{Colors.RESET}")
        
        # Add location
        if self.log_path:
            import inspect
            frame = inspect.stack()[_stack_offset]
            filename = os.path.basename(frame.filename)
            lineno = frame.lineno
            parts.append(f"{Colors.CYAN}{filename}{Colors.RESET}:{Colors.YELLOW}{lineno}{Colors.RESET}")
        
        # Add separator
        if parts:
            prefix = " ".join(parts) + " "
        else:
            prefix = ""
        
        # Convert objects
        str_objects = [str(obj) if not isinstance(obj, str) else obj for obj in objects]
        text = sep.join(str_objects)
        
        # Parse markup
        should_markup = markup if markup is not None else self.markup
        if should_markup:
            text = self._parse_markup(text)
        
        # Apply style
        if style:
            style_code = self._get_style_code(style)
            if style_code:
                text = f"{style_code}{text}{Colors.RESET}"
        
        output = f"{prefix}{text}"
        
        # Add local variables
        if log_locals:
            import inspect
            frame = inspect.stack()[_stack_offset]
            local_vars = frame.frame.f_locals
            if local_vars:
                output += f"\n{Colors.DIM}Local variables:{Colors.RESET}\n"
                for key, value in local_vars.items():
                    if not key.startswith("_"):
                        try:
                            value_repr = repr(value)[:100]
                        except Exception:
                            value_repr = "<error>"
                        output += f"  {Colors.MAGENTA}{key}{Colors.RESET} = {value_repr}\n"
        
        output += end
        
        try:
            self.file.write(output)
            self.file.flush()
        except Exception:
            pass
    
    def rule(
        self,
        title: str = "",
        *,
        characters: str = "─",
        style: str = "dim",
        align: str = "center",
    ) -> None:
        """Draw a horizontal rule with optional title.
        
        Args:
            title: Optional title to embed in the rule.
            characters: Character(s) to draw the rule with.
            style: Style for the rule.
            align: Title alignment ("left", "center", "right").
        """
        if self.quiet:
            return
        
        width = self.width
        style_code = self._get_style_code(style) if style else ""
        reset = Colors.RESET if style_code else ""
        
        if not title:
            rule_line = characters * width
        else:
            title_with_space = f" {title} "
            remaining = width - len(title_with_space)
            
            if align == "left":
                left_part = characters * 2
                right_part = characters * (remaining - 2)
            elif align == "right":
                left_part = characters * (remaining - 2)
                right_part = characters * 2
            else:  # center
                left_len = remaining // 2
                right_len = remaining - left_len
                left_part = characters * left_len
                right_part = characters * right_len
            
            rule_line = f"{left_part}{title_with_space}{right_part}"
        
        output = f"{style_code}{rule_line}{reset}\n"
        
        try:
            self.file.write(output)
            self.file.flush()
        except Exception:
            pass
    
    @contextmanager
    def status(
        self,
        status: str,
        *,
        spinner: str = "dots",
        spinner_style: str = "cyan",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ) -> Iterator[None]:
        """Display a status message with optional spinner.
        
        Args:
            status: Status message to display.
            spinner: Spinner animation type.
            spinner_style: Style for the spinner.
            speed: Animation speed.
            refresh_per_second: Refresh rate.
            
        Yields:
            Context for the status display.
        """
        # Simple implementation - just print the status
        spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        style_code = self._get_style_code(spinner_style) if spinner_style else ""
        reset = Colors.RESET if style_code else ""
        
        self.print(f"{style_code}●{reset} {status}...")
        try:
            yield
        finally:
            self.print(f"{Colors.GREEN}✓{Colors.RESET} {status} - done")
    
    def input(
        self,
        prompt: str = "",
        *,
        markup: bool = True,
        emoji: bool = True,
        password: bool = False,
        stream: Optional[IO[str]] = None,
    ) -> str:
        """Get input from the user with styled prompt.
        
        Args:
            prompt: Prompt to display.
            markup: Parse markup in prompt.
            emoji: Parse emoji in prompt.
            password: Hide input (like for passwords).
            stream: Stream to read from.
            
        Returns:
            User input as string.
        """
        if markup:
            prompt = self._parse_markup(prompt)
        
        self.file.write(prompt)
        self.file.flush()
        
        if password:
            import getpass
            return getpass.getpass("")
        
        if stream:
            return stream.readline().rstrip("\n")
        return builtins.input()
    
    def clear(self, home: bool = True) -> None:
        """Clear the console.
        
        Args:
            home: Move cursor to home position.
        """
        if self.is_terminal:
            self.file.write(Colors.CLEAR_SCREEN)
            if home:
                self.file.write(Colors.HOME)
            self.file.flush()
    
    def clear_line(self) -> None:
        """Clear the current line."""
        if self.is_terminal:
            self.file.write(Colors.CLEAR_LINE)
            self.file.write("\r")
            self.file.flush()
    
    def show_cursor(self, show: bool = True) -> None:
        """Show or hide the cursor.
        
        Args:
            show: Whether to show the cursor.
        """
        if self.is_terminal:
            if show:
                self.file.write(Colors.SHOW_CURSOR)
            else:
                self.file.write(Colors.HIDE_CURSOR)
            self.file.flush()
    
    @contextmanager
    def capture(self) -> Iterator["Capture"]:
        """Capture printed output.
        
        Yields:
            A Capture object with the captured output.
        """
        capture = Capture()
        old_file = self._file
        self._file = capture._buffer
        try:
            yield capture
        finally:
            self._file = old_file
    
    @contextmanager
    def pager(
        self,
        pager: Optional[str] = None,
        styles: bool = False,
        links: bool = False,
    ) -> Iterator[None]:
        """Use a pager for output.
        
        Args:
            pager: Pager command (default: $PAGER or 'less').
            styles: Preserve styles in pager.
            links: Preserve links in pager.
            
        Yields:
            Context for paged output.
        """
        # Simple implementation - just yield without paging
        # Full paging would require subprocess and buffering
        yield
    
    def export_text(self, *, clear: bool = True, styles: bool = False) -> str:
        """Export recorded output as plain text.
        
        Args:
            clear: Clear the recording buffer.
            styles: Include ANSI styles.
            
        Returns:
            Recorded output as string.
        """
        if styles:
            text = "".join(seg.render() for seg in self._record_buffer)
        else:
            text = Segment.strip_styles(self._record_buffer)
        
        if clear:
            self._record_buffer.clear()
        
        return text
    
    def export_html(
        self,
        *,
        clear: bool = True,
        theme: Optional[str] = None,
        inline_styles: bool = False,
    ) -> str:
        """Export recorded output as HTML.
        
        Args:
            clear: Clear the recording buffer.
            theme: Theme for HTML export.
            inline_styles: Use inline styles.
            
        Returns:
            Recorded output as HTML string.
        """
        # Simple HTML export - convert ANSI to HTML spans
        text = Segment.strip_styles(self._record_buffer)
        html = f"<pre>{text}</pre>"
        
        if clear:
            self._record_buffer.clear()
        
        return html
    
    def save_text(
        self,
        path: str,
        *,
        clear: bool = True,
        styles: bool = False,
    ) -> None:
        """Save recorded output to a text file.
        
        Args:
            path: Path to save to.
            clear: Clear the recording buffer.
            styles: Include ANSI styles.
        """
        text = self.export_text(clear=clear, styles=styles)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    
    def save_html(
        self,
        path: str,
        *,
        clear: bool = True,
        theme: Optional[str] = None,
        inline_styles: bool = False,
    ) -> None:
        """Save recorded output to an HTML file.
        
        Args:
            path: Path to save to.
            clear: Clear the recording buffer.
            theme: Theme for HTML export.
            inline_styles: Use inline styles.
        """
        html = self.export_html(clear=clear, theme=theme, inline_styles=inline_styles)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    
    def bell(self) -> None:
        """Play a bell sound."""
        self.file.write("\x07")
        self.file.flush()
    
    def set_window_title(self, title: str) -> None:
        """Set the terminal window title.
        
        Args:
            title: New window title.
        """
        if self.is_terminal:
            self.file.write(f"\x1b]0;{title}\x07")
            self.file.flush()


class Capture:
    """Captures console output."""
    
    def __init__(self):
        self._buffer = io.StringIO()
    
    def get(self) -> str:
        """Get the captured output.
        
        Returns:
            Captured text.
        """
        return self._buffer.getvalue()


# ========== Module-level functions (backward compatible) ==========

def _parse_markup(text: str) -> str:
    """Parse simple color markup in text and return ANSI formatted string."""
    result: List[str] = []
    stack: List[str] = []
    pos = 0
    
    for match in _MARKUP_RE.finditer(text):
        result.append(text[pos:match.start()])
        closing, tag = match.groups()
        tag = tag.lower() if tag else ""
        
        if closing:
            if stack and stack[-1] == tag:
                stack.pop()
                result.append(Colors.RESET)
            else:
                result.append(match.group(0))
        else:
            ansi = _STYLE_MAP.get(tag)
            if ansi:
                stack.append(tag)
                result.append(ansi)
            else:
                result.append(match.group(0))
        
        pos = match.end()
    
    result.append(text[pos:])
    if stack:
        result.append(Colors.RESET)
    
    return "".join(result)


def cprint(
    *objects: Iterable,
    sep: str = " ",
    end: str = "\n",
    file=sys.stdout,
    flush: bool = False,
) -> None:
    """Print objects with simple Rich-like markup support.

    Use syntax like ``[red]error[/red]`` or ``[bold]bold text[/bold]``. Unknown
    tags are printed literally.
    Also supports being used as a drop-in replacement for print, including when a slice is passed as an argument.
    """
    text = sep.join(str(o) if not isinstance(o, slice) else str(o) for o in objects)
    formatted = _parse_markup(text)
    builtins.print(formatted, file=file, end=end, flush=flush)


def print(*args, **kwargs):
    """Alias for cprint, so this module's print behaves like cprint."""
    return cprint(*args, **kwargs)


# ========== Default console instance ==========

# Global console instance for convenience
console = Console()
