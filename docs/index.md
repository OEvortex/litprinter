# LitPrinter Documentation

Welcome to the LitPrinter documentation!

LitPrinter is the most sophisticated debug printing library for Python - a powerful fusion of **IceCream** and **Rich** with beautiful formatting, syntax highlighting, and gorgeous tracebacks.

## Installation

```bash
pip install litprinter
```

## Quick Start

```python
# No import needed after pip install!
x = 42
ic(x)  # Output: ic| x: 42
```

That's it! After installing, `ic()` is automatically available in all your Python scripts - no import required!

## Why LitPrinter?

LitPrinter combines the best of two worlds:

| Feature | print() | IceCream | LitPrinter |
|---------|---------|----------|------------|
| Shows variable names | ❌ | ✅ | ✅ |
| Syntax highlighting | ❌ | ❌ | ✅ |
| Rich-style panels | ❌ | ❌ | ✅ |
| Pretty tracebacks | ❌ | ❌ | ✅ |
| Context (file/line) | ❌ | ✅ | ✅ |
| Configurable output | ❌ | ✅ | ✅ |
| Enable/disable | ❌ | ✅ | ✅ |

## Core Features

### IceCream-Compatible API

```python
from litprinter import ic

# Basic usage - shows variable names and values
x, y = 10, 20
ic(x, y)  # Output: ic| x: 10, y: 20

# Works with expressions
ic(x * 2)  # Output: ic| x * 2: 20

# Empty call shows timestamp
ic()  # Output: ic| 11:30:47.532

# Returns values for inline use
result = ic(calculate(x))  # Prints AND returns the value
```

### Configuration

```python
from litprinter import ic

# Change the prefix
ic.configureOutput(prefix='DEBUG| ')
ic(x)  # Output: DEBUG| x: 10

# Show file/line/function context
ic.configureOutput(includeContext=True)
ic(x)  # Output: DEBUG| [script.py:5 in my_function()] >>> x: 10

# Use absolute paths
ic.configureOutput(contextAbsPath=True)
ic(x)  # Output: DEBUG| [C:\Users\koula\Desktop\litprinter\test_ic.py:5 in my_function()] >>> x: 10

# Custom output function (e.g., to a logger)
ic.configureOutput(outputFunction=my_logger.debug)
ic(x)  # Output: DEBUG| x: 10

# Custom argument formatting
ic.configureOutput(argToStringFunction=my_formatter)
ic(x)  # Output: DEBUG| x: 10
```

### Enable/Disable

```python
from litprinter import ic

# Disable output (values still pass through)
ic.disable()
result = ic(calculate())  # Silent, but returns value

# Re-enable output
ic.enable()
ic("I'm back!")  # Output: ic| "I'm back!"
```

### Format Without Printing

```python
from litprinter import ic

# Get formatted string without printing
formatted = ic.format(x, y)
my_logger.debug(formatted)
ic(x)  # Output: DEBUG| x: 10
```

### Per-Call Context Override

```python
from litprinter import ic

# Override includeContext for a single call
ic(x, includeContext=True)  # Shows context for this call only
```

## Rich-Style Console

LitPrinter includes a Rich-compatible Console for styled output:

```python
from litprinter import Console

console = Console()

# Rich-style markup
console.print("[bold red]Error:[/bold red] Something went wrong!")

# Log with timestamp and location
console.log("Processing started")

# Horizontal rules
console.rule("Section Header")

# JSON with highlighting
console.print_json({"name": "Alice", "age": 30})
```

## Beautiful Panels

```python
from litprinter import Panel

# Basic panel
panel = Panel("Hello, World!", title="Greeting")
print(panel)
# Output:
# ╭ Greeting ────────╮
# │ Hello, World!    │
# ╰──────────────────╯

# Fitted panel (doesn't expand)
panel = Panel.fit("Short text", title="Fitted")
```

## Pretty Tracebacks

```python
from litprinter.traceback import install

# Install globally
install(
    theme="cyberpunk",      # Color theme
    show_locals=True,       # Show local variables
    extra_lines=3,          # Context around error
)

# Now all exceptions show beautiful tracebacks!
```

## Builtins Installation

Make `ic()` available globally without imports (just like IceCream):

```python
from litprinter import install

install()

# Now works anywhere without import:
ic(x)  # Available globally!
```

## API Reference

### `ic(*args, **kwargs)`

Debug print arguments and return them.

**Parameters:**
- `*args`: Values to debug print
- `includeContext`: Override context setting for this call
- `contextAbsPath`: Override path setting for this call

**Returns:** 
- `None` if no args
- Single value if one arg
- Tuple if multiple args

### `ic.configureOutput(**kwargs)`

Configure output settings.

**Parameters:**
- `prefix`: String or callable returning prefix
- `outputFunction`: Function to call with formatted output
- `argToStringFunction`: Function to convert args to strings
- `includeContext`: Show file/line/function context
- `contextAbsPath`: Use absolute paths in context

### `ic.enable()` / `ic.disable()`

Enable or disable debug output. When disabled, `ic()` still returns values but produces no output.

### `ic.format(*args)`

Format arguments without printing. Returns the formatted string.

### `argumentToString(obj)`

Convert an object to string representation. Supports singledispatch for custom types:

```python
from litprinter import argumentToString

class MyClass:
    def __init__(self, name):
        self.name = name

@argumentToString.register(MyClass)
def format_myclass(obj):
    return f"MyClass({obj.name})"
```

## Available Themes

For tracebacks and syntax highlighting:

- **JARVIS** - Inspired by Iron Man's AI
- **RICH** - Balanced and readable
- **MODERN** - Subtle with good contrast
- **NEON** - Vibrant neon colors
- **CYBERPUNK** - Pinks, blues, and yellows
- **DRACULA** - Popular dark theme
- **MONOKAI** - Classic color scheme
- **SOLARIZED** - Low-contrast theme
- **NORD** - Arctic-inspired colors
- **GITHUB** - GitHub's color scheme
- **VSCODE** - VS Code inspired
- **MATERIAL** - Material design colors
- **RETRO** - Nostalgic colors
- **OCEAN** - Cool blue tones
- **AUTUMN** - Warm fall colors
- **SYNTHWAVE** - 80s inspired
- **FOREST** - Natural greens
- **MONOCHROME** - Black and white
- **SUNSET** - Warm orange tones

## Migration from IceCream

LitPrinter is a drop-in replacement for IceCream:

```python
# Before
from icecream import ic

# After
from litprinter import ic
```

All IceCream features work identically:
- `ic(x)` - Debug print
- `ic.configureOutput(...)` - Configure
- `ic.disable()` / `ic.enable()` - Toggle
- `ic.format(...)` - Format without print

Plus you get:
- Syntax highlighting
- Rich-style panels and console
- Beautiful tracebacks
- 19 color themes

## Version

Current version: **0.3.0**

For more examples, see the [GitHub repository](https://github.com/OEvortex/litprinter).
