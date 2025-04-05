#!/usr/bin/env python3
"""
LitPrinter Core Themes Demo

This script demonstrates the various syntax highlighting themes available in litprinter.core.
It shows how to use the colorize function with different themes.
"""

import sys
import os

# Add the parent directory to the path so we can import litprinter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.litprinter.core import colorize, colorizedStderrPrint

def demonstrate_theme(theme_name):
    """Demonstrate a specific theme using the colorize function."""
    print(f"\n\n{'=' * 80}")
    print(f"Theme: {theme_name}")
    print(f"{'=' * 80}\n")
    
    # Sample Python code to colorize
    sample_code = '''
def example_function(param1, param2=None):
    """This is a docstring."""
    # This is a comment
    numbers = [1, 2, 3, 4, 5]
    text = "Hello, World!"
    result = {
        "numbers": numbers,
        "text": text,
        "boolean": True,
        "none": None
    }
    
    if param2 is not None:
        result["param2"] = param2
    
    for num in numbers:
        if num % 2 == 0:
            print(f"{num} is even")
        else:
            print(f"{num} is odd")
    
    return result
'''
    
    # Colorize the code with the specified theme
    colorizedStderrPrint(sample_code, theme_name)

def main():
    """Demonstrate all available themes."""
    # List of all available themes
    themes = [
        "jarvis",
        "rich",
        "modern",
        "neon",
        "cyberpunk",
        "dracula",
        "monokai",
        "solarized",
        "nord",
        "github",
        "vscode",
        "material",
        "retro",
        "ocean",
        "autumn"
    ]
    
    # Show each theme
    for theme in themes:
        demonstrate_theme(theme)

if __name__ == "__main__":
    main()
