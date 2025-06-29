#!/usr/bin/env python3
"""
LitPrinter Panel Module

Professional panel rendering system for creating bordered, styled content areas.
Supports various border styles, padding, alignment, and sophisticated layout options.
Enhanced with Rich-inspired features including box styles, text overflow handling,
background patterns, shadows, and advanced styling capabilities.

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

import os
import shutil
import textwrap
from typing import Optional, Union, Literal, Dict, Any, List, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

try:
    from .colors import Colors
except ImportError:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    from litprinter.colors import Colors


class BorderStyle(Enum):
    """Predefined border styles for panels."""
    NONE = "none"
    SINGLE = "single"
    DOUBLE = "double"
    THICK = "thick"
    ROUNDED = "rounded"
    ASCII = "ascii"
    DASHED = "dashed"
    DOTTED = "dotted"
    SIMPLE = "simple"
    HEAVY = "heavy"
    SQUARE = "square"
    MINIMAL = "minimal"


class TextOverflow(Enum):
    """Text overflow handling strategies."""
    FOLD = "fold"          # Wrap text to next line
    ELLIPSIS = "ellipsis"  # Add ... at end
    CROP = "crop"          # Cut off text
    IGNORE = "ignore"      # Let text overflow


class RenderableType(ABC):
    """Abstract base class for renderable objects."""
    
    @abstractmethod
    def render(self, width: int) -> List[str]:
        """Render the object to a list of strings."""
        pass


@dataclass
class Segment:
    """A segment of styled text."""
    text: str
    style: Optional[str] = None
    
    def __len__(self) -> int:
        return len(self.text)
    
    def apply_style(self, colors: 'Colors') -> str:
        """Apply styling to the text."""
        if not self.style:
            return self.text
        # Apply color/style logic here
        return self.text


@dataclass
class BorderChars:
    """Character set for drawing panel borders."""
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    horizontal: str
    vertical: str
    cross: str = "+"
    
    def __post_init__(self):
        if not self.cross:
            self.cross = "+"


# Predefined border character sets
BORDER_CHARS = {
    BorderStyle.NONE: BorderChars("", "", "", "", "", ""),
    BorderStyle.SINGLE: BorderChars("┌", "┐", "└", "┘", "─", "│", "┼"),
    BorderStyle.DOUBLE: BorderChars("╔", "╗", "╚", "╝", "═", "║", "╬"),
    BorderStyle.THICK: BorderChars("┏", "┓", "┗", "┛", "━", "┃", "╋"),
    BorderStyle.ROUNDED: BorderChars("╭", "╮", "╰", "╯", "─", "│", "┼"),
    BorderStyle.ASCII: BorderChars("+", "+", "+", "+", "-", "|", "+"),
    BorderStyle.DASHED: BorderChars("┌", "┐", "└", "┘", "╌", "╎", "┼"),
    BorderStyle.DOTTED: BorderChars("┌", "┐", "└", "┘", "┄", "┆", "┼"),
    BorderStyle.SIMPLE: BorderChars(" ", " ", " ", " ", " ", " ", " "),
    BorderStyle.HEAVY: BorderChars("┏", "┓", "┗", "┛", "━", "┃", "╋"),
    BorderStyle.SQUARE: BorderChars("┌", "┐", "└", "┘", "─", "│", "┼"),
    BorderStyle.MINIMAL: BorderChars("┌", "┐", "└", "┘", "─", "│", "┼"),
}


@dataclass
class Shadow:
    """Shadow configuration for panels."""
    enabled: bool = False
    offset_x: int = 1
    offset_y: int = 1
    color: str = "black"
    opacity: float = 0.5
    char: str = "▓"


@dataclass 
class Background:
    """Background pattern configuration."""
    char: str = " "
    color: Optional[str] = None
    pattern: Optional[str] = None  # dots, stripes, etc.


@dataclass
class BoxModel:
    """Box model for advanced layout control."""
    margin: 'Padding' = field(default_factory=lambda: Padding.all(0))
    border: Optional['BorderStyle'] = None
    padding: 'Padding' = field(default_factory=lambda: Padding.symmetric(0, 1))
    content_width: Optional[int] = None
    content_height: Optional[int] = None


@dataclass
class Padding:
    """Padding configuration for panels."""
    top: int = 0
    right: int = 1
    bottom: int = 0
    left: int = 1
    
    @classmethod
    def all(cls, value: int) -> 'Padding':
        """Create padding with same value for all sides."""
        return cls(value, value, value, value)
    
    @classmethod
    def symmetric(cls, vertical: int, horizontal: int) -> 'Padding':
        """Create padding with vertical and horizontal values."""
        return cls(vertical, horizontal, vertical, horizontal)
    
    @classmethod
    def from_tuple(cls, values: Tuple[int, ...]) -> 'Padding':
        """Create padding from tuple (top, right, bottom, left) or (vertical, horizontal)."""
        if len(values) == 1:
            return cls.all(values[0])
        elif len(values) == 2:
            return cls.symmetric(values[0], values[1])
        elif len(values) == 4:
            return cls(*values)
        else:
            raise ValueError("Padding tuple must have 1, 2, or 4 values")
    
    @property
    def total_vertical(self) -> int:
        """Get total vertical padding."""
        return self.top + self.bottom
    
    @property
    def total_horizontal(self) -> int:
        """Get total horizontal padding."""
        return self.left + self.right


class Panel:
    """
    Professional panel renderer for creating bordered, styled content areas.
    
    Enhanced Features:
    - Multiple border styles (single, double, thick, rounded, ASCII, dashed, dotted, etc.)
    - Flexible padding and alignment options
    - Advanced color and styling support
    - Auto-sizing and manual width/height control
    - Title and subtitle support with flexible positioning
    - Multi-line content handling with overflow strategies
    - Shadow effects and background patterns
    - Box model with margin, border, padding
    - Rich-style text rendering and markup support
    - Content wrapping and truncation options
    - Vertical alignment and content distribution
    - Theme support and style inheritance
    """
    
    def __init__(
        self,
        content: Union[str, RenderableType] = "",
        *,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        border_style: Union[BorderStyle, str] = BorderStyle.SINGLE,
        border_color: Optional[str] = None,
        title_color: Optional[str] = None,
        subtitle_color: Optional[str] = None,
        content_color: Optional[str] = None,
        background_color: Optional[str] = None,
        padding: Union[Padding, int, Tuple[int, ...]] = Padding.symmetric(0, 1),
        margin: Union[Padding, int, Tuple[int, ...]] = Padding.all(0),
        width: Optional[int] = None,
        height: Optional[int] = None,
        min_width: int = 0,
        max_width: Optional[int] = None,
        min_height: int = 0,
        max_height: Optional[int] = None,
        align: Literal["left", "center", "right"] = "left",
        vertical_align: Literal["top", "middle", "bottom"] = "top",
        title_align: Literal["left", "center", "right"] = "left",
        subtitle_align: Literal["left", "center", "right"] = "left",
        expand: bool = False,
        expand_height: bool = False,
        highlight: bool = False,
        safe_box: bool = True,
        overflow: TextOverflow = TextOverflow.FOLD,
        no_wrap: bool = False,
        tab_size: int = 4,
        box_model: Optional[BoxModel] = None,
        shadow: Optional[Shadow] = None,
        background: Optional[Background] = None,
        style: Optional[str] = None,
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize an enhanced panel.
        
        Args:
            content: The main content to display (string or renderable object)
            title: Optional title for the panel (displayed in top border)
            subtitle: Optional subtitle for the panel (displayed in bottom border)
            border_style: Border style to use (BorderStyle enum or string)
            border_color: Color for the border (ANSI color name or code)
            title_color: Color for the title text
            subtitle_color: Color for the subtitle text
            content_color: Color for the content text
            background_color: Background color for the panel
            padding: Padding around content (Padding object, int, or tuple)
            margin: Margin around panel (Padding object, int, or tuple)
            width: Fixed width for the panel (None for auto-sizing)
            height: Fixed height for the panel (None for auto-sizing)
            min_width: Minimum width for the panel
            max_width: Maximum width for the panel
            min_height: Minimum height for the panel
            max_height: Maximum height for the panel
            align: Horizontal content alignment within the panel
            vertical_align: Vertical content alignment within the panel
            title_align: Title alignment within the top border
            subtitle_align: Subtitle alignment within the bottom border
            expand: Whether to expand to fill available width
            expand_height: Whether to expand to fill available height
            highlight: Whether to apply highlight styling
            safe_box: Whether to use safe box characters for compatibility
            overflow: How to handle text overflow (fold, ellipsis, crop, ignore)
            no_wrap: Whether to disable text wrapping
            tab_size: Size of tabs in characters
            box_model: Advanced box model configuration
            shadow: Shadow configuration
            background: Background pattern configuration
            style: CSS-like style string
            theme: Theme configuration dictionary
        """
        self.content = content
        self.title = title
        self.subtitle = subtitle
        
        # Handle border style
        if isinstance(border_style, str):
            try:
                self.border_style = BorderStyle(border_style.lower())
            except ValueError:
                self.border_style = BorderStyle.SINGLE
        else:
            self.border_style = border_style
            
        # Handle padding and margin
        self.padding = self._normalize_spacing(padding)
        self.margin = self._normalize_spacing(margin)
        
        # Use box model if provided
        if box_model:
            self.padding = box_model.padding
            self.margin = box_model.margin
            if box_model.border:
                self.border_style = box_model.border
            
        # Colors and styling
        self.border_color = border_color
        self.title_color = title_color
        self.subtitle_color = subtitle_color or title_color
        self.content_color = content_color
        self.background_color = background_color
        self.style = style
        self.theme = theme or {}
        
        # Dimensions and layout
        self.width = width
        self.height = height
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.align = align
        self.vertical_align = vertical_align
        self.title_align = title_align
        self.subtitle_align = subtitle_align
        self.expand = expand
        self.expand_height = expand_height
        self.highlight = highlight
        self.safe_box = safe_box
        self.overflow = overflow
        self.no_wrap = no_wrap
        self.tab_size = tab_size
        
        # Advanced features
        self.shadow = shadow
        self.background = background or Background()
        
        # Get terminal dimensions for auto-sizing
        self.terminal_width, self.terminal_height = self._get_terminal_size()
        
    @staticmethod
    def _normalize_spacing(spacing: Union[Padding, int, Tuple[int, ...]]) -> Padding:
        """Normalize spacing input to Padding object."""
        if isinstance(spacing, Padding):
            return spacing
        elif isinstance(spacing, int):
            return Padding.all(spacing)
        elif isinstance(spacing, tuple):
            return Padding.from_tuple(spacing)
        else:
            return Padding.all(0)
        
    @staticmethod
    def _get_terminal_size() -> Tuple[int, int]:
        """Get the current terminal dimensions."""
        try:
            size = shutil.get_terminal_size(fallback=(80, 20))
            return size.columns, size.lines
        except Exception:
            return 80, 20
    
    def _get_style_value(self, key: str, default: Any = None) -> Any:
        """Get a style value from theme or direct attribute."""
        if self.theme and key in self.theme:
            return self.theme[key]
        return getattr(self, key, default)
    
    def _parse_markup(self, text: str) -> List[Segment]:
        """Parse markup text into styled segments (basic implementation)."""
        # This is a simplified version - in Rich this would be much more sophisticated
        segments = []
        current_text = ""
        
        # For now, just return the text as a single segment
        # In a full implementation, this would parse [color], [bold], etc.
        if text:
            segments.append(Segment(text))
        
        return segments
    
    def _measure_content(self, content: str) -> Tuple[int, int]:
        """Measure the natural size of content."""
        if not content:
            return 0, 0
            
        lines = content.split('\n')
        width = max(self._get_display_width(line) for line in lines) if lines else 0
        height = len(lines)
        
        return width, height
    
    def _expand_tabs(self, text: str) -> str:
        """Expand tabs to spaces."""
        return text.expandtabs(self.tab_size)
    
    def _handle_overflow(self, text: str, max_width: int) -> str:
        """Handle text overflow according to strategy."""
        if self._get_display_width(text) <= max_width:
            return text
            
        if self.overflow == TextOverflow.CROP:
            return self._crop_text(text, max_width)
        elif self.overflow == TextOverflow.ELLIPSIS:
            return self._ellipsis_text(text, max_width)
        elif self.overflow == TextOverflow.IGNORE:
            return text
        else:  # FOLD
            return text  # Will be handled by wrapping
    
    def _crop_text(self, text: str, max_width: int) -> str:
        """Crop text to fit width."""
        if max_width <= 0:
            return ""
        
        # Simple character-based cropping
        cropped = ""
        current_width = 0
        
        for char in text:
            char_width = 1  # Simplified - in reality would handle wide chars
            if current_width + char_width > max_width:
                break
            cropped += char
            current_width += char_width
            
        return cropped
    
    def _ellipsis_text(self, text: str, max_width: int) -> str:
        """Add ellipsis to text that's too long."""
        if max_width <= 3:
            return "..." if max_width >= 3 else "." * max_width
            
        cropped = self._crop_text(text, max_width - 3)
        return cropped + "..."
    
    def _apply_background(self, text: str, width: int) -> str:
        """Apply background pattern to text."""
        if not self.background or not self.background_color:
            return text
            
        # Simple background application
        bg_color = self._apply_color("", self.background_color)
        reset = Colors.RESET if bg_color else ""
        
        return f"{bg_color}{text}{reset}"
    
    def _apply_color(self, text: str, color: Optional[str]) -> str:
        """Apply color to text if color is specified."""
        if not color:
            return text
            
        # Handle predefined color names
        color_map = {
            "red": Colors.RED,
            "green": Colors.GREEN,
            "yellow": Colors.YELLOW,
            "blue": Colors.BLUE,
            "magenta": Colors.MAGENTA,
            "cyan": Colors.CYAN,
            "white": Colors.WHITE,
            "black": Colors.BLACK,
            "gray": Colors.GRAY,
            "grey": Colors.GRAY,
            "bright_red": Colors.BRIGHT_RED,
            "bright_green": Colors.BRIGHT_GREEN,
            "bright_yellow": Colors.BRIGHT_YELLOW,
            "bright_blue": Colors.BRIGHT_BLUE,
            "bright_magenta": Colors.BRIGHT_MAGENTA,
            "bright_cyan": Colors.BRIGHT_CYAN,
            "bright_white": Colors.BRIGHT_WHITE,
            "bold": Colors.BOLD,
            "dim": Colors.DIM,
            "italic": Colors.ITALIC,
            "underline": Colors.UNDERLINE,
        }
        
        color_code = color_map.get(color.lower(), color)
        return f"{color_code}{text}{Colors.RESET}"
    
    def _strip_ansi(self, text: str) -> str:
        """Remove ANSI escape codes from text for length calculation."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)
    
    def _get_display_width(self, text: str) -> int:
        """Get the display width of text (excluding ANSI codes)."""
        return len(self._strip_ansi(text))
    
    def _pad_line(self, line: str, width: int, align: str = "left") -> str:
        """Pad a line to the specified width with proper alignment."""
        display_width = self._get_display_width(line)
        padding_needed = max(0, width - display_width)
        
        if align == "center":
            left_pad = padding_needed // 2
            right_pad = padding_needed - left_pad
            return " " * left_pad + line + " " * right_pad
        elif align == "right":
            return " " * padding_needed + line
        else:  # left
            return line + " " * padding_needed
    
    def _wrap_content(self, content: str, max_width: int) -> List[str]:
        """Wrap content to fit within the specified width with enhanced options."""
        if not content:
            return [""]
        
        if self.no_wrap:
            lines = content.split('\n')
            return [self._handle_overflow(line, max_width) for line in lines]
            
        lines = []
        for line in content.split('\n'):
            if not line:
                lines.append("")
                continue
            
            # Expand tabs first
            line = self._expand_tabs(line)
            
            # Handle lines that are already within the limit
            if self._get_display_width(line) <= max_width:
                lines.append(line)
                continue
            
            # Enhanced word wrapping with better break handling
            if self.overflow == TextOverflow.FOLD:
                wrapped = textwrap.fill(
                    line, 
                    width=max_width,
                    break_long_words=True,
                    break_on_hyphens=True,
                    expand_tabs=False,  # Already handled
                )
                lines.extend(wrapped.split('\n'))
            else:
                lines.append(self._handle_overflow(line, max_width))
        
        return lines
    
    def _apply_vertical_alignment(self, content_lines: List[str], available_height: int) -> List[str]:
        """Apply vertical alignment to content within available space."""
        content_height = len(content_lines)
        
        if content_height >= available_height or self.vertical_align == "top":
            return content_lines[:available_height]
        
        extra_lines = available_height - content_height
        
        if self.vertical_align == "middle":
            top_padding = extra_lines // 2
            bottom_padding = extra_lines - top_padding
            return ([""] * top_padding + 
                   content_lines + 
                   [""] * bottom_padding)
        elif self.vertical_align == "bottom":
            return [""] * extra_lines + content_lines
        
        return content_lines
    
    def _calculate_dimensions(self, content_lines: List[str]) -> Tuple[int, int, int]:
        """Calculate the optimal panel dimensions and content area."""
        # Calculate content width
        content_width = max(
            (self._get_display_width(line) for line in content_lines),
            default=0
        )
        
        # Consider title and subtitle width
        title_width = 0
        if self.title:
            title_width = self._get_display_width(self.title) + 4  # Space for " title "
        if self.subtitle:
            title_width = max(title_width, self._get_display_width(self.subtitle) + 4)
        
        # Calculate total content width including titles
        total_content_width = max(content_width, title_width)
        
        # Calculate panel width
        panel_width = total_content_width + self.padding.total_horizontal
        
        # Handle border width (2 characters for left and right borders)
        if self.border_style != BorderStyle.NONE:
            panel_width += 2
            
        # Apply width constraints
        if self.width is not None:
            panel_width = self.width
        else:
            panel_width = max(panel_width, self.min_width)
            if self.max_width is not None:
                panel_width = min(panel_width, self.max_width)
            if self.expand:
                panel_width = min(self.terminal_width - self.margin.total_horizontal, panel_width)
        
        # Calculate content area width
        content_area_width = panel_width
        if self.border_style != BorderStyle.NONE:
            content_area_width -= 2
        content_area_width -= self.padding.total_horizontal
        content_area_width = max(1, content_area_width)  # Ensure minimum width
        
        # Calculate panel height
        content_height = len(content_lines)
        panel_height = content_height + self.padding.total_vertical
        if self.border_style != BorderStyle.NONE:
            panel_height += 2  # Top and bottom borders
            
        # Apply height constraints
        if self.height is not None:
            panel_height = self.height
        else:
            panel_height = max(panel_height, self.min_height)
            if self.max_height is not None:
                panel_height = min(panel_height, self.max_height)
            if self.expand_height:
                panel_height = min(self.terminal_height - self.margin.total_vertical, panel_height)
        
        # Calculate available content height
        available_content_height = panel_height
        if self.border_style != BorderStyle.NONE:
            available_content_height -= 2
        available_content_height -= self.padding.total_vertical
        available_content_height = max(1, available_content_height)
            
        return panel_width, content_area_width, available_content_height
    
    def render(self) -> str:
        """Render the enhanced panel to a string."""
        if not self.content and not self.title and not self.subtitle:
            return ""
        
        # Handle different content types
        if isinstance(self.content, RenderableType):
            # For renderable objects, get their string representation
            content_str = str(self.content)
        else:
            content_str = str(self.content) if self.content else ""
            
        # Prepare content
        content_lines = content_str.split('\n') if content_str else [""]
        
        # Calculate dimensions
        panel_width, content_area_width, available_content_height = self._calculate_dimensions(content_lines)
        
        # Wrap content if necessary
        if content_area_width > 0:
            wrapped_lines = []
            for line in content_lines:
                wrapped_lines.extend(self._wrap_content(line, content_area_width))
            content_lines = wrapped_lines
        
        # Apply vertical alignment
        content_lines = self._apply_vertical_alignment(content_lines, available_content_height)
        
        # Get border characters
        border_chars = BORDER_CHARS[self.border_style]
        
        # Build the panel
        panel_lines = []
        
        # Add top margin
        for _ in range(self.margin.top):
            panel_lines.append(" " * (panel_width + self.margin.total_horizontal))
        
        # Top border with title
        if self.border_style != BorderStyle.NONE:
            top_border = self._render_border_with_text(
                panel_width, border_chars.top_left, border_chars.top_right,
                border_chars.horizontal, self.title, self.title_color, self.title_align
            )
            panel_lines.append(" " * self.margin.left + top_border + " " * self.margin.right)
        
        # Top padding
        for _ in range(self.padding.top):
            line = self._render_empty_line(panel_width, border_chars)
            panel_lines.append(" " * self.margin.left + line + " " * self.margin.right)
        
        # Content lines
        for line in content_lines:
            # Apply content color
            colored_line = self._apply_color(line, self.content_color)
            
            # Apply background
            colored_line = self._apply_background(colored_line, content_area_width)
            
            # Pad the line to fit the content area
            padded_line = self._pad_line(colored_line, content_area_width, self.align)
            
            # Add left and right padding
            content_with_padding = " " * self.padding.left + padded_line + " " * self.padding.right
            
            # Add borders
            if self.border_style != BorderStyle.NONE:
                full_line = (
                    self._apply_color(border_chars.vertical, self.border_color) +
                    content_with_padding +
                    self._apply_color(border_chars.vertical, self.border_color)
                )
            else:
                full_line = content_with_padding
                
            panel_lines.append(" " * self.margin.left + full_line + " " * self.margin.right)
        
        # Bottom padding
        for _ in range(self.padding.bottom):
            line = self._render_empty_line(panel_width, border_chars)
            panel_lines.append(" " * self.margin.left + line + " " * self.margin.right)
        
        # Bottom border with subtitle
        if self.border_style != BorderStyle.NONE:
            bottom_border = self._render_border_with_text(
                panel_width, border_chars.bottom_left, border_chars.bottom_right,
                border_chars.horizontal, self.subtitle, self.subtitle_color, self.subtitle_align
            )
            panel_lines.append(" " * self.margin.left + bottom_border + " " * self.margin.right)
        
        # Add bottom margin
        for _ in range(self.margin.bottom):
            panel_lines.append(" " * (panel_width + self.margin.total_horizontal))
        
        # Add shadow if enabled
        if self.shadow and self.shadow.enabled:
            panel_lines = self._add_shadow(panel_lines, panel_width)
        
        return '\n'.join(panel_lines)
    
    def _render_border_with_text(
        self, 
        panel_width: int, 
        left_char: str, 
        right_char: str, 
        horizontal_char: str, 
        text: Optional[str], 
        text_color: Optional[str], 
        text_align: str
    ) -> str:
        """Render a border line with optional text."""
        if not text:
            return (
                self._apply_color(left_char, self.border_color) +
                self._apply_color(horizontal_char * (panel_width - 2), self.border_color) +
                self._apply_color(right_char, self.border_color)
            )
        
        text_with_spaces = f" {text} "
        text_colored = self._apply_color(text_with_spaces, text_color)
        text_display_width = len(text_with_spaces)  # Use original length for calculation
        
        remaining_width = panel_width - 2 - text_display_width  # Account for corners
        
        if text_align == "center":
            left_border_len = remaining_width // 2
            right_border_len = remaining_width - left_border_len
        elif text_align == "right":
            left_border_len = remaining_width
            right_border_len = 0
        else:  # left
            left_border_len = 0
            right_border_len = remaining_width
        
        return (
            self._apply_color(left_char, self.border_color) +
            self._apply_color(horizontal_char * left_border_len, self.border_color) +
            text_colored +
            self._apply_color(horizontal_char * right_border_len, self.border_color) +
            self._apply_color(right_char, self.border_color)
        )
    
    def _render_empty_line(self, panel_width: int, border_chars: BorderChars) -> str:
        """Render an empty line with borders."""
        if self.border_style != BorderStyle.NONE:
            return (
                self._apply_color(border_chars.vertical, self.border_color) +
                " " * (panel_width - 2) +
                self._apply_color(border_chars.vertical, self.border_color)
            )
        else:
            return " " * panel_width
    
    def _add_shadow(self, panel_lines: List[str], panel_width: int) -> List[str]:
        """Add shadow effect to the panel."""
        if not self.shadow or not self.shadow.enabled:
            return panel_lines
        
        shadowed_lines = []
        shadow_char = self._apply_color(self.shadow.char, self.shadow.color)
        
        # Add lines with shadow
        for i, line in enumerate(panel_lines):
            if i >= self.shadow.offset_y:
                # Add shadow to the right
                line += shadow_char * self.shadow.offset_x
            shadowed_lines.append(line)
        
        # Add shadow lines at the bottom
        for _ in range(self.shadow.offset_y):
            shadow_line = (
                " " * (self.margin.left + self.shadow.offset_x) +
                shadow_char * panel_width +
                " " * self.margin.right
            )
            shadowed_lines.append(shadow_line)
        
        return shadowed_lines
    
    def print(self, *, file=None) -> None:
        """Print the panel to stdout or specified file."""
        import sys
        if file is None:
            file = sys.stdout
        print(self.render(), file=file)


# Convenience functions with enhanced features
def panel(
    content: Union[str, RenderableType],
    *,
    title: Optional[str] = None,
    border_style: Union[BorderStyle, str] = BorderStyle.SINGLE,
    **kwargs
) -> str:
    """Create and render a panel with the given content."""
    return Panel(content, title=title, border_style=border_style, **kwargs).render()

# Theme presets
PANEL_THEMES = {
    "default": {
        "border_style": BorderStyle.SINGLE,
        "border_color": None,
        "padding": Padding.symmetric(0, 1),
    },
    "modern": {
        "border_style": BorderStyle.ROUNDED,
        "border_color": "bright_blue",
        "padding": Padding.symmetric(1, 2),
        "shadow": Shadow(enabled=True, offset_x=1, offset_y=1, color="gray"),
    },
    "minimal": {
        "border_style": BorderStyle.NONE,
        "padding": Padding.symmetric(1, 2),
        "background": Background(color="gray"),
    },
    "classic": {
        "border_style": BorderStyle.DOUBLE,
        "border_color": "white",
        "padding": Padding.all(1),
    },
    "terminal": {
        "border_style": BorderStyle.ASCII,
        "border_color": "green",
        "content_color": "green",
        "padding": Padding.symmetric(0, 1),
    },
    "elegant": {
        "border_style": BorderStyle.SINGLE,
        "border_color": "cyan",
        "padding": Padding.symmetric(1, 3),
        "align": "center",
    },
}


class PanelGroup:
    """Group multiple panels together with advanced layout options."""
    
    def __init__(
        self,
        *panels: Panel,
        layout: Literal["vertical", "horizontal", "grid"] = "vertical",
        spacing: int = 1,
        equal_width: bool = False,
        equal_height: bool = False,
        align: Literal["left", "center", "right"] = "left",
    ):
        """Initialize a panel group."""
        self.panels = list(panels)
        self.layout = layout
        self.spacing = spacing
        self.equal_width = equal_width
        self.equal_height = equal_height
        self.align = align
    
    def add_panel(self, panel: Panel) -> None:
        """Add a panel to the group."""
        self.panels.append(panel)
    
    def render(self) -> str:
        """Render all panels in the group."""
        if not self.panels:
            return ""
        
        if self.layout == "vertical":
            return self._render_vertical()
        elif self.layout == "horizontal":
            return self._render_horizontal()
        elif self.layout == "grid":
            return self._render_grid()
        else:
            return self._render_vertical()
    
    def _render_vertical(self) -> str:
        """Render panels vertically stacked."""
        rendered = []
        for i, panel in enumerate(self.panels):
            rendered.append(panel.render())
            if i < len(self.panels) - 1:  # Add spacing between panels
                rendered.extend([""] * self.spacing)
        return "\n".join(rendered)
    
    def _render_horizontal(self) -> str:
        """Render panels side by side."""
        panel_lines = []
        max_height = 0
        
        # Render each panel and find max height
        for panel in self.panels:
            lines = panel.render().split('\n')
            panel_lines.append(lines)
            max_height = max(max_height, len(lines))
        
        # Pad panels to same height if needed
        if self.equal_height:
            for lines in panel_lines:
                while len(lines) < max_height:
                    lines.append(" " * len(lines[0]) if lines else "")
        
        # Combine lines horizontally
        result_lines = []
        for row in range(max_height):
            line_parts = []
            for i, lines in enumerate(panel_lines):
                if row < len(lines):
                    line_parts.append(lines[row])
                else:
                    line_parts.append("")
                
                # Add spacing between panels
                if i < len(panel_lines) - 1:
                    line_parts.append(" " * self.spacing)
            
            result_lines.append("".join(line_parts))
        
        return "\n".join(result_lines)
    
    def _render_grid(self) -> str:
        """Render panels in a grid layout."""
        # Simple 2-column grid for now
        cols = 2
        rows = []
        
        for i in range(0, len(self.panels), cols):
            row_panels = self.panels[i:i + cols]
            if len(row_panels) == cols:
                # Create horizontal group for this row
                row_group = PanelGroup(*row_panels, layout="horizontal", spacing=self.spacing)
                rows.append(row_group.render())
            else:
                # Handle incomplete row
                for panel in row_panels:
                    rows.append(panel.render())
        
        return ("\n" * self.spacing).join(rows)


# Example usage and demonstrations
if __name__ == "__main__":
    # Demonstrate enhanced panel features
    print("🎨 LitPrinter Enhanced Panel Examples\n")
    
    # Basic panel with new features
    print(panel(
        "This is an enhanced panel with modern features!", 
        title="✨ Enhanced Panel",
        border_style=BorderStyle.ROUNDED,
        border_color="bright_blue",
        padding=Padding.symmetric(1, 2)
    ))
    print()
    
    # Panel with overflow handling
    long_text = "This is a very long line of text that demonstrates the overflow handling capabilities of the enhanced panel system. " * 3
    
    print(panel(
        long_text,
        title="Overflow: Fold",
        width=50,
        overflow=TextOverflow.FOLD,
        border_color="yellow"
    ))
    print()
    
    print(panel(
        long_text,
        title="Overflow: Ellipsis",
        width=50,
        overflow=TextOverflow.ELLIPSIS,
        border_color="red"
    ))
    print()
    
    # Vertical alignment
    print(panel(
        "Centered content",
        title="Vertical Alignment",
        height=8,
        vertical_align="middle",
        align="center",
        border_style=BorderStyle.DOUBLE,
        border_color="magenta"
    ))
    print()
    
    # Multi-line content with advanced formatting
    multiline_content = """📊 Enhanced Multi-line Panel Features:

