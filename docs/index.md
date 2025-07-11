# LitPrinter Documentation

Welcome to the LitPrinter documentation!

LitPrinter is the most sophisticated debug printing library for Python with rich formatting, syntax highlighting, and beautiful tracebacks. It's designed to make debugging more pleasant and productive with features like context-aware output, smart formatting, and powerful traceback handling.

## Installation

```bash
pip install litprinter
```

## Basic Usage

```python
from litprinter import litprint, lit

# Basic usage
litprint("Hello, world!")
# Output: LIT -> [script.py:3] in () >>> Hello, world!

# Print variables with their names
x, y = 10, 20
lit(x, y)
# Output: LIT -> [script.py:7] in () >>> x: 10, y: 20

# Use in functions
def my_function(a, b):
    lit(a, b)
    return a + b

result = my_function(5, 10)
# Output: LIT -> [script.py:12] in my_function() >>> a: 5, b: 10
```

## Features

- Variable inspection with expression display
- Return value handling for inline usage
- Support for custom formatters for specific data types
- Execution context tracking
- Rich-like colorized output with multiple themes (JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI)
- Better JSON formatting with indent=2 by default
- Advanced pretty printing for complex data structures with smart truncation
- Clickable file paths in supported terminals and editors (VSCode compatible)
- Enhanced visual formatting with better spacing and separators
- Special formatters for common types (Exception, bytes, set, frozenset, etc.)
- Smart object introspection for custom classes
- Logging capabilities with timestamp and log levels
- **Performance optimizations** with style caching system
- **Cross-platform compatibility** with enhanced Windows support and colorama integration
- **Memory management** with cache control utilities
- **Standards compliance** with NO_COLOR environment variable support
- **Robust error handling** with graceful fallbacks for invalid styles

## API Reference

### Main Functions

#### litprint

```python
from litprinter import litprint

litprint(*args, **kwargs)
```

The `litprint` function is an enhanced print function for debugging purposes. It displays the values of the provided arguments along with context information (file, line number, function name).

Key parameters:
- `prefix`: Custom prefix for output lines (default: "LIT -> ")
- `includeContext`: Show file/line/function context (default: True)
- `contextAbsPath`: Use absolute paths in context (default: False)
- `disable_colors`: Turn off syntax highlighting (default: False)
- `log_file`: File to write output to (default: None)
- `log_timestamp`: Include timestamps in output (default: False)

#### lit

```python
from litprinter import lit

lit(*args, **kwargs)
```

The `lit` function is similar to `litprint` but with enhanced variable inspection. It shows both the variable names and their values.

It accepts the same parameters as `litprint` and returns the last argument, making it suitable for inline usage.

#### log

```python
from litprinter import log

log(*args, level="debug", **kwargs)
```

The `log` function is a logging utility that adds timestamp and log level information to the output.

Key parameters:
- `level`: Log level ("debug", "info", "warning", "error", "critical")
- All parameters from `litprint` are also supported

#### install/uninstall

```python
from litprinter import install, uninstall

install(name="litprint", ic="ic")
uninstall(name="litprint", ic="ic")
```

These functions install/uninstall LitPrinter functions into the Python builtins module, making them available globally without imports.

- `name`: Name of the function to install in builtins (default: "litprint")
- `ic`: Name of the icecream-compatible function to install (default: "ic")

### Themes and Styling

```python
from litprinter import JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI, create_custom_style

# Use a predefined theme
lit.style = NEON

# Create a custom theme
my_style = create_custom_style(
    primary_color="#FF5733",
    secondary_color="#33FF57",
    accent_color="#5733FF"
)
lit.style = my_style
```

LitPrinter comes with several built-in themes:

- **JARVIS**: A Tron-inspired theme with black background and vibrant cyan/green/magenta highlights
- **RICH**: A rich-text inspired theme with balanced colors for good readability
- **MODERN**: A modern theme with subtle colors and good contrast
- **NEON**: A vibrant neon theme with bright colors on dark background
- **CYBERPUNK**: A cyberpunk-inspired theme with bright pinks, blues, and yellows
- **DRACULA**: A dark theme inspired by the popular Dracula color scheme
- **MONOKAI**: A theme based on the classic Monokai color scheme

You can also create custom themes using the `create_custom_style` function, which allows you to specify colors for different syntax elements.

### Builtins Integration

```python
from litprinter import install, uninstall

# Install to builtins
install()

# Now you can use ic() directly
ic("This works without import!")

# Uninstall from builtins
uninstall()
```

## Advanced Usage

### Traceback Enhancement

LitPrinter includes a powerful traceback enhancement module that makes Python's error messages more readable and informative:

