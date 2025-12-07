#!/usr/bin/env python3
"""
LitPrinter Box Module

Provides Box classes for defining panel borders and box-drawing characters.
Inspired by Rich's Box class with support for various border styles.

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class Box:
    """Defines characters for drawing a box border.
    
    A Box contains 11 characters that define corners, edges, and
    dividers for drawing bordered panels and tables.
    
    The characters are arranged as follows:
    ```
    top_left      horizontal    top_right
    vertical      cross         vertical
    row_left      row_horizontal row_right
    bottom_left   horizontal    bottom_right
    ```
    
    Attributes:
        top_left: Top left corner character.
        top: Top horizontal edge character.
        top_right: Top right corner character.
        left: Left vertical edge character.
        cross: Cross/intersection character (for tables).
        right: Right vertical edge character.
        row_left: Left row divider character.
        row_horizontal: Horizontal row divider character.
        row_right: Right row divider character.
        bottom_left: Bottom left corner character.
        bottom: Bottom horizontal edge character.
        bottom_right: Bottom right corner character.
    """
    top_left: str
    top: str
    top_right: str
    left: str
    cross: str
    right: str
    row_left: str
    row_horizontal: str
    row_right: str
    bottom_left: str
    bottom: str
    bottom_right: str
    
    def __repr__(self) -> str:
        return f"Box({self.top_left}{self.top}{self.top_right}...)"
    
    def get_top(self, widths: List[int]) -> str:
        """Get the top row of the box.
        
        Args:
            widths: List of column widths.
            
        Returns:
            String for the top row.
        """
        parts = []
        for i, width in enumerate(widths):
            parts.append(self.top * width)
            if i < len(widths) - 1:
                parts.append(self.top)
        return self.top_left + "".join(parts) + self.top_right
    
    def get_row(
        self,
        widths: List[int],
        level: str = "row",
        edge: bool = True,
    ) -> str:
        """Get a row divider.
        
        Args:
            widths: List of column widths.
            level: Type of row ("row", "foot", "head").
            edge: Whether to include edge characters.
            
        Returns:
            String for the row divider.
        """
        left = self.row_left if edge else ""
        right = self.row_right if edge else ""
        
        parts = []
        for i, width in enumerate(widths):
            parts.append(self.row_horizontal * width)
            if i < len(widths) - 1:
                parts.append(self.cross)
        
        return left + "".join(parts) + right
    
    def get_bottom(self, widths: List[int]) -> str:
        """Get the bottom row of the box.
        
        Args:
            widths: List of column widths.
            
        Returns:
            String for the bottom row.
        """
        parts = []
        for i, width in enumerate(widths):
            parts.append(self.bottom * width)
            if i < len(widths) - 1:
                parts.append(self.bottom)
        return self.bottom_left + "".join(parts) + self.bottom_right
    
    def substitute(
        self,
        safe_box: bool = False,
        legacy_windows: bool = False,
    ) -> "Box":
        """Substitute box with a compatible version.
        
        Args:
            safe_box: Use ASCII-safe box characters.
            legacy_windows: Use legacy Windows-compatible characters.
            
        Returns:
            A compatible Box, possibly ASCII.
        """
        if safe_box or legacy_windows:
            return ASCII
        return self


# ========== Standard Box Styles ==========

# No border (for borderless panels)
NONE = Box(
    top_left="",
    top="",
    top_right="",
    left="",
    cross="",
    right="",
    row_left="",
    row_horizontal="",
    row_right="",
    bottom_left="",
    bottom="",
    bottom_right="",
)

# ASCII-safe border
ASCII = Box(
    top_left="+",
    top="-",
    top_right="+",
    left="|",
    cross="+",
    right="|",
    row_left="+",
    row_horizontal="-",
    row_right="+",
    bottom_left="+",
    bottom="-",
    bottom_right="+",
)

# Simple box with double lines
ASCII_DOUBLE = Box(
    top_left="+",
    top="=",
    top_right="+",
    left="|",
    cross="+",
    right="|",
    row_left="+",
    row_horizontal="=",
    row_right="+",
    bottom_left="+",
    bottom="=",
    bottom_right="+",
)

# Square corners (single line)
SQUARE = Box(
    top_left="┌",
    top="─",
    top_right="┐",
    left="│",
    cross="┼",
    right="│",
    row_left="├",
    row_horizontal="─",
    row_right="┤",
    bottom_left="└",
    bottom="─",
    bottom_right="┘",
)

# Single line (alias for SQUARE)
SINGLE = SQUARE

# Rounded corners
ROUNDED = Box(
    top_left="╭",
    top="─",
    top_right="╮",
    left="│",
    cross="┼",
    right="│",
    row_left="├",
    row_horizontal="─",
    row_right="┤",
    bottom_left="╰",
    bottom="─",
    bottom_right="╯",
)

# Heavy/thick border
HEAVY = Box(
    top_left="┏",
    top="━",
    top_right="┓",
    left="┃",
    cross="╋",
    right="┃",
    row_left="┣",
    row_horizontal="━",
    row_right="┫",
    bottom_left="┗",
    bottom="━",
    bottom_right="┛",
)

# Thick (alias for HEAVY)
THICK = HEAVY

# Double line border
DOUBLE = Box(
    top_left="╔",
    top="═",
    top_right="╗",
    left="║",
    cross="╬",
    right="║",
    row_left="╠",
    row_horizontal="═",
    row_right="╣",
    bottom_left="╚",
    bottom="═",
    bottom_right="╝",
)

# Dashed border
DASHED = Box(
    top_left="┌",
    top="╌",
    top_right="┐",
    left="╎",
    cross="┼",
    right="╎",
    row_left="├",
    row_horizontal="╌",
    row_right="┤",
    bottom_left="└",
    bottom="╌",
    bottom_right="┘",
)

# Dotted border
DOTTED = Box(
    top_left="┌",
    top="┄",
    top_right="┐",
    left="┆",
    cross="┼",
    right="┆",
    row_left="├",
    row_horizontal="┄",
    row_right="┤",
    bottom_left="└",
    bottom="┄",
    bottom_right="┘",
)

# Heavy dashed border
HEAVY_DASHED = Box(
    top_left="┏",
    top="╍",
    top_right="┓",
    left="╏",
    cross="╋",
    right="╏",
    row_left="┣",
    row_horizontal="╍",
    row_right="┫",
    bottom_left="┗",
    bottom="╍",
    bottom_right="┛",
)

# Minimal border (just corners and thin lines)
MINIMAL = Box(
    top_left="╴",
    top=" ",
    top_right="╶",
    left=" ",
    cross=" ",
    right=" ",
    row_left="╴",
    row_horizontal=" ",
    row_right="╶",
    bottom_left="╴",
    bottom=" ",
    bottom_right="╶",
)

# Simple border with horizontal head
SIMPLE = Box(
    top_left=" ",
    top=" ",
    top_right=" ",
    left=" ",
    cross=" ",
    right=" ",
    row_left="─",
    row_horizontal="─",
    row_right="─",
    bottom_left=" ",
    bottom=" ",
    bottom_right=" ",
)

# Double edge border (double on outside, single inside)
DOUBLE_EDGE = Box(
    top_left="╔",
    top="═",
    top_right="╗",
    left="║",
    cross="┼",
    right="║",
    row_left="╠",
    row_horizontal="─",
    row_right="╣",
    bottom_left="╚",
    bottom="═",
    bottom_right="╝",
)

# Horizontals only (for simple tables)
HORIZONTALS = Box(
    top_left=" ",
    top="─",
    top_right=" ",
    left=" ",
    cross=" ",
    right=" ",
    row_left=" ",
    row_horizontal="─",
    row_right=" ",
    bottom_left=" ",
    bottom="─",
    bottom_right=" ",
)

# Markdown-style table
MARKDOWN = Box(
    top_left=" ",
    top=" ",
    top_right=" ",
    left="|",
    cross="|",
    right="|",
    row_left="|",
    row_horizontal="-",
    row_right="|",
    bottom_left=" ",
    bottom=" ",
    bottom_right=" ",
)


# ========== Box Name Mapping ==========

BOX_MAP = {
    "none": NONE,
    "ascii": ASCII,
    "ascii_double": ASCII_DOUBLE,
    "square": SQUARE,
    "single": SINGLE,
    "rounded": ROUNDED,
    "heavy": HEAVY,
    "thick": THICK,
    "double": DOUBLE,
    "dashed": DASHED,
    "dotted": DOTTED,
    "heavy_dashed": HEAVY_DASHED,
    "minimal": MINIMAL,
    "simple": SIMPLE,
    "double_edge": DOUBLE_EDGE,
    "horizontals": HORIZONTALS,
    "markdown": MARKDOWN,
}


def get_box(name: str, safe_box: bool = False) -> Box:
    """Get a Box by name.
    
    Args:
        name: Name of the box style.
        safe_box: Whether to use ASCII-safe version.
        
    Returns:
        The requested Box.
        
    Raises:
        KeyError: If the box name is not recognized.
    """
    name_lower = name.lower().replace("-", "_")
    if name_lower not in BOX_MAP:
        raise KeyError(f"Unknown box style: {name!r}. "
                      f"Available: {', '.join(sorted(BOX_MAP.keys()))}")
    
    box = BOX_MAP[name_lower]
    if safe_box:
        return box.substitute(safe_box=True)
    return box


# ========== Convenience Functions ==========

def render_box(
    content_lines: List[str],
    box: Box = ROUNDED,
    width: Optional[int] = None,
    title: Optional[str] = None,
    title_align: str = "left",
    subtitle: Optional[str] = None,
    subtitle_align: str = "left",
    padding: Tuple[int, int] = (0, 1),
) -> List[str]:
    """Render content inside a box.
    
    Args:
        content_lines: Lines of content to put in box.
        box: Box style to use.
        width: Width of the box (auto if None).
        title: Optional title for top border.
        title_align: Title alignment ("left", "center", "right").
        subtitle: Optional subtitle for bottom border.
        subtitle_align: Subtitle alignment.
        padding: Padding as (vertical, horizontal).
        
    Returns:
        List of strings forming the box.
    """
    v_padding, h_padding = padding
    
    # Calculate content width
    if content_lines:
        content_width = max(len(line) for line in content_lines)
    else:
        content_width = 0
    
    # Account for title/subtitle
    if title:
        content_width = max(content_width, len(title) + 2)
    if subtitle:
        content_width = max(content_width, len(subtitle) + 2)
    
    # Apply width constraint
    if width is not None:
        inner_width = width - 2 - (h_padding * 2)  # -2 for borders
        content_width = max(content_width, inner_width)
    else:
        inner_width = content_width
    
    total_inner = inner_width + (h_padding * 2)
    
    result = []
    
    # Top border with title
    if title:
        title_text = f" {title} "
        remaining = total_inner - len(title_text)
        
        if title_align == "left":
            left_part = box.top
            right_part = box.top * (remaining - 1)
        elif title_align == "right":
            left_part = box.top * (remaining - 1)
            right_part = box.top
        else:  # center
            left_len = remaining // 2
            right_len = remaining - left_len
            left_part = box.top * left_len
            right_part = box.top * right_len
        
        result.append(f"{box.top_left}{left_part}{title_text}{right_part}{box.top_right}")
    else:
        result.append(f"{box.top_left}{box.top * total_inner}{box.top_right}")
    
    # Top padding
    for _ in range(v_padding):
        result.append(f"{box.left}{' ' * total_inner}{box.right}")
    
    # Content lines
    for line in content_lines:
        padded_line = f"{' ' * h_padding}{line}{' ' * (inner_width - len(line))}{' ' * h_padding}"
        result.append(f"{box.left}{padded_line}{box.right}")
    
    # Bottom padding
    for _ in range(v_padding):
        result.append(f"{box.left}{' ' * total_inner}{box.right}")
    
    # Bottom border with subtitle
    if subtitle:
        subtitle_text = f" {subtitle} "
        remaining = total_inner - len(subtitle_text)
        
        if subtitle_align == "left":
            left_part = box.bottom
            right_part = box.bottom * (remaining - 1)
        elif subtitle_align == "right":
            left_part = box.bottom * (remaining - 1)
            right_part = box.bottom
        else:  # center
            left_len = remaining // 2
            right_len = remaining - left_len
            left_part = box.bottom * left_len
            right_part = box.bottom * right_len
        
        result.append(f"{box.bottom_left}{left_part}{subtitle_text}{right_part}{box.bottom_right}")
    else:
        result.append(f"{box.bottom_left}{box.bottom * total_inner}{box.bottom_right}")
    
    return result