• Improved text wrapping with textwrap
• Multiple overflow strategies
• Vertical alignment options
• Background patterns support
• Shadow effects
• Theme system
• Box model with margins
• Rich-style text rendering"""
    
    print(panel(
        multiline_content,
        title="🎨 Feature Showcase",
        subtitle="Enhanced LitPrinter Panel v2.0",
        border_style=BorderStyle.THICK,
        border_color="bright_green",
        title_color="bright_white",
        subtitle_color="bright_cyan",
        content_color="white",
        padding=Padding.symmetric(1, 3),
        margin=Padding.symmetric(0, 2),
        align="left",
        title_align="center",
        subtitle_align="center"
    ))
    print()
    
    # Panel group demonstration
    print("👥 Panel Group Examples:")
    
    # Vertical group
    group = PanelGroup(
        Panel("Panel 1", title="First", border_color="red"),
        Panel("Panel 2", title="Second", border_color="green"), 
        Panel("Panel 3", title="Third", border_color="blue"),
        layout="vertical",
        spacing=1
    )
    print("Vertical Layout:")
    print(group.render())
    print()
    
    # Horizontal group
    h_group = PanelGroup(
        Panel("Left\nPanel", title="Left", border_color="cyan", width=15),
        Panel("Right\nPanel", title="Right", border_color="magenta", width=15),
        layout="horizontal",
        spacing=3
    )
    print("Horizontal Layout:")
    print(h_group.render())
    print()
    
    # Different border styles showcase
    print("🎭 Border Styles Showcase:")
    styles = [
        BorderStyle.SINGLE, BorderStyle.DOUBLE, BorderStyle.THICK, 
        BorderStyle.ROUNDED, BorderStyle.ASCII, BorderStyle.DASHED,
        BorderStyle.DOTTED, BorderStyle.HEAVY
    ]
    
    for style in styles:
        print(panel(
            f"This panel uses {style.value} border style.",
            title=f"{style.value.title()} Border",
            border_style=style,
            border_color="bright_white"
        ))
        print()
    
    print("🎉 Enhanced Panel System Demo Complete!")
    print("Check out all the new features: themes, shadows, overflow handling, groups, and more!")
