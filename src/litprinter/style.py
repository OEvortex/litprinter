"""
LitPrinter Style Module

Provides a Style class for representing and composing terminal styles.
Inspired by Rich's Style class with support for parsing, combining, and rendering styles.

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

import re
from dataclasses import dataclass, field
from typing import Optional, Dict, Tuple, Union, Any, TYPE_CHECKING
from functools import lru_cache

if TYPE_CHECKING:
    pass


@dataclass
class Style:
    """Represents a terminal style with colors and attributes.
    
    A Style can include foreground color, background color, and various
    text attributes like bold, italic, underline, etc. Styles can be
    combined using the + operator.
    
    Attributes:
        color: Foreground color name or hex code.
        bgcolor: Background color name or hex code.
        bold: Whether text should be bold.
        dim: Whether text should be dim.
        italic: Whether text should be italic.
        underline: Whether text should be underlined.
        blink: Whether text should blink.
        reverse: Whether to reverse foreground/background.
        strike: Whether text should have strikethrough.
        hidden: Whether text should be hidden.
        link: Optional URL for hyperlink.
    """
    color: Optional[str] = None
    bgcolor: Optional[str] = None
    bold: Optional[bool] = None
    dim: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    blink: Optional[bool] = None
    reverse: Optional[bool] = None
    strike: Optional[bool] = None
    hidden: Optional[bool] = None
    link: Optional[str] = None
    
    # Cache for parsed styles
    _style_cache: Dict[str, "Style"] = field(default_factory=dict, repr=False, compare=False)
    
    def __post_init__(self):
        # Normalize color names
        if self.color:
            self.color = self.color.lower().strip()
        if self.bgcolor:
            self.bgcolor = self.bgcolor.lower().strip()
    
    def __hash__(self) -> int:
        return hash((
            self.color, self.bgcolor, self.bold, self.dim, self.italic,
            self.underline, self.blink, self.reverse, self.strike, self.hidden
        ))
    
    def __bool__(self) -> bool:
        """Check if style has any attributes set."""
        return any([
            self.color, self.bgcolor, self.bold, self.dim, self.italic,
            self.underline, self.blink, self.reverse, self.strike, self.hidden
        ])
    
    def __add__(self, other: Optional["Style"]) -> "Style":
        """Combine two styles. The other style takes precedence."""
        if other is None:
            return self
        if not isinstance(other, Style):
            return NotImplemented
        
        return Style(
            color=other.color if other.color is not None else self.color,
            bgcolor=other.bgcolor if other.bgcolor is not None else self.bgcolor,
            bold=other.bold if other.bold is not None else self.bold,
            dim=other.dim if other.dim is not None else self.dim,
            italic=other.italic if other.italic is not None else self.italic,
            underline=other.underline if other.underline is not None else self.underline,
            blink=other.blink if other.blink is not None else self.blink,
            reverse=other.reverse if other.reverse is not None else self.reverse,
            strike=other.strike if other.strike is not None else self.strike,
            hidden=other.hidden if other.hidden is not None else self.hidden,
            link=other.link if other.link is not None else self.link,
        )
    
    def __radd__(self, other: Optional["Style"]) -> "Style":
        """Support adding None + Style."""
        if other is None:
            return self
        return NotImplemented
    
    @classmethod
    @lru_cache(maxsize=256)
    def parse(cls, style_definition: str) -> "Style":
        """Parse a style definition string into a Style object.
        
        The style definition can include color names, background colors
        (prefixed with "on_" or "on "), and attribute names.
        
        Examples:
            "bold red"
            "italic bright_blue on white"
            "bold underline green on_black"
            "#ff0000"
            "bold #00ff00 on #0000ff"
        
        Args:
            style_definition: Space-separated style descriptors.
            
        Returns:
            A Style object with the parsed attributes.
        """
        if not style_definition:
            return NULL_STYLE
        
        style_definition = style_definition.strip().lower()
        
        color = None
        bgcolor = None
        bold = None
        dim = None
        italic = None
        underline = None
        blink = None
        reverse = None
        strike = None
        hidden = None
        
        # Attribute names
        attributes = {
            "bold": "bold",
            "b": "bold",
            "dim": "dim",
            "italic": "italic",
            "i": "italic",
            "underline": "underline",
            "u": "underline",
            "blink": "blink",
            "reverse": "reverse",
            "strike": "strike",
            "strikethrough": "strike",
            "s": "strike",
            "hidden": "hidden",
            "conceal": "hidden",
        }
        
        # Color names
        color_names = {
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
            "gray", "grey",
            "bright_black", "bright_red", "bright_green", "bright_yellow",
            "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
            "default",
        }
        
        # Extended color names
        extended_colors = {
            "purple": "magenta",
            "pink": "bright_magenta",
            "orange": "bright_red",
            "brown": "yellow",
            "aqua": "cyan",
            "lime": "bright_green",
            "navy": "blue",
            "teal": "cyan",
            "olive": "yellow",
            "maroon": "red",
            "silver": "white",
            "fuchsia": "magenta",
        }
        
        parts = style_definition.split()
        i = 0
        while i < len(parts):
            part = parts[i]
            
            # Check for "on <color>" pattern
            if part == "on" and i + 1 < len(parts):
                bg_part = parts[i + 1]
                if bg_part in color_names:
                    bgcolor = bg_part
                elif bg_part in extended_colors:
                    bgcolor = extended_colors[bg_part]
                elif bg_part.startswith("#"):
                    bgcolor = bg_part
                i += 2
                continue
            
            # Check for "on_<color>" pattern
            if part.startswith("on_"):
                bg_part = part[3:]
                if bg_part in color_names:
                    bgcolor = bg_part
                elif bg_part in extended_colors:
                    bgcolor = extended_colors[bg_part]
                elif bg_part.startswith("#"):
                    bgcolor = bg_part
                i += 1
                continue
            
            # Check for attributes
            if part in attributes:
                attr_name = attributes[part]
                if attr_name == "bold":
                    bold = True
                elif attr_name == "dim":
                    dim = True
                elif attr_name == "italic":
                    italic = True
                elif attr_name == "underline":
                    underline = True
                elif attr_name == "blink":
                    blink = True
                elif attr_name == "reverse":
                    reverse = True
                elif attr_name == "strike":
                    strike = True
                elif attr_name == "hidden":
                    hidden = True
                i += 1
                continue
            
            # Check for "not <attribute>" pattern
            if part == "not" and i + 1 < len(parts):
                neg_part = parts[i + 1]
                if neg_part in attributes:
                    attr_name = attributes[neg_part]
                    if attr_name == "bold":
                        bold = False
                    elif attr_name == "dim":
                        dim = False
                    elif attr_name == "italic":
                        italic = False
                    elif attr_name == "underline":
                        underline = False
                    elif attr_name == "blink":
                        blink = False
                    elif attr_name == "reverse":
                        reverse = False
                    elif attr_name == "strike":
                        strike = False
                    elif attr_name == "hidden":
                        hidden = False
                i += 2
                continue
            
            # Check for colors
            if part in color_names:
                color = part
                i += 1
                continue
            
            if part in extended_colors:
                color = extended_colors[part]
                i += 1
                continue
            
            # Check for hex color
            if part.startswith("#") and len(part) in (4, 7):
                color = part
                i += 1
                continue
            
            # Unknown part, skip
            i += 1
        
        return cls(
            color=color,
            bgcolor=bgcolor,
            bold=bold,
            dim=dim,
            italic=italic,
            underline=underline,
            blink=blink,
            reverse=reverse,
            strike=strike,
            hidden=hidden,
        )
    
    def copy(self) -> "Style":
        """Create a copy of this style.
        
        Returns:
            A new Style with the same attributes.
        """
        return Style(
            color=self.color,
            bgcolor=self.bgcolor,
            bold=self.bold,
            dim=self.dim,
            italic=self.italic,
            underline=self.underline,
            blink=self.blink,
            reverse=self.reverse,
            strike=self.strike,
            hidden=self.hidden,
            link=self.link,
        )
    
    @classmethod
    def chain(cls, *styles: Optional["Style"]) -> "Style":
        """Chain multiple styles together.
        
        Later styles take precedence over earlier ones.
        
        Args:
            *styles: Variable number of Style objects.
            
        Returns:
            A new Style combining all input styles.
        """
        result = NULL_STYLE
        for style in styles:
            if style is not None:
                result = result + style
        return result
    
    @classmethod
    def combine(cls, styles: list) -> "Style":
        """Combine a list of styles.
        
        Args:
            styles: List of Style objects.
            
        Returns:
            A new Style combining all input styles.
        """
        return cls.chain(*styles)
    
    def render(self, text: str) -> str:
        """Apply this style to text and return ANSI-formatted string.
        
        Args:
            text: The text to style.
            
        Returns:
            Text with ANSI escape codes applied.
        """
        if not text:
            return ""
        
        if not self:
            return text
        
        from .colors import Colors
        
        codes = []
        
        # Add attribute codes
        if self.bold:
            codes.append(Colors.BOLD)
        if self.dim:
            codes.append(Colors.DIM)
        if self.italic:
            codes.append(Colors.ITALIC)
        if self.underline:
            codes.append(Colors.UNDERLINE)
        if self.blink:
            codes.append(Colors.BLINK)
        if self.reverse:
            codes.append(Colors.REVERSE)
        if self.strike:
            codes.append(Colors.STRIKE)
        if self.hidden:
            codes.append(Colors.HIDDEN)
        
        # Add foreground color
        if self.color:
            codes.append(self._get_color_code(self.color, is_background=False))
        
        # Add background color
        if self.bgcolor:
            codes.append(self._get_color_code(self.bgcolor, is_background=True))
        
        if codes:
            return "".join(codes) + text + Colors.RESET
        return text
    
    def _get_color_code(self, color: str, is_background: bool = False) -> str:
        """Get ANSI code for a color.
        
        Args:
            color: Color name or hex code.
            is_background: Whether this is a background color.
            
        Returns:
            ANSI escape code string.
        """
        from .colors import Colors
        
        # Basic color map
        fg_colors = {
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
            "bright_black": Colors.BRIGHT_BLACK,
            "bright_red": Colors.BRIGHT_RED,
            "bright_green": Colors.BRIGHT_GREEN,
            "bright_yellow": Colors.BRIGHT_YELLOW,
            "bright_blue": Colors.BRIGHT_BLUE,
            "bright_magenta": Colors.BRIGHT_MAGENTA,
            "bright_cyan": Colors.BRIGHT_CYAN,
            "bright_white": Colors.BRIGHT_WHITE,
            "default": Colors.RESET_FOREGROUND,
        }
        
        bg_colors = {
            "black": Colors.BG_BLACK,
            "red": Colors.BG_RED,
            "green": Colors.BG_GREEN,
            "yellow": Colors.BG_YELLOW,
            "blue": Colors.BG_BLUE,
            "magenta": Colors.BG_MAGENTA,
            "cyan": Colors.BG_CYAN,
            "white": Colors.BG_WHITE,
            "gray": Colors.BG_BRIGHT_BLACK,
            "grey": Colors.BG_BRIGHT_BLACK,
            "bright_black": Colors.BG_BRIGHT_BLACK,
            "bright_red": Colors.BG_BRIGHT_RED,
            "bright_green": Colors.BG_BRIGHT_GREEN,
            "bright_yellow": Colors.BG_BRIGHT_YELLOW,
            "bright_blue": Colors.BG_BRIGHT_BLUE,
            "bright_magenta": Colors.BG_BRIGHT_MAGENTA,
            "bright_cyan": Colors.BG_BRIGHT_CYAN,
            "bright_white": Colors.BG_BRIGHT_WHITE,
            "default": Colors.RESET_BACKGROUND,
        }
        
        color_map = bg_colors if is_background else fg_colors
        
        if color in color_map:
            return color_map[color]
        
        # Handle hex colors
        if color.startswith("#"):
            try:
                hex_color = color.lstrip("#")
                if len(hex_color) == 3:
                    r = int(hex_color[0] * 2, 16)
                    g = int(hex_color[1] * 2, 16)
                    b = int(hex_color[2] * 2, 16)
                else:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                
                if is_background:
                    return Colors.bg_rgb(r, g, b)
                else:
                    return Colors.rgb(r, g, b)
            except (ValueError, IndexError):
                pass
        
        # Handle rgb(r, g, b) format
        rgb_match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", color)
        if rgb_match:
            r, g, b = map(int, rgb_match.groups())
            if is_background:
                return Colors.bg_rgb(r, g, b)
            else:
                return Colors.rgb(r, g, b)
        
        return ""
    
    def __str__(self) -> str:
        """Return a string representation of the style."""
        parts = []
        
        if self.bold:
            parts.append("bold")
        if self.dim:
            parts.append("dim")
        if self.italic:
            parts.append("italic")
        if self.underline:
            parts.append("underline")
        if self.blink:
            parts.append("blink")
        if self.reverse:
            parts.append("reverse")
        if self.strike:
            parts.append("strike")
        if self.hidden:
            parts.append("hidden")
        
        if self.color:
            parts.append(self.color)
        
        if self.bgcolor:
            parts.append(f"on_{self.bgcolor}")
        
        return " ".join(parts) if parts else "none"
    
    def without_color(self) -> "Style":
        """Return a copy of this style without color.
        
        Returns:
            A new Style with colors removed.
        """
        return Style(
            color=None,
            bgcolor=None,
            bold=self.bold,
            dim=self.dim,
            italic=self.italic,
            underline=self.underline,
            blink=self.blink,
            reverse=self.reverse,
            strike=self.strike,
            hidden=self.hidden,
            link=self.link,
        )


# Null style singleton
NULL_STYLE = Style()


# Convenience functions
def style(text: str, style_definition: str) -> str:
    """Apply a style to text.
    
    Args:
        text: The text to style.
        style_definition: Style definition string.
        
    Returns:
        Styled text with ANSI codes.
    """
    return Style.parse(style_definition).render(text)


# Pre-defined styles
BOLD = Style(bold=True)
DIM = Style(dim=True)
ITALIC = Style(italic=True)
UNDERLINE = Style(underline=True)
BLINK = Style(blink=True)
REVERSE = Style(reverse=True)
STRIKE = Style(strike=True)

# Color styles
RED = Style(color="red")
GREEN = Style(color="green")
BLUE = Style(color="blue")
YELLOW = Style(color="yellow")
MAGENTA = Style(color="magenta")
CYAN = Style(color="cyan")
WHITE = Style(color="white")
BLACK = Style(color="black")

# Combined styles
ERROR = Style(color="red", bold=True)
WARNING = Style(color="yellow", bold=True)
INFO = Style(color="blue", bold=True)
SUCCESS = Style(color="green", bold=True)
