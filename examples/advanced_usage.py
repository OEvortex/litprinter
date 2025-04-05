"""
Advanced usage examples for LitPrinter.

This example demonstrates more advanced features of LitPrinter including:
- Custom formatters
- Traceback enhancement
- Logging to file
- Custom themes
- VS Code integration
"""

from litprinter import lit, log, argumentToString, install, uninstall
from litprinter.traceback import install as install_traceback
from litprinter.coloring import (
    JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI,
    SOLARIZED, NORD, GITHUB, VSCODE, MATERIAL, RETRO, OCEAN, AUTUMN,
    create_custom_style
)
from pygments.token import Text, String, Number


# Define a custom class
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        self._private = "This is private"
        self.__very_private = "This is very private"


# Register a custom formatter for the Person class
@argumentToString.register(Person)
def format_person(person):
    return f"Person(name='{person.name}', age={person.age}, email='{person.email}')"


def demonstrate_custom_formatter():
    """Demonstrate custom formatter for a user-defined class."""
    print("\n=== Custom Formatter Example ===")

    # Create a Person instance
    person = Person("John Doe", 30, "john@example.com")

    # Use lit to print the person
    lit("Person object:", person)


def demonstrate_traceback():
    """Demonstrate traceback enhancement with different themes."""
    print("\n=== Traceback Enhancement Example ===")
    print("(This will raise an exception with a pretty traceback using different themes)")

    # Define a function that will raise an exception
    def outer_function():
        x = 10
        y = "test"
        inner_function(x, y)

    def inner_function(a, b):
        c = {"key1": a, "key2": b}
        # This will raise a TypeError
        result = c["key1"] + c["key2"]
        return result

    # Demonstrate with a few selected themes
    selected_themes = ["cyberpunk", "retro", "github", "nord", "autumn"]

    for theme in selected_themes:
        print(f"\n--- Traceback with {theme.upper()} theme ---")

        # Install the traceback handler with the current theme
        install_traceback(
            theme=theme,
            show_locals=True,
            extra_lines=2
        )

        try:
            outer_function()
        except Exception as e:
            print(f"Caught exception: {type(e).__name__}: {e}")
            print(f"(The above exception was displayed with {theme.upper()} theme)")


def demonstrate_logging():
    """Demonstrate logging capabilities."""
    print("\n=== Logging Example ===")

    # Log with different levels
    log("This is a debug message", level="debug")
    log("This is an info message", level="info")
    log("This is a warning message", level="warning")
    log("This is an error message", level="error")

    # Log to a file
    log("This message is logged to a file", log_file="example.log", log_timestamp=True)
    print(f"Message was also logged to 'example.log'")


def demonstrate_all_themes():
    """Demonstrate all available themes."""
    print("\n=== All Available Themes ===")

    # Sample data to display with each theme
    sample_data = {
        "string": "This is a string",
        "number": 42,
        "list": [1, 2, 3, "mixed", True],
        "dict": {"key": "value", "nested": {"data": ["structure"]}}
    }

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

    # Demonstrate each theme
    for theme_name, theme_style in themes:
        print(f"\n--- {theme_name} Theme ---")
        lit.style = theme_style
        lit(f"Using {theme_name} theme:", sample_data)

    # Reset to CYBERPUNK theme
    lit.style = CYBERPUNK
    print("\n(Reset to CYBERPUNK theme)")


def demonstrate_custom_theme():
    """Demonstrate custom theme creation."""
    print("\n=== Custom Theme Example ===")

    # Create a custom theme
    matrix_theme = create_custom_style(
        "MatrixTheme",
        {
            Text: "#00ff00",      # Matrix-green text
            String: "#88ff88",    # Light green strings
            Number: "#ffffff",    # White numbers
        }
    )

    # Use the custom theme
    lit.style = matrix_theme
    lit("Using custom 'Matrix' theme:",
        "This is a string",
        42,
        {"nested": ["data", "structure"]})

    # Reset to CYBERPUNK theme
    lit.style = CYBERPUNK
    lit("Back to CYBERPUNK theme")


def demonstrate_builtins_integration():
    """Demonstrate builtins integration."""
    print("\n=== Builtins Integration Example ===")

    # Install to builtins
    install()

    # Now we can use ic() directly without importing
    print("Using ic() from builtins:")
    ic("This works without import!") # type: ignore

    # Uninstall from builtins
    uninstall()

    print("Uninstalled from builtins")


def demonstrate_vscode_integration():
    """Demonstrate VS Code integration with clickable links."""
    print("\n=== VS Code Integration Example ===")

    # Use absolute path to create clickable links in VS Code
    lit("This output includes a clickable link to the source location", contextAbsPath=True)

    print("(If you're using VS Code, you can click on the file path in the output above)")


if __name__ == "__main__":
    print("LitPrinter Advanced Usage Examples")

    demonstrate_custom_formatter()
    demonstrate_logging()
    demonstrate_all_themes()  # Show all available themes
    demonstrate_custom_theme()
    demonstrate_builtins_integration()
    demonstrate_vscode_integration()

    # Run the traceback example last since it raises an exception
    demonstrate_traceback()
