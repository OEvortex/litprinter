# LitPrinter Documentation

LitPrinter is the debug printer that replaces `print()`, `logging` and
`icecream` — smart debugging, a drop-in `print()`, logging helpers and
syntax-highlighted tracebacks in one small package.

## Installation

```bash
pip install litprinter
```

## Quick Start

```python
# No import needed after pip install!
x = 42
ic(x)                      # ic| x: 42
ic.print("value:", x)      # value: 42
ic.info("service ready")   # INFO  service ready
```

`ic` is registered in `builtins` automatically, so it works in every script.

## Feature comparison

| Feature | `print()` | IceCream | logging | LitPrinter |
|---------|-----------|----------|---------|------------|
| Shows variable names | ❌ | ✅ | ❌ | ✅ |
| Replaces `print()` | ❌ | ❌ | ❌ | ✅ |
| Colored markup | ❌ | ❌ | ❌ | ✅ |
| Context only when useful | ❌ | ❌ | ✅ | ✅ |
| Pretty tracebacks | ❌ | ❌ | ❌ | ✅ |
| Zero-import | — | ❌ | — | ✅ |

## Debugging

```python
def calculate(a, b):
    total = a + b
    ic(total)               # ic| total: 30
    ic(total * 2)           # ic| [app.py:3 in calculate()] >>> total * 2: 60
    ic()                    # ic| app.py:3 in calculate() - 14:02:11.004
    return total
```

Context rules (`contextMode='auto'` by default):

| Call | Context | Reason |
|------|---------|--------|
| `ic(x)` | no | variable name already shown |
| `ic(x + 1)` | yes | expression needs a location |
| `ic(data["k"])` | yes | subscript needs a location |
| `ic(f"{x}")` | no | value is self-describing |
| `ic()` | yes | breadcrumb: where and when |

```python
ic(x, includeContext=True)   # per-call force on
ic(x, includeContext=False)  # per-call force off

ic.configureOutput(contextMode="always")   # 'auto' | 'always' | 'never'
ic.configureOutput(contextAbsPath=True)    # absolute paths
```

## `ic.print` — drop-in `print()`

Identical signature to builtin `print()`, plus markup and highlighting:

```python
ic.print("plain output")
ic.print("a", "b", sep=" | ", end="!\n")
ic.print("stderr line", file=sys.stderr, flush=True)

ic.print("[bold red]ERROR[/bold red] connection refused")
ic.print("[on_blue] INFO [/on_blue] listening on :8080")
ic.print("styled", style="bold cyan")
ic.print({"port": 8080}, highlight=True)
ic.print("[literal]", markup=False)   # opt out of markup
```

Markup tags: `bold`, `dim`, `italic`, `underline`, `strike`, `reverse`,
`blink`, colors (`red`, `bright_red`, …), backgrounds (`on_blue`, …),
`#hex` and `rgb(r,g,b)` values, closed with `[/]`.

`from litprinter import print` gives you the same function.

## Logging

```python
ic.debug("cache miss", key)
ic.info("connected", url)
ic.success("migration done")
ic.warning("retrying", attempt=2)
ic.error("request failed", status=500)
ic.critical("disk full")

ic.log("generic", level="info")
ic.log("timestamped", level="warn", timestamp=True)
```

Levels: `debug`, `info`, `success`, `warning`/`warn`, `error`, `critical`.
Level output goes to stderr so piped stdout stays clean.

## Configuration

```python
ic.configureOutput(
    prefix="dbg| ",
    contextMode="auto",
    contextAbsPath=False,
    pairDelimiter=", ",
    outputFunction=my_logger.debug,
    argToStringFunction=my_formatter,
)

ic.disable()      # silent, values still returned
ic.enable()
s = ic.format(x)  # format without printing
```

## Custom formatters

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

## Pretty tracebacks

```python
from litprinter import traceback

traceback.install(
    theme="cyberpunk",
    show_locals=True,
    extra_lines=3,
)
```

Themes available for tracebacks: `JARVIS`, `RICH`, `MODERN`, `NEON`,
`CYBERPUNK`, `DRACULA`, `MONOKAI`, `SOLARIZED`, `NORD`, `GITHUB`, `VSCODE`,
`MATERIAL`, `RETRO`, `OCEAN`, `AUTUMN`, `SYNTHWAVE`, `FOREST`, `MONOCHROME`,
`SUNSET`.

## Builtins control

```python
from litprinter import install, uninstall

install()     # re-register ic
uninstall()   # remove ic from builtins
```

## API reference

| API | Description |
|-----|-------------|
| `ic(*args, includeContext=None, contextAbsPath=None)` | Debug print, returns the values |
| `ic.print(*values, sep, end, file, flush, markup, style, color, highlight)` | `print()` replacement |
| `ic.log(*values, level, sep, file, flush, timestamp, markup)` | Logging output |
| `ic.debug/info/success/warning/warn/error/critical` | Level shortcuts |
| `ic.configureOutput(prefix, outputFunction, argToStringFunction, includeContext, contextAbsPath, contextMode, pairDelimiter)` | Configure output |
| `ic.enable()` / `ic.disable()` | Toggle debug output |
| `ic.format(*args)` | Format without printing |
| `ic.install()` / `ic.uninstall()` | (Un)register builtins |
| `set_style(style)` / `get_style()` | Theme control |
| `argumentToString.register(Type)` | Custom formatters |
| `render_markup(text, style=, color=)` | Render markup to ANSI |
| `traceback.install(...)` / `traceback.uninstall()` | Pretty tracebacks |

Aliases: `LIT`, `litprint`, `lit`.

## Removed in 0.4.0

The bundled Rich re-implementation was deleted to keep the package focused:
`Console`, `console`, `cprint`, `Panel`, `Box`, `Text`, `Span`, `Segment`,
`Style` and the `styles/` theme collection. Use `ic.print()` for colored
markup, or [Rich](https://github.com/Textualize/rich) for full console
rendering.

## Migration

```python
# print -> ic
print(f"user: {user['name']}")   # before
ic(user["name"])                  # after

# logging -> ic
logger.info("connected to %s", url)  # before
ic.info("connected", url)            # after

# icecream -> litprinter
from icecream import ic   # before
# after: no import needed at all
```

## Version

Current version: **0.4.0**

For more examples, see the [GitHub repository](https://github.com/OEvortex/litprinter).