```python
from litprinter.traceback import install

# Basic installation
install()

# Advanced configuration
install(
    theme="CYBERPUNK",       # Choose from JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI
    show_locals=True,        # Show local variables in each frame
    extra_lines=3,           # Show extra context lines around error
    locals_max_length=150,   # Limit local variable display length
    locals_max_depth=3,      # How deep to format nested structures
    locals_hide_dunder=True, # Hide __dunder__ variables
    width=120                # Terminal width for formatting
)
```

### Custom Formatters

You can register custom formatters for your own types:

```python
from litprinter import argumentToString

class MyCustomClass:
    def __init__(self, id, name):
        self.id = id
        self.name = name

@argumentToString.register(MyCustomClass)
def format_my_class(obj):
    return f"MyClass(id={obj.id}, name='{obj.name}')"

# Now LitPrinter will use your custom formatter
my_obj = MyCustomClass(42, "Example")
lit(my_obj)  # Will display using your custom formatter
```

### Logging to File

You can log output to a file in addition to the console:

```python
from litprinter import lit

# Log to both console and file
lit("Important debug info", log_file="debug.log", log_timestamp=True)
```

### Performance and System Utilities

LitPrinter includes several utility functions for performance management and system compatibility:

```python
from litprinter.core import clearStyleCache, getStyleCacheInfo, isTerminalCapable

# Check cache status
cache_info = getStyleCacheInfo()
print(f"Cache size: {cache_info['cache_size']}")
print(f"Cached styles: {cache_info['cached_styles']}")

# Clear cache for memory management
clearStyleCache()

# Check terminal capabilities (respects NO_COLOR environment variable)
if isTerminalCapable():
    print("Terminal supports colors")
else:
    print("Terminal does not support colors or NO_COLOR is set")
```

#### Available Utility Functions

| Function | Description |
|----------|-------------|
| `clearStyleCache()` | Clear the style formatter cache for memory management |
| `getStyleCacheInfo()` | Get cache statistics and currently cached styles |
| `isTerminalCapable()` | Check if terminal supports color output (respects NO_COLOR standard) |

### Cross-Platform Compatibility

LitPrinter automatically handles cross-platform differences and provides robust compatibility features:

```python
# LitPrinter automatically handles cross-platform differences:
# - Detects Windows terminal capabilities and initializes colorama
# - Respects NO_COLOR environment variable standard
# - Uses proper path normalization across platforms
# - Gracefully falls back to plain text when colors aren't supported

import os
os.environ['NO_COLOR'] = '1'  # Disable colors globally
lit("This will be plain text")  # No colors will be applied
```

**Cross-platform features:**
- Windows terminal detection with automatic colorama initialization
- NO_COLOR environment variable support for accessibility
- Cross-platform path normalization using `os.path.normpath()`
- Graceful fallbacks when color support is unavailable
- Robust error handling for different terminal environments

### Integration with VS Code

LitPrinter creates clickable links in supported terminals and editors. In VS Code, clicking on the file path in the output will open the file at the exact line.

```python
lit(data, contextAbsPath=True)  # Creates clickable link to source line
```

## Recent Improvements

### Code Quality & Performance (v0.2.0)
- **90% Code Duplication Eliminated**: Consolidated `lit.py` and `litprint.py` implementations
- **Enhanced Cross-Platform Support**: Improved Windows terminal detection and colorama integration
- **Performance Optimizations**: Added style caching system for better performance
- **Memory Management**: New cache control functions for production environments
- **Standards Compliance**: Full NO_COLOR environment variable support
- **Robust Error Handling**: Graceful fallbacks for invalid styles and edge cases
- **Import Fixes**: Resolved module import issues for better package compatibility

These improvements make LitPrinter more maintainable, performant, and reliable across different platforms and environments.

### Traceback Module API

```python
from litprinter.traceback import install, uninstall, PrettyTraceback
```

#### install

```python
install(theme="RICH", show_locals=True, extra_lines=2, **kwargs)
```

Replaces Python's default traceback handler with LitPrinter's enhanced version.

Key parameters:
- `theme`: Color theme to use ("JARVIS", "RICH", "MODERN", "NEON", "CYBERPUNK", "DRACULA", "MONOKAI")
- `show_locals`: Whether to show local variables in each frame
- `extra_lines`: Number of context lines to show around the error
- `locals_max_length`: Maximum length for local variable display
- `locals_max_depth`: Maximum depth for nested structures
- `locals_hide_dunder`: Whether to hide __dunder__ variables
- `width`: Terminal width for formatting

#### uninstall

```python
uninstall()
```

Restores Python's original traceback handler.

#### PrettyTraceback

```python
tb = PrettyTraceback(exc_type, exc_value, traceback, **kwargs)
tb.print()
```

Creates a traceback formatter instance for one-time use. Accepts the same parameters as `install()`.

For more advanced usage examples, see the [README.md](https://github.com/OEvortex/litprinter).
