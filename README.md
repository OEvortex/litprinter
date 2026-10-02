<div align="center">
  <a href="https://github.com/OEvortex/litprinter">
    <img src="https://img.shields.io/badge/LitPrinter-print%20%2B%20debug-blue?style=for-the-badge&logo=python&logoColor=white" alt="LitPrinter Logo">
  </a>
  <br/>
  <h1>🔥 LitPrinter</h1>
  <p><strong>The debug printer that replaces print(), logging and icecream</strong></p>
  <p>
    One tool for your terminal: smart debugging, a drop-in <code>print()</code>,
    logging without <code>logging</code>, and beautiful tracebacks.
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

| Feature | `print()` | IceCream | logging | LitPrinter |
|---------|-----------|----------|---------|------------|
| Shows variable names | ❌ | ✅ | ❌ | ✅ |
| Replaces `print()` | ❌ | ❌ | ❌ | ✅ |
| Colored markup output | ❌ | ❌ | ❌ | ✅ |
| Auto context when useful | ❌ | ❌ | ✅ | ✅ |
| Pretty tracebacks | ❌ | ❌ | ❌ | ✅ |
| Zero-import (works everywhere) | — | ❌ | — | ✅ |

## ⚡ Quick Start

```bash
pip install litprinter
```

```python
# No import needed! ic is automatically available
x = 42
ic(x)                      # ic| x: 42
ic.print("hello", x)       # hello 42
ic.info("server started")  # INFO  server started
```

That's it. After `pip install litprinter`, `ic` is available in **every** Python
script — no import required.

> Editors: this repo ships a patched typeshed (`.typeshed`) so `ic` is typed as
> a real builtin for ty, Pylance/pyright and mypy, with hover docs and
> completions like `print()`.

## 🐛 Debugging that explains itself

```python
def calculate(a, b):
    total = a + b
    ic(total)              # ic| total: 30        <- name is obvious, no noise
    ic(total / len(items)) # ic| [app.py:3 in calculate()] >>> total / len(items): 10.0
    ic()                   # ic| app.py:3 in calculate() - 14:02:11.004
    return total

ic(total * 2)             # ic| [app.py:9] >>> total * 2: 60  <- module level: no `in <module>`
```

At module level (the top level of a script) there is no enclosing function, so
the context is just `file:line`. Inside a function it also names the function.

Context is added **only when it helps**:

| Call | Context shown? | Why |
|------|----------------|-----|
| `ic(x)` | no | the name is already printed |
| `ic(x + 1)` | yes | the expression matters |
| `ic(items[0])` | yes | needs a location |
| `ic(f"hi {name}")` | no | the value is self-describing |
| `ic()` | yes | acts as a "where am I" breadcrumb |

Override it any time:

```python
ic(x, includeContext=True)   # force context for this call
ic(x, includeContext=False)  # suppress context for this call

ic.configureOutput(contextMode="always")  # 'auto' (default) | 'always' | 'never'
```

## 🖨️ `ic.print` — drop-in `print()` replacement

Same signature as builtin `print()`, so you can sed-replace `print(` → `ic.print(`:

```python
ic.print("plain")                                   # plain
ic.print("a", "b", sep=" | ", end="!\n")            # a | b!
ic.print("to stderr", file=sys.stderr, flush=True)

# Inline markup (Rich-style tags, zero dependencies)
ic.print("[bold red]ERROR[/bold red] connection refused")
ic.print("[on_blue] INFO [/on_blue] listening on :8080")
ic.print("styled", style="bold cyan")

# Syntax highlight non-string values
ic.print({"port": 8080, "host": "0.0.0.0"}, highlight=True)

# Disable markup if your data contains brackets
ic.print("[not markup]", markup=False)
```

Supported tags: `bold`, `dim`, `italic`, `underline`, `strike`, `reverse`,
`blink`, the 8/16 colors (`red`, `bright_red`, …), backgrounds (`on_blue`, …),
`#ff8800` hex colors, `rgb(255,0,0)`, and `[/]` to close.

`litprinter.print` is exported too, so `from litprinter import print` works.

## 📋 Logging without `logging`

```python
ic.debug("cache miss", key)
ic.info("connected", url)
ic.success("migration complete")
ic.warning("retrying in 5s", attempt=2)
ic.error("request failed", status=500)
ic.critical("disk full")

# Or generic
ic.log("custom level line", level="info")
ic.log("with timestamp", level="warn", timestamp=True)

# Or module-level
from litprinter import log
log("hello", level="info")
```

Levels: `debug`, `info`, `success`, `warning`/`warn`, `error`, `critical`.
Output goes to stderr so it stays out of your piped stdout.

## 🧵 Inline usage

```python
result = ic(calculate(x))  # prints AND returns the value
```

## 🎨 Themes

```python
from litprinter import ic, set_style, LitStyle, CyberpunkStyle, MonokaiStyle

ic(x)
set_style(LitStyle)       # vibrant and modern
ic(x)
set_style(CyberpunkStyle) # neon
set_style(MonokaiStyle)   # classic code editor
```

Available: `TokyoNight` (default), `SolarizedDark`, `LitStyle`,
`CyberpunkStyle`, `MonokaiStyle`.

## 💥 Beautiful tracebacks

```python
from litprinter import traceback

traceback.install(
    theme="cyberpunk",
    show_locals=True,
    extra_lines=3,
)
```

Shows syntax-highlighted source, local variables, and a clean layout for
uncaught exceptions.

## 🔧 Configuration

```python
ic.configureOutput(
    prefix="dbg| ",            # custom prefix
    contextMode="auto",        # 'auto' | 'always' | 'never'
    contextAbsPath=False,      # relative paths in context
    pairDelimiter=", ",        # separator between debugged values
    outputFunction=my_logger,  # send output anywhere
)

ic.disable()   # silent, but still returns values
ic.enable()
s = ic.format(x, y)   # format without printing
```

### Custom formatters

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

## 🔁 Migration

From **IceCream**:

```python
# before
from icecream import ic
# after: nothing to do - ic is already a builtin after install
```

From **`print()`**:

```python
# before
print(f"user: {user['name']}")
# after - shows the expression, no f-string needed
ic(user["name"])
```

From **`logging`**:

```python
# before
logger.info("connected to %s", url)
# after
ic.info("connected", url)
```

## 📚 API Reference

| API | Description |
|-----|-------------|
| `ic(*args)` | Debug print with source expressions and passthrough return |
| `ic.print(*values, sep=, end=, file=, flush=, markup=, style=, highlight=)` | `print()` replacement with markup |
| `ic.log(*values, level=)` | Logging-style output |
| `ic.debug/info/success/warning/error/critical(*values)` | Level shortcuts |
| `ic.configureOutput(...)` | Configure prefix, context, formatters, output |
| `ic.disable()` / `ic.enable()` | Toggle debug output |
| `ic.format(*args)` | Format without printing |
| `ic.install()` / `ic.uninstall()` | (Un)register the builtins |
| `set_style(style)` / `get_style()` | Theme control |
| `argumentToString.register(Type)` | Custom value formatters |
| `traceback.install(...)` | Pretty tracebacks |

Aliases: `LIT`, `litprint`, `lit` all point at `ic`.

## 🗑️ Removed in 0.4.0

The bundled Rich re-implementation was removed so the package stays small and
focused on printing/debugging:

`Console`, `console`, `cprint`, `Panel`, `Box`, `Text`, `Span`, `Segment`,
`Style`, and the `styles/` theme collection. `ic.print(markup=True)` covers the
colored-output use case; use the real [Rich](https://github.com/Textualize/rich)
if you need full-blown console rendering.

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
