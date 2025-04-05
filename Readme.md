<div align="center">
  <a href="https://github.com/OEvortex/litprinter">
    <img src="https://img.shields.io/badge/LitPrinter-Beautiful%20Debug%20Printing-blue?style=for-the-badge&logo=python&logoColor=white" alt="LitPrinter Logo">
  </a>
  <br/>
  <h1>🔥 LitPrinter</h1>
  <p><strong>The most sophisticated debug printing library for Python with rich formatting, syntax highlighting, and beautiful tracebacks.</strong></p>
  <p>
    Turn your debugging experience from mundane to magnificent with color themes, context-aware output, smart formatting, and powerful traceback handling.
  </p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/pypi/v/litprinter.svg?style=flat-square&logo=pypi&label=PyPI" alt="Version">
    <img src="https://img.shields.io/badge/python-3.6+-brightgreen.svg?style=flat-square&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square" alt="License">
    <img src="https://img.shields.io/badge/pygments-required-purple.svg?style=flat-square" alt="Dependencies">
  </p>
</div>

## 🚀 Introduction

LitPrinter is an enhanced debugging tool for Python that provides beautiful, informative output in your terminal. Inspired by the `icecream` package, LitPrinter takes debugging to the next level with context-aware output, syntax highlighting, and powerful formatting options.

```python
from litprinter import lit

# Print variables with their names and values
x, y = 10, 20
lit(x, y)  # Prints: LIT| [script.py:6] in () >>> x: 10, y: 20
```

## ✨ Features

### 🎨 Rich Syntax Highlighting

```python
# Choose from multiple color themes
from litprinter import lit
lit.color_style = "CYBERPUNK"  # Options: JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI

# Or use as a parameter
lit(my_complex_object, color_style="NEON")
```

### 📊 Smart Object Formatting

```python
# Automatically pretty-formats different data types
data = {
    "users": ["alice", "bob", "charlie"],
    "active": True,
    "settings": {
        "theme": "dark",
        "notifications": True
    }
}
lit(data)  # Formatted with proper indentation and syntax highlighting
```

### 🔍 Context-Aware Output

```python
# Shows file, line number, and function name
def calculate_total(a, b):
    lit(a, b)  # Shows: LIT| [script.py:3] in calculate_total() >>> a: 10, b: 20
    return a + b
```

### 🧵 Inline Usage

```python
# Use in-line without disrupting your code flow
def get_user(user_id):
    user = database.find(user_id)
    return lit(user)  # Both prints and returns the value
```

### 📝 Logging Support

```python
from litprinter import log

# Different log levels
log("System starting...", level="info")
log("Debug information", level="debug")
log("Warning: disk space low", level="warning")
log("Critical error occurred", level="error")
```

### 💥 Beautiful Traceback Handling

```python
from litprinter.traceback import install as install_traceback

# Replace Python's default traceback with beautiful, colorful tracebacks
install_traceback(
    theme="cyberpunk",  # Use any theme: JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI
    show_locals=True,   # Show local variables in each frame
    extra_lines=3       # Show extra context lines around error
)

# Now any exceptions will be displayed with beautiful formatting
def example():
    x = {"test": [1, 2, 3]}
    y = x["not_found"]  # This will raise a KeyError with beautiful traceback
```

### 🛠️ Advanced Traceback Options

```python
from litprinter.traceback import install, PrettyTraceback

# Basic installation with defaults
install()

# Advanced configuration
install(
    extra_lines=5,            # Show 5 lines of context around errors
    theme="dracula",          # Use Dracula theme
    show_locals=True,         # Show local variables
    locals_max_length=150,    # Limit local variable display length
    locals_max_depth=3,       # How deep to format nested structures
    locals_hide_dunder=True,  # Hide __dunder__ variables
    width=120                 # Terminal width for formatting
)

# Or use PrettyTraceback directly for one-time use
try:
    risky_operation()
except Exception as e:
    tb = PrettyTraceback(type(e), e, e.__traceback__, theme="neon", show_locals=True)
    tb.print()
```

### ⚙️ Highly Customizable

```python
from litprinter import lit, argumentToString

# Register custom formatters for your types
@argumentToString.register(MyCustomClass)
def format_my_class(obj):
    return f"MyClass(id={obj.id}, name='{obj.name}')"

# Customize output format
lit(my_object,
    prefix="DEBUG >>> ",
    includeContext=True,
    contextAbsPath=True,
    disable_colors=False)
```

