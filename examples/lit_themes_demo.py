#!/usr/bin/env python3
"""
LitPrinter Lit Themes Demo

This script demonstrates the various syntax highlighting themes available in litprinter.
It shows how to use the lit function with different themes.
"""

import sys
import os

# Add the parent directory to the path so we can import litprinter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.litprinter import lit
from src.litprinter.coloring import (
    JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI,
    SOLARIZED, NORD, GITHUB, VSCODE, MATERIAL, RETRO, OCEAN, AUTUMN
)

def demonstrate_theme(theme_name, theme_style):
    """Demonstrate a specific theme using the lit function."""
    print(f"\n\n{'=' * 80}")
    print(f"Theme: {theme_name}")
    print(f"{'=' * 80}\n")
    
    # Set the theme
    lit.style = theme_style
    
    # Sample data to display
    sample_data = {
        "string": "Hello, World!",
        "numbers": [1, 2, 3, 4, 5],
        "boolean": True,
        "none": None,
        "nested": {
            "list": ["a", "b", "c"],
            "dict": {"key1": "value1", "key2": "value2"}
        }
    }
    
    # Use lit to display the data
    lit(f"Using {theme_name} theme:", sample_data)

def main():
    """Demonstrate all available themes."""
    # List of all available themes
    themes = [
        ("JARVIS", JARVIS),
        ("RICH", RICH),
        ("MODERN", MODERN),
        ("NEON", NEON),
        ("CYBERPUNK", CYBERPUNK),
        ("DRACULA", DRACULA),
        ("MONOKAI", MONOKAI),
        ("SOLARIZED", SOLARIZED),
        ("NORD", NORD),
        ("GITHUB", GITHUB),
        ("VSCODE", VSCODE),
        ("MATERIAL", MATERIAL),
        ("RETRO", RETRO),
        ("OCEAN", OCEAN),
        ("AUTUMN", AUTUMN)
    ]
    
    # Show each theme
    for theme_name, theme_style in themes:
        demonstrate_theme(theme_name, theme_style)

if __name__ == "__main__":
    main()
