#!/usr/bin/env python3
"""
LitPrinter Colors Demo

This script demonstrates the enhanced color capabilities of the Colors class.
"""

import sys
import os

# Add the parent directory to the path so we can import litprinter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.litprinter.colors import Colors

def print_header(text):
    """Print a section header."""
    print("\n" + Colors.BOLD + Colors.UNDERLINE + text + Colors.RESET)

def main():
    """Demonstrate the color capabilities of the Colors class."""
    print(Colors.BOLD + Colors.UNDERLINE + "LitPrinter Colors Demo" + Colors.RESET)

    # Basic colors
    print_header("Basic Colors")
    for color_name in ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "GRAY"]:
        color_code = getattr(Colors, color_name)
        print(f"{color_code}This text is in {color_name.lower()}{Colors.RESET}")

    # Bright colors
    print_header("Bright Colors")
    for color_name in ["BRIGHT_BLACK", "BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW",
                       "BRIGHT_BLUE", "BRIGHT_MAGENTA", "BRIGHT_CYAN", "BRIGHT_WHITE"]:
        color_code = getattr(Colors, color_name)
        print(f"{color_code}This text is in {color_name.lower()}{Colors.RESET}")

    # Text styles
    print_header("Text Styles")
    styles = {
        "BOLD": "Bold text",
        "DIM": "Dim text",
        "ITALIC": "Italic text",
        "UNDERLINE": "Underlined text",
        "BLINK": "Blinking text (if supported)",
        "REVERSE": "Reversed text",
        "STRIKE": "Strikethrough text"
    }

    for style_name, description in styles.items():
        style_code = getattr(Colors, style_name)
        print(f"{style_code}{description}{Colors.RESET}")

    # Background colors
    print_header("Background Colors")
    for bg_name in ["BG_BLACK", "BG_RED", "BG_GREEN", "BG_YELLOW",
                   "BG_BLUE", "BG_MAGENTA", "BG_CYAN", "BG_WHITE"]:
        bg_code = getattr(Colors, bg_name)
        print(f"{bg_code}This text has a {bg_name[3:].lower()} background{Colors.RESET}")

    # RGB colors
    print_header("RGB Colors")
    for r in range(0, 256, 64):
        print(f"{Colors.rgb(r, 100, 200)}RGB({r}, 100, 200){Colors.RESET}", end=" ")
    print()

    for g in range(0, 256, 64):
        print(f"{Colors.rgb(100, g, 200)}RGB(100, {g}, 200){Colors.RESET}", end=" ")
    print()

    for b in range(0, 256, 64):
        print(f"{Colors.rgb(100, 200, b)}RGB(100, 200, {b}){Colors.RESET}", end=" ")
    print()

    # Named colors
    print_header("Named Colors (Sample)")
    named_colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "purple",
                   "orange", "pink", "brown", "gold", "silver", "lime", "teal"]

    for name in named_colors:
        try:
            color = Colors.from_name(name)
            print(f"{color}{name}{Colors.RESET}", end=" ")
        except ValueError:
            pass
    print()

    # Hex colors
    print_header("Hex Colors")
    hex_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF",
                 "#FF8800", "#8800FF", "#00FF88"]

    for hex_color in hex_colors:
        color = Colors.from_hex(hex_color)
        print(f"{color}{hex_color}{Colors.RESET}", end=" ")
    print()

    # 256 colors (sample)
    print_header("256 Colors (Sample)")
    for i in range(0, 256, 16):
        color = Colors.color256(i)
        print(f"{color}Color-{i}{Colors.RESET}", end=" ")
    print()

    # Special effects
    print_header("Special Effects")

    # Gradient
    start_color = (255, 0, 0)  # Red
    end_color = (0, 0, 255)    # Blue
    text = "This text has a red to blue gradient effect"
    print(Colors.gradient(text, start_color, end_color))

    # Rainbow
    text = "This text has rainbow colors applied to it"
    print(Colors.rainbow(text))

    # Combined styles
    print_header("Combined Styles")
    print(f"{Colors.BOLD}{Colors.UNDERLINE}{Colors.RED}Bold, underlined red text{Colors.RESET}")
    print(f"{Colors.ITALIC}{Colors.YELLOW}{Colors.BG_BLUE}Italic yellow text on blue background{Colors.RESET}")

    # Using style method
    print_header("Using style() Method")
    print(Colors.style("Styled text", Colors.BOLD, Colors.GREEN, Colors.UNDERLINE))

if __name__ == "__main__":
    main()
