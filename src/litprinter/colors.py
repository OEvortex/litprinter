#!/usr/bin/env python3
"""
LitPrinter Colors Module

Provides ANSI color codes and utilities for terminal output styling.
Inspired by the Rich package with extensive color support.

Features:
- Standard 16 colors (8 normal, 8 bright)
- Background colors
- 256-color support
- RGB/True color support
- Named colors
- Text styling (bold, italic, etc.)
- Color utilities and helpers

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

import re
from typing import Dict, Tuple, Union, Optional, List, Any


class Colors:
    """ANSI color codes and utilities for terminal output.

    This class provides constants and methods for working with terminal colors
    and text styling, similar to the Rich package.
    """
    # Base colors (standard 8 colors)
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'  # Same as BRIGHT_BLACK
    GREY = '\033[90m'  # Alternative spelling

    # Bright colors (high intensity)
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Bright background colors
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'
    BG_GRAY = '\033[100m'  # Same as BG_BRIGHT_BLACK
    BG_GREY = '\033[100m'  # Alternative spelling

    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    BLINK_RAPID = '\033[6m'  # Not widely supported
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'
    DOUBLE_UNDERLINE = '\033[21m'  # Not widely supported
    OVERLINE = '\033[53m'  # Not widely supported

    # Special control codes
    RESET = '\033[0m'
    RESET_FOREGROUND = '\033[39m'
    RESET_BACKGROUND = '\033[49m'
    CLEAR_SCREEN = '\033[2J'
    CLEAR_LINE = '\033[2K'
    CLEAR_TO_END = '\033[0K'
    CLEAR_TO_START = '\033[1K'

    # Cursor movement
    UP = '\033[1A'
    DOWN = '\033[1B'
    RIGHT = '\033[1C'
    LEFT = '\033[1D'
    HOME = '\033[H'
    SAVE_POSITION = '\033[s'
    RESTORE_POSITION = '\033[u'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'

    # Named colors (similar to Rich)
    # A subset of CSS color names
    NAMED_COLORS: Dict[str, Tuple[int, int, int]] = {
        "aliceblue": (240, 248, 255),
        "antiquewhite": (250, 235, 215),
        "aqua": (0, 255, 255),
        "aquamarine": (127, 255, 212),
        "azure": (240, 255, 255),
        "beige": (245, 245, 220),
        "bisque": (255, 228, 196),
        "black": (0, 0, 0),
        "blanchedalmond": (255, 235, 205),
        "blue": (0, 0, 255),
        "blueviolet": (138, 43, 226),
        "brown": (165, 42, 42),
        "burlywood": (222, 184, 135),
        "cadetblue": (95, 158, 160),
        "chartreuse": (127, 255, 0),
        "chocolate": (210, 105, 30),
        "coral": (255, 127, 80),
        "cornflowerblue": (100, 149, 237),
        "cornsilk": (255, 248, 220),
        "crimson": (220, 20, 60),
        "cyan": (0, 255, 255),
        "darkblue": (0, 0, 139),
        "darkcyan": (0, 139, 139),
        "darkgoldenrod": (184, 134, 11),
        "darkgray": (169, 169, 169),
        "darkgrey": (169, 169, 169),
        "darkgreen": (0, 100, 0),
        "darkkhaki": (189, 183, 107),
        "darkmagenta": (139, 0, 139),
        "darkolivegreen": (85, 107, 47),
        "darkorange": (255, 140, 0),
        "darkorchid": (153, 50, 204),
        "darkred": (139, 0, 0),
        "darksalmon": (233, 150, 122),
        "darkseagreen": (143, 188, 143),
        "darkslateblue": (72, 61, 139),
        "darkslategray": (47, 79, 79),
        "darkslategrey": (47, 79, 79),
        "darkturquoise": (0, 206, 209),
        "darkviolet": (148, 0, 211),
        "deeppink": (255, 20, 147),
        "deepskyblue": (0, 191, 255),
        "dimgray": (105, 105, 105),
        "dimgrey": (105, 105, 105),
        "dodgerblue": (30, 144, 255),
        "firebrick": (178, 34, 34),
        "floralwhite": (255, 250, 240),
        "forestgreen": (34, 139, 34),
        "fuchsia": (255, 0, 255),
        "gainsboro": (220, 220, 220),
        "ghostwhite": (248, 248, 255),
        "gold": (255, 215, 0),
        "goldenrod": (218, 165, 32),
        "gray": (128, 128, 128),
        "grey": (128, 128, 128),
        "green": (0, 128, 0),
        "greenyellow": (173, 255, 47),
        "honeydew": (240, 255, 240),
        "hotpink": (255, 105, 180),
        "indianred": (205, 92, 92),
        "indigo": (75, 0, 130),
        "ivory": (255, 255, 240),
        "khaki": (240, 230, 140),
        "lavender": (230, 230, 250),
        "lavenderblush": (255, 240, 245),
        "lawngreen": (124, 252, 0),
        "lemonchiffon": (255, 250, 205),
        "lightblue": (173, 216, 230),
        "lightcoral": (240, 128, 128),
        "lightcyan": (224, 255, 255),
        "lightgoldenrodyellow": (250, 250, 210),
        "lightgray": (211, 211, 211),
        "lightgrey": (211, 211, 211),
        "lightgreen": (144, 238, 144),
        "lightpink": (255, 182, 193),
        "lightsalmon": (255, 160, 122),
        "lightseagreen": (32, 178, 170),
        "lightskyblue": (135, 206, 250),
        "lightslategray": (119, 136, 153),
        "lightslategrey": (119, 136, 153),
        "lightsteelblue": (176, 196, 222),
        "lightyellow": (255, 255, 224),
        "lime": (0, 255, 0),
        "limegreen": (50, 205, 50),
        "linen": (250, 240, 230),
        "magenta": (255, 0, 255),
        "maroon": (128, 0, 0),
        "mediumaquamarine": (102, 205, 170),
        "mediumblue": (0, 0, 205),
        "mediumorchid": (186, 85, 211),
        "mediumpurple": (147, 112, 219),
        "mediumseagreen": (60, 179, 113),
        "mediumslateblue": (123, 104, 238),
        "mediumspringgreen": (0, 250, 154),
        "mediumturquoise": (72, 209, 204),
        "mediumvioletred": (199, 21, 133),
        "midnightblue": (25, 25, 112),
        "mintcream": (245, 255, 250),
        "mistyrose": (255, 228, 225),
        "moccasin": (255, 228, 181),
        "navajowhite": (255, 222, 173),
        "navy": (0, 0, 128),
        "oldlace": (253, 245, 230),
        "olive": (128, 128, 0),
        "olivedrab": (107, 142, 35),
        "orange": (255, 165, 0),
        "orangered": (255, 69, 0),
        "orchid": (218, 112, 214),
        "palegoldenrod": (238, 232, 170),
        "palegreen": (152, 251, 152),
        "paleturquoise": (175, 238, 238),
        "palevioletred": (219, 112, 147),
        "papayawhip": (255, 239, 213),
        "peachpuff": (255, 218, 185),
        "peru": (205, 133, 63),
        "pink": (255, 192, 203),
        "plum": (221, 160, 221),
        "powderblue": (176, 224, 230),
        "purple": (128, 0, 128),
        "rebeccapurple": (102, 51, 153),
        "red": (255, 0, 0),
        "rosybrown": (188, 143, 143),
        "royalblue": (65, 105, 225),
        "saddlebrown": (139, 69, 19),
        "salmon": (250, 128, 114),
        "sandybrown": (244, 164, 96),
        "seagreen": (46, 139, 87),
        "seashell": (255, 245, 238),
        "sienna": (160, 82, 45),
        "silver": (192, 192, 192),
        "skyblue": (135, 206, 235),
        "slateblue": (106, 90, 205),
        "slategray": (112, 128, 144),
        "slategrey": (112, 128, 144),
        "snow": (255, 250, 250),
        "springgreen": (0, 255, 127),
        "steelblue": (70, 130, 180),
        "tan": (210, 180, 140),
        "teal": (0, 128, 128),
        "thistle": (216, 191, 216),
        "tomato": (255, 99, 71),
        "turquoise": (64, 224, 208),
        "violet": (238, 130, 238),
        "wheat": (245, 222, 179),
        "white": (255, 255, 255),
        "whitesmoke": (245, 245, 245),
        "yellow": (255, 255, 0),
        "yellowgreen": (154, 205, 50),
    }

    # Color palettes
    RAINBOW = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA]
    SPECTRUM = [RED, BRIGHT_RED, YELLOW, BRIGHT_YELLOW, GREEN, BRIGHT_GREEN,
                CYAN, BRIGHT_CYAN, BLUE, BRIGHT_BLUE, MAGENTA, BRIGHT_MAGENTA]
    MONOCHROME = [BLACK, GRAY, WHITE, BRIGHT_WHITE]

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Generate a 24-bit (true color) ANSI color code.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            ANSI escape sequence for the RGB color
        """
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return f'\033[38;2;{r};{g};{b}m'

    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        """Generate a 24-bit (true color) ANSI background color code.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            ANSI escape sequence for the RGB background color
        """
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return f'\033[48;2;{r};{g};{b}m'

    @staticmethod
    def color256(n: int) -> str:
        """Generate an ANSI color code for 256-color terminals.

        Args:
            n: Color number (0-255)

        Returns:
            ANSI escape sequence for the 256-color
        """
        n = max(0, min(255, n))
        return f'\033[38;5;{n}m'

    @staticmethod
    def bg_color256(n: int) -> str:
        """Generate an ANSI background color code for 256-color terminals.

        Args:
            n: Color number (0-255)

        Returns:
            ANSI escape sequence for the 256-color background
        """
        n = max(0, min(255, n))
        return f'\033[48;5;{n}m'

    @classmethod
    def from_name(cls, name: str) -> str:
        """Get an ANSI color code from a named color.

        Args:
            name: Color name (e.g., 'red', 'blue', 'lightgreen')

        Returns:
            ANSI escape sequence for the named color

        Raises:
            ValueError: If the color name is not recognized
        """
        name = name.lower()
        if name in cls.NAMED_COLORS:
            r, g, b = cls.NAMED_COLORS[name]
            return cls.rgb(r, g, b)
        raise ValueError(f"Unknown color name: {name}")

    @classmethod
    def bg_from_name(cls, name: str) -> str:
        """Get an ANSI background color code from a named color.

        Args:
            name: Color name (e.g., 'red', 'blue', 'lightgreen')

        Returns:
            ANSI escape sequence for the named background color

        Raises:
            ValueError: If the color name is not recognized
        """
        name = name.lower()
        if name in cls.NAMED_COLORS:
            r, g, b = cls.NAMED_COLORS[name]
            return cls.bg_rgb(r, g, b)
        raise ValueError(f"Unknown color name: {name}")

    @staticmethod
    def from_hex(hex_color: str) -> str:
        """Convert a hex color code to an ANSI color code.

        Args:
            hex_color: Hex color code (e.g., '#FF0000', 'FF0000')

        Returns:
            ANSI escape sequence for the hex color

        Raises:
            ValueError: If the hex color is invalid
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) not in (3, 6):
            raise ValueError(f"Invalid hex color: {hex_color}")

        if len(hex_color) == 3:
            r = int(hex_color[0] + hex_color[0], 16)
            g = int(hex_color[1] + hex_color[1], 16)
            b = int(hex_color[2] + hex_color[2], 16)
        else:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

        return Colors.rgb(r, g, b)

    @staticmethod
    def bg_from_hex(hex_color: str) -> str:
        """Convert a hex color code to an ANSI background color code.

        Args:
            hex_color: Hex color code (e.g., '#FF0000', 'FF0000')

        Returns:
            ANSI escape sequence for the hex background color

        Raises:
            ValueError: If the hex color is invalid
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) not in (3, 6):
            raise ValueError(f"Invalid hex color: {hex_color}")

        if len(hex_color) == 3:
            r = int(hex_color[0] + hex_color[0], 16)
            g = int(hex_color[1] + hex_color[1], 16)
            b = int(hex_color[2] + hex_color[2], 16)
        else:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

        return Colors.bg_rgb(r, g, b)

    @classmethod
    def parse(cls, color: str) -> str:
        """Parse a color name or hex code and return an ANSI color code.

        This helper makes it easy to accept either hex strings like ``"#ff00ff"``
        or one of the ``NAMED_COLORS`` entries. The comparison is case
        insensitive and the leading ``#`` is optional for hex codes.
        """
        if not color:
            raise ValueError("Color value cannot be empty")

        color = color.strip()
        if re.fullmatch(r"#?[0-9a-fA-F]{3}", color) or re.fullmatch(r"#?[0-9a-fA-F]{6}", color):
            return cls.from_hex(color)

        return cls.from_name(color)

    @classmethod
    def bg_parse(cls, color: str) -> str:
        """Parse a color name or hex code and return an ANSI background code."""
        if not color:
            raise ValueError("Color value cannot be empty")

        color = color.strip()
        if re.fullmatch(r"#?[0-9a-fA-F]{3}", color) or re.fullmatch(r"#?[0-9a-fA-F]{6}", color):
            return cls.bg_from_hex(color)

        return cls.bg_from_name(color)

    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove ANSI escape sequences from a string.

        Args:
            text: Text containing ANSI escape sequences

        Returns:
            Text with ANSI escape sequences removed
        """
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    @staticmethod
    def style(text: str, *styles: str) -> str:
        """Apply multiple styles to text.

        Args:
            text: Text to style
            *styles: ANSI style codes to apply

        Returns:
            Styled text with ANSI escape sequences
        """
        if not text:
            return ""
        return "".join(styles) + str(text) + Colors.RESET

    @staticmethod
    def gradient(text: str, start_color: Tuple[int, int, int], end_color: Tuple[int, int, int]) -> str:
        """Apply a gradient color effect to text.

        Args:
            text: Text to apply gradient to
            start_color: RGB tuple for starting color
            end_color: RGB tuple for ending color

        Returns:
            Text with gradient color effect
        """
        if not text:
            return ""

        result = ""
        text_len = len(text)

        for i, char in enumerate(text):
            if char.isspace():
                result += char
                continue

            # Calculate color for this position
            progress = i / (text_len - 1) if text_len > 1 else 0
            r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)

            result += Colors.rgb(r, g, b) + char

        return result + Colors.RESET

    @classmethod
    def rainbow(cls, text: str) -> str:
        """Apply rainbow colors to text.

        Args:
            text: Text to apply rainbow colors to

        Returns:
            Text with rainbow colors
        """
        if not text:
            return ""

        rainbow_colors = [
            (255, 0, 0),      # Red
            (255, 127, 0),    # Orange
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (0, 0, 255),      # Blue
            (75, 0, 130),     # Indigo
            (148, 0, 211)     # Violet
        ]

        result = ""
        for i, char in enumerate(text):
            if char.isspace():
                result += char
                continue

            color_idx = i % len(rainbow_colors)
            r, g, b = rainbow_colors[color_idx]
            result += cls.rgb(r, g, b) + char

        return result + cls.RESET

