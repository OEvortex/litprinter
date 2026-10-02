<div align="center">
  <a href="https://github.com/OEvortex/litprinter">
    <img src="https://img.shields.io/badge/LitPrinter-IceCream%20+%20Rich-blue?style=for-the-badge&logo=python&logoColor=white" alt="LitPrinter Logo">
  </a>
  <br/>
  <h1>🔥 LitPrinter</h1>
  <p><strong>IceCream + Rich = LitPrinter — The ultimate debug printing library for Python</strong></p>
  <p>
    A powerful fusion of IceCream-style debugging with Rich-style formatting, syntax highlighting, and beautiful tracebacks.
  </p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/pypi/v/litprinter.svg?style=flat-square&logo=pypi&label=PyPI" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8+-brightgreen.svg?style=flat-square&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square" alt="License">
    <img src="https://img.shields.io/badge/IceCream-compatible-cyan.svg?style=flat-square" alt="IceCream Compatible">
  </p>
</div>

## 🚀 Why LitPrinter?

LitPrinter is a **drop-in replacement for IceCream** with additional Rich-style features:

| Feature | print() | IceCream | LitPrinter |
|---------|---------|----------|------------|
| Shows variable names | ❌ | ✅ | ✅ |
| Syntax highlighting | ❌ | ✅ | ✅ |
| Rich-style panels | ❌ | ❌ | ✅ |
| Pretty tracebacks | ❌ | ❌ | ✅ |
| Configurable colors | ❌ | ❌ | ✅ |
| Enable/disable toggle | ❌ | ✅ | ✅ |

## ⚡ Quick Start

```bash
pip install litprinter
```

```python
# No import needed! ic is automatically available
x = 42
ic(x)  # Output: ic| x: 42
```

That's it! After installing, `ic()` is automatically available in all your Python scripts - no import required!

## 🎯 IceCream-Compatible API

LitPrinter is fully compatible with IceCream's API:

```python
from litprinter import ic

# Basic debugging
x, y = 10, 20
ic(x, y)  # ic| x: 10, y: 20

# Works with expressions
ic(x * 2)  # ic| x * 2: 20

# Configure output
ic.configureOutput(prefix='DEBUG| ')
ic.configureOutput(includeContext=True)

# Enable/disable
ic.disable()  # Silent, but still returns values
ic.enable()   # Re-enable output

# Format without printing
s = ic.format(x, y)
```

## 🎨 Color Themes

LitPrinter includes multiple color themes:

```python
from litprinter import ic, set_style, SolarizedDark, LitStyle, CyberpunkStyle, MonokaiStyle

# Default is SolarizedDark (IceCream-compatible)
ic(x)

# Switch to vibrant LitStyle
set_style(LitStyle)
ic(x)

# Try neon Cyberpunk
set_style(CyberpunkStyle)
ic(x)

# Classic Monokai
set_style(MonokaiStyle)
ic(x)
```

**Available Themes:**
- `SolarizedDark` - IceCream-compatible (default)
- `LitStyle` - Vibrant and modern
- `CyberpunkStyle` - Neon pink, teal, green
- `MonokaiStyle` - Classic code editor theme

## ✨ Features

### 📊 Smart Object Formatting

```python
data = {
    "users": ["alice", "bob"],
    "settings": {"theme": "dark"}
}
ic(data)  # Formatted with proper indentation and highlighting
```

### 🔍 Context-Aware Output

```python
def calculate_total(a, b):
    ic(a, b, includeContext=True)
    # Output: ic| [script.py:3 in calculate_total()] >>> a: 10, b: 20
    return a + b
```

### 🧵 Inline Usage

```python
# Use inline - ic() returns the value
result = ic(calculate(x))  # Prints AND returns the value
```

### 💥 Beautiful Tracebacks

```python
from litprinter.traceback import install

install(
    theme="cyberpunk",
    show_locals=True,
    extra_lines=3
)

# Now all exceptions show beautiful tracebacks!
```

### 🖼️ Rich-Style Panels

```python
from litprinter import Panel, Console

# Create bordered panels
panel = Panel("Hello, World!", title="Greeting")
print(panel)

# Rich-style console
console = Console()
console.print("[bold red]Error:[/bold red] Something went wrong!")
```

## 🔧 Configuration

### Global Configuration

```python
from litprinter import ic

ic.configureOutput(
    prefix='DEBUG| ',           # Custom prefix
    includeContext=True,        # Show file/line/function
    contextAbsPath=False,       # Use relative paths
    outputFunction=my_logger,   # Custom output function
)
```

### Per-Call Override

```python
ic(x, includeContext=True)  # Override for this call only
```

### Custom Formatters

```python
from litprinter import argumentToString

class MyClass:
    def __init__(self, name):
        self.name = name

@argumentToString.register(MyClass)
def format_myclass(obj):
    return f"MyClass({obj.name})"

ic(MyClass("test"))  # ic| MyClass(test)
```

## 🌐 Always Available

After `pip install litprinter`, `ic()` is **automatically available** in all Python scripts - no import needed!

```python
# my_script.py - no import required!
x = 42
ic(x)  # Just works!
```

If you want to temporarily disable:
```python
from litprinter import uninstall
uninstall()  # Remove ic from builtins

# To re-enable:
from litprinter import install
install()
```

## 📦 Migration from IceCream

Just change your import:

```python
# Before
from icecream import ic

# After
from litprinter import ic
```

All IceCream features work identically, plus you get:
- Multiple color themes
- Rich-style panels and console
- Beautiful tracebacks
- Panel rendering

## 📚 API Reference

### Main Functions

| Function | Description |
|----------|-------------|
| `ic(*args)` | Debug print with variable names |
| `ic.configureOutput(...)` | Configure output settings |
| `ic.disable()` / `ic.enable()` | Toggle output |
| `ic.format(*args)` | Format without printing |
| `set_style(style)` | Set color theme |

### Aliases

| Alias | Same as |
|-------|---------|
| `LIT` | `ic` |
| `litprint` | `ic` |
| `lit` | `ic` |

### Traceback Functions

| Function | Description |
|----------|-------------|
| `traceback.install(**kwargs)` | Install pretty tracebacks |
| `traceback.uninstall()` | Restore default tracebacks |
| `PrettyTraceback(...)` | Create traceback formatter |

## 🆕 What's New in v0.3.0

- **IceCream-compatible API**: Full `ic.configureOutput()`, `ic.disable()`, `ic.enable()` support
- **Multiple color themes**: SolarizedDark, LitStyle, CyberpunkStyle, MonokaiStyle
- **Style switching**: `set_style()` to change colors at runtime
- **Rich-style features**: Console, Panel, styled text
- **Pretty tracebacks**: Frame suppression, max_frames, Rich protocols
- **Dynamic versioning**: Version from `__init__.py`
- **Cleaner codebase**: Removed duplicate code, simplified architecture

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

<div align="center">

---

<p>Made with ❤️ by OEvortex</p>

<div align="center">
  <a href="https://t.me/PyscoutAI"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  <a href="https://www.instagram.com/oevortex/"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/oe-vortex-29a407265/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://buymeacoffee.com/oevortex"><img alt="Buy Me A Coffee" src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black"></a>
</div>

</div>
