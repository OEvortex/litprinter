"""
Command-line interface for LitPrinter.

This module allows LitPrinter to be run as a module:
    python -m litprinter

It provides a simple demonstration of LitPrinter's capabilities.
"""

import sys
from litprinter import litprint, lit, __version__


def main():
    """Run a simple demonstration of LitPrinter."""
    print(f"LitPrinter v{__version__}")
    print("A sophisticated debug printing library for Python")
    print("\nDemo:")
    
    # Simple demo
    x, y = 10, 20
    litprint("Basic usage with litprint:", x, y)
    
    # More complex demo
    data = {
        "name": "LitPrinter",
        "version": __version__,
        "features": ["colorized output", "context tracking", "pretty printing"],
        "nested": {
            "level1": {
                "level2": [1, 2, 3, 4, 5]
            }
        }
    }
    
    lit("Complex data structure:", data)
    
    print("\nFor more information, visit: https://github.com/yourusername/litprinter")


if __name__ == "__main__":
    main()
