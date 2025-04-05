"""
Basic usage examples for LitPrinter.
"""

from litprinter import litprint, lit, NEON, JARVIS, RICH, MODERN, CYBERPUNK


def basic_examples():
    """Show basic usage examples."""
    # Basic usage
    litprint("Hello, world!")
    
    # Print variables with their names
    x, y = 10, 20
    lit(x, y)
    
    # Print complex data structures
    data = {
        "name": "LitPrinter",
        "version": "0.2.0",
        "features": ["colorized output", "context tracking", "pretty printing"],
        "nested": {
            "level1": {
                "level2": [1, 2, 3, 4, 5]
            }
        }
    }
    lit("Complex data:", data)


def theme_examples():
    """Show theme examples."""
    # Default theme
    lit("Default theme")
    
    # NEON theme
    lit.style = NEON
    lit("NEON theme")
    
    # JARVIS theme
    lit.style = JARVIS
    lit("JARVIS theme")
    
    # RICH theme
    lit.style = RICH
    lit("RICH theme")
    
    # MODERN theme
    lit.style = MODERN
    lit("MODERN theme")
    
    # CYBERPUNK theme
    lit.style = CYBERPUNK
    lit("CYBERPUNK theme")


def function_example():
    """Show usage in functions."""
    def add(a, b):
        lit("Adding", a, b)
        return a + b
    
    result = add(5, 10)
    lit("Result:", result)


if __name__ == "__main__":
    print("=== Basic Examples ===")
    basic_examples()
    
    print("\n=== Theme Examples ===")
    theme_examples()
    
    print("\n=== Function Example ===")
    function_example()