## 🛠️ Installation

```bash
pip install -U litprinter
```

Or for direct access to LitPrinter's functions:

```python
# Install as builtins for convenience
from litprinter import install
install()  # Now 'litprint' and 'ic' are available globally
```

## 📖 API Overview

### Main Functions

| Function | Description |
|----------|-------------|
| `lit(*args, **kwargs)` | Primary debugging function with variable inspection |
| `litprint(*args, **kwargs)` | Alias for `lit` with similar behavior |
| `log(*args, level="debug", **kwargs)` | Logging with level support |
| `install(name='litprint', ic='ic')` | Install functions as builtins |
| `uninstall(name='litprint', ic='ic')` | Remove from builtins |

### Traceback Module Functions

| Function | Description |
|----------|-------------|
| `traceback.install(**kwargs)` | Replace default Python traceback with pretty version |
| `traceback.uninstall()` | Restore original Python traceback handler |
| `PrettyTraceback(exc_type, exc_value, tb, **kwargs)` | Create traceback formatter instance |

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prefix` | str | Custom prefix for output lines |
| `color_style` | str/dict | Color theme or custom colors |
| `includeContext` | bool | Show file/line/function context |
| `contextAbsPath` | bool | Use absolute paths in context |
| `disable_colors` | bool | Turn off syntax highlighting |
| `log_file` | str | File to write output to |
| `log_timestamp` | bool | Include timestamps in output |

## 📚 Examples

### Debug Print with Context

```python
from litprinter import lit

def process_user_data(user):
    name = user.get('name', 'Unknown')
    age = user.get('age', 0)

    # Debug print shows variable names, values, and source location
    lit(name, age)  # Shows: LIT| [users.py:6] in process_user_data() >>> name: 'John', age: 30

    # Process the data...
```

### Custom Traceback Theme

```python
from litprinter.traceback import install
from litprinter.coloring import create_custom_style
from pygments.token import Text, String, Number

# Create a cyberpunk-inspired output for tracebacks
install(theme="CYBERPUNK", show_locals=True)

# Or define a completely custom style for tracebacks
custom_colors = {
    Text: "#00ff00",      # Matrix-green text
    String: "#ff00ff",    # Magenta strings
    Number: "#ffff00"     # Yellow numbers
}
custom_style = create_custom_style("MatrixStyle", custom_colors)
install(theme="custom", _selected_pygments_style_cls=custom_style)

# Now any exceptions will use your custom coloring
```

### Integration with Error Handling

```python
try:
    result = complex_operation()
except Exception as e:
    lit(e)  # Pretty-prints the exception with traceback highlighting
    raise
```

### Log to File

```python
from litprinter import lit

# Log to both console and file
lit("Initializing system...", log_file="app.log", log_timestamp=True)
```

## 🧩 Integration with VS Code and Other Editors

LitPrinter creates clickable links in supported terminals and editors. In VS Code, clicking on the file path in the output will open the file at the exact line.

```python
lit(data, contextAbsPath=True)  # Creates clickable link to source line
```

For tracebacks, the file paths are also clickable, making it easy to jump to the error location:

```python
from litprinter.traceback import install
install(show_locals=True)

# When an exception occurs, you can click the file paths in the traceback
```

## 🧠 Why Choose LitPrinter?

- 🚀 **All-in-one solution**: Combines debugging, logging, formatting and traceback enhancement
- 🎨 **Beautiful output**: Makes debugging more pleasant with syntax highlighting
- 🔍 **Context-aware**: Automatically shows where the call was made from
- 🧠 **Smart handling**: Special formatters for complex data types
- 🔄 **Flow-friendly**: Use inline without disrupting your code
- 🛠️ **Extensible**: Register custom formatters for your types
- 💥 **Enhanced tracebacks**: Transform boring Python tracebacks into beautiful, informative displays

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues on the [LitPrinter GitHub repository](https://github.com/OEvortex/litprinter).

See the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details on how to contribute to this project.

<div align="center">

---

<p>
Made with ❤️ by OEvortex
</p>

<div align="center">
  <a href="https://t.me/PyscoutAI"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  <a href="https://www.instagram.com/oevortex/"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/oe-vortex-29a407265/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://buymeacoffee.com/oevortex"><img alt="Buy Me A Coffee" src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black"></a>
</div>

</div>
