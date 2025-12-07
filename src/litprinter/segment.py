#!/usr/bin/env python3
"""
LitPrinter Segment Module

Provides a Segment class for representing styled text segments, inspired by Rich.
Segments are the fundamental building blocks for rendering styled terminal output.

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterable, Iterator, NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .style import Style


class ControlType:
    """Control codes for terminal manipulation."""
    BELL = "bell"
    CARRIAGE_RETURN = "carriage_return"
    HOME = "home"
    CLEAR = "clear"
    SHOW_CURSOR = "show_cursor"
    HIDE_CURSOR = "hide_cursor"
    ENABLE_ALT_SCREEN = "enable_alt_screen"
    DISABLE_ALT_SCREEN = "disable_alt_screen"
    CURSOR_UP = "cursor_up"
    CURSOR_DOWN = "cursor_down"
    CURSOR_FORWARD = "cursor_forward"
    CURSOR_BACKWARD = "cursor_backward"
    CURSOR_MOVE_TO_COLUMN = "cursor_move_to_column"
    CURSOR_MOVE_TO = "cursor_move_to"
    ERASE_IN_LINE = "erase_in_line"
    SET_WINDOW_TITLE = "set_window_title"


class ControlCode(NamedTuple):
    """A control code with optional parameters."""
    code: str
    parameters: Tuple = ()


@dataclass(frozen=True)
class Segment:
    """A piece of text with associated style.
    
    Segments are immutable and represent the smallest unit of styled text
    in the rendering pipeline. They can be combined and manipulated to
    create complex styled output.
    
    Attributes:
        text: The text content of the segment.
        style: Optional style string or Style object to apply.
        control: Optional control code (for cursor movement, etc.).
    """
    text: str
    style: Optional[str] = None
    control: Optional[ControlCode] = None
    
    def __repr__(self) -> str:
        if self.control:
            return f"Segment.control({self.control!r})"
        elif self.style:
            return f"Segment({self.text!r}, {self.style!r})"
        else:
            return f"Segment({self.text!r})"
    
    def __len__(self) -> int:
        """Return the length of the text (display width)."""
        return self.cell_length
    
    def __bool__(self) -> bool:
        """Check if segment has content."""
        return bool(self.text or self.control)
    
    @property
    def cell_length(self) -> int:
        """Get the cell length of the text (for display purposes)."""
        if self.control:
            return 0
        return len(self.text)
    
    @property
    def is_control(self) -> bool:
        """Check if this is a control segment."""
        return self.control is not None
    
    @classmethod
    def line(cls) -> "Segment":
        """Create a newline segment."""
        return cls("\n")
    
    @classmethod
    def control_segment(cls, control_code: ControlCode) -> "Segment":
        """Create a control segment.
        
        Args:
            control_code: The control code to embed.
            
        Returns:
            A control segment with no visible text.
        """
        return cls("", control=control_code)
    
    def apply_style(self, style: Optional[str]) -> "Segment":
        """Apply a style to this segment, combining with existing style.
        
        Args:
            style: Style to apply.
            
        Returns:
            A new Segment with the combined style.
        """
        if not style:
            return self
        if not self.style:
            return Segment(self.text, style, self.control)
        # Combine styles - new style takes precedence
        combined = f"{self.style} {style}"
        return Segment(self.text, combined, self.control)
    
    def render(self) -> str:
        """Render the segment to an ANSI-formatted string.
        
        Returns:
            The text with ANSI escape codes applied.
        """
        from .colors import Colors
        
        if self.control:
            return self._render_control()
        
        if not self.style:
            return self.text
        
        # Parse style and apply ANSI codes
        return self._apply_style_string(self.text, self.style)
    
    def _render_control(self) -> str:
        """Render a control code to ANSI sequence."""
        if not self.control:
            return ""
        
        code = self.control.code
        params = self.control.parameters
        
        control_map = {
            ControlType.BELL: "\x07",
            ControlType.CARRIAGE_RETURN: "\r",
            ControlType.HOME: "\x1b[H",
            ControlType.CLEAR: "\x1b[2J",
            ControlType.SHOW_CURSOR: "\x1b[?25h",
            ControlType.HIDE_CURSOR: "\x1b[?25l",
            ControlType.ENABLE_ALT_SCREEN: "\x1b[?1049h",
            ControlType.DISABLE_ALT_SCREEN: "\x1b[?1049l",
        }
        
        if code in control_map:
            return control_map[code]
        
        if code == ControlType.CURSOR_UP and params:
            return f"\x1b[{params[0]}A"
        if code == ControlType.CURSOR_DOWN and params:
            return f"\x1b[{params[0]}B"
        if code == ControlType.CURSOR_FORWARD and params:
            return f"\x1b[{params[0]}C"
        if code == ControlType.CURSOR_BACKWARD and params:
            return f"\x1b[{params[0]}D"
        if code == ControlType.CURSOR_MOVE_TO_COLUMN and params:
            return f"\x1b[{params[0]}G"
        if code == ControlType.CURSOR_MOVE_TO and len(params) >= 2:
            return f"\x1b[{params[0]};{params[1]}H"
        if code == ControlType.ERASE_IN_LINE and params:
            return f"\x1b[{params[0]}K"
        if code == ControlType.SET_WINDOW_TITLE and params:
            return f"\x1b]0;{params[0]}\x07"
        
        return ""
    
    @staticmethod
    def _apply_style_string(text: str, style: str) -> str:
        """Apply a style string to text.
        
        Args:
            text: The text to style.
            style: Space-separated style descriptors (e.g., "bold red").
            
        Returns:
            ANSI-formatted text.
        """
        from .colors import Colors
        
        if not style or not text:
            return text
        
        codes = []
        style_parts = style.lower().split()
        
        style_map = {
            # Text styles
            "bold": Colors.BOLD,
            "dim": Colors.DIM,
            "italic": Colors.ITALIC,
            "underline": Colors.UNDERLINE,
            "blink": Colors.BLINK,
            "reverse": Colors.REVERSE,
            "strike": Colors.STRIKE,
            "hidden": Colors.HIDDEN,
            # Basic colors
            "black": Colors.BLACK,
            "red": Colors.RED,
            "green": Colors.GREEN,
            "yellow": Colors.YELLOW,
            "blue": Colors.BLUE,
            "magenta": Colors.MAGENTA,
            "cyan": Colors.CYAN,
            "white": Colors.WHITE,
            "gray": Colors.GRAY,
            "grey": Colors.GRAY,
            # Bright colors
            "bright_black": Colors.BRIGHT_BLACK,
            "bright_red": Colors.BRIGHT_RED,
            "bright_green": Colors.BRIGHT_GREEN,
            "bright_yellow": Colors.BRIGHT_YELLOW,
            "bright_blue": Colors.BRIGHT_BLUE,
            "bright_magenta": Colors.BRIGHT_MAGENTA,
            "bright_cyan": Colors.BRIGHT_CYAN,
            "bright_white": Colors.BRIGHT_WHITE,
        }
        
        for part in style_parts:
            if part in style_map:
                codes.append(style_map[part])
            elif part.startswith("on_"):
                # Background color
                bg_color = part[3:]
                bg_map = {
                    "black": Colors.BG_BLACK,
                    "red": Colors.BG_RED,
                    "green": Colors.BG_GREEN,
                    "yellow": Colors.BG_YELLOW,
                    "blue": Colors.BG_BLUE,
                    "magenta": Colors.BG_MAGENTA,
                    "cyan": Colors.BG_CYAN,
                    "white": Colors.BG_WHITE,
                }
                if bg_color in bg_map:
                    codes.append(bg_map[bg_color])
        
        if codes:
            return "".join(codes) + text + Colors.RESET
        return text
    
    # --- Class methods for segment operations ---
    
    @classmethod
    def strip_styles(cls, segments: Iterable["Segment"]) -> str:
        """Join segments into plain text, stripping all styles.
        
        Args:
            segments: An iterable of segments.
            
        Returns:
            Plain text without any styling.
        """
        return "".join(
            segment.text for segment in segments if not segment.is_control
        )
    
    @classmethod
    def strip_links(cls, segments: Iterable["Segment"]) -> Iterator["Segment"]:
        """Remove links from segments (placeholder for future link support).
        
        Args:
            segments: An iterable of segments.
            
        Yields:
            Segments with links removed.
        """
        for segment in segments:
            yield segment
    
    @classmethod
    def get_line_length(cls, segments: Iterable["Segment"]) -> int:
        """Get the total cell length of segments.
        
        Args:
            segments: An iterable of segments.
            
        Returns:
            Total display width of the segments.
        """
        return sum(segment.cell_length for segment in segments)
    
    @classmethod
    def get_shape(cls, segments: List["Segment"]) -> Tuple[int, int]:
        """Get the shape (width, height) of rendered segments.
        
        Args:
            segments: List of segments.
            
        Returns:
            Tuple of (max_width, number_of_lines).
        """
        lines = cls.split_lines(segments)
        max_width = 0
        height = 0
        for line in lines:
            width = cls.get_line_length(line)
            max_width = max(max_width, width)
            height += 1
        return max_width, height
    
    @classmethod
    def split_lines(cls, segments: Iterable["Segment"]) -> Iterator[List["Segment"]]:
        """Split segments at newline characters.
        
        Args:
            segments: An iterable of segments.
            
        Yields:
            Lists of segments for each line.
        """
        line: List[Segment] = []
        for segment in segments:
            if segment.is_control:
                line.append(segment)
                continue
            
            text = segment.text
            if "\n" in text:
                parts = text.split("\n")
                for i, part in enumerate(parts):
                    if i > 0:
                        yield line
                        line = []
                    if part:
                        line.append(Segment(part, segment.style))
            else:
                line.append(segment)
        
        if line:
            yield line
    
    @classmethod
    def split_and_crop_lines(
        cls,
        segments: Iterable["Segment"],
        length: int,
        style: Optional[str] = None,
        pad: bool = True,
        include_new_lines: bool = True,
    ) -> Iterator[List["Segment"]]:
        """Split segments into lines and crop/pad to the given length.
        
        Args:
            segments: An iterable of segments.
            length: Maximum line length.
            style: Style for padding.
            pad: Whether to pad lines to the given length.
            include_new_lines: Whether to append newline segments.
            
        Yields:
            Lists of segments for each cropped line.
        """
        for line in cls.split_lines(segments):
            cropped = cls.crop_line(line, length, style, pad)
            if include_new_lines:
                cropped.append(Segment.line())
            yield cropped
    
    @classmethod
    def crop_line(
        cls,
        segments: List["Segment"],
        length: int,
        style: Optional[str] = None,
        pad: bool = True,
    ) -> List["Segment"]:
        """Crop a line of segments to the given length.
        
        Args:
            segments: List of segments representing a line.
            length: Maximum length.
            style: Style for padding.
            pad: Whether to pad to length.
            
        Returns:
            Cropped list of segments.
        """
        result: List[Segment] = []
        total_length = 0
        
        for segment in segments:
            if segment.is_control:
                result.append(segment)
                continue
            
            segment_length = segment.cell_length
            if total_length + segment_length <= length:
                result.append(segment)
                total_length += segment_length
            else:
                # Crop this segment
                remaining = length - total_length
                if remaining > 0:
                    result.append(Segment(segment.text[:remaining], segment.style))
                    total_length = length
                break
        
        if pad and total_length < length:
            padding = " " * (length - total_length)
            result.append(Segment(padding, style))
        
        return result
    
    @classmethod
    def adjust_line_length(
        cls,
        line: List["Segment"],
        length: int,
        style: Optional[str] = None,
        pad: bool = True,
    ) -> List["Segment"]:
        """Adjust a line to the given length.
        
        Args:
            line: List of segments.
            length: Target length.
            style: Style for padding.
            pad: Whether to pad short lines.
            
        Returns:
            Adjusted list of segments.
        """
        line_length = cls.get_line_length(line)
        
        if line_length < length:
            if pad:
                line = list(line) + [Segment(" " * (length - line_length), style)]
            return line
        elif line_length > length:
            return cls.crop_line(line, length, style, pad=False)
        
        return line
    
    @classmethod
    def align_line(
        cls,
        line: List["Segment"],
        length: int,
        align: str = "left",
        style: Optional[str] = None,
    ) -> List["Segment"]:
        """Align a line within the given length.
        
        Args:
            line: List of segments.
            length: Target length.
            align: Alignment ("left", "center", "right").
            style: Style for padding.
            
        Returns:
            Aligned list of segments.
        """
        line_length = cls.get_line_length(line)
        
        if line_length >= length:
            return cls.crop_line(line, length, style, pad=False)
        
        extra = length - line_length
        
        if align == "left":
            return list(line) + [Segment(" " * extra, style)]
        elif align == "right":
            return [Segment(" " * extra, style)] + list(line)
        elif align == "center":
            left = extra // 2
            right = extra - left
            return [Segment(" " * left, style)] + list(line) + [Segment(" " * right, style)]
        
        return list(line)
    
    @classmethod
    def simplify(cls, segments: Iterable["Segment"]) -> Iterator["Segment"]:
        """Simplify segments by combining adjacent segments with the same style.
        
        Args:
            segments: An iterable of segments.
            
        Yields:
            Simplified segments.
        """
        current_text = ""
        current_style = None
        
        for segment in segments:
            if segment.is_control:
                if current_text:
                    yield Segment(current_text, current_style)
                    current_text = ""
                    current_style = None
                yield segment
            elif segment.style == current_style:
                current_text += segment.text
            else:
                if current_text:
                    yield Segment(current_text, current_style)
                current_text = segment.text
                current_style = segment.style
        
        if current_text:
            yield Segment(current_text, current_style)


# Convenience function
def render_segments(segments: Iterable[Segment]) -> str:
    """Render a sequence of segments to a string.
    
    Args:
        segments: An iterable of segments.
        
    Returns:
        The rendered string with ANSI codes.
    """
    return "".join(segment.render() for segment in segments)
