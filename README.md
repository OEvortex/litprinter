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
ic("server started", level="info")  # INFO  server started
```

That's it. After `pip install litprinter`, `ic` is available in **every** Python
script — no import required — and so are the pretty tracebacks.

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

### 🎨 Rich-like rendering

Values are syntax highlighted automatically and multi-line values hang off
the first line instead of restarting at column 0:

```python
config = {"host": "0.0.0.0", "port": 8080, "tags": ["a", "b"]}
ic(config)
```

```
ic| config: {
        'host': '0.0.0.0',
        'port': 8080,
        'tags': ['a', 'b']
      }
```

Colors follow the terminal: on for a TTY, off when piped to a file. Force them
with `FORCE_COLOR=1`, suppress with `NO_COLOR=1`.

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

`ic()` *is* the logger. Add `level=` and the line is tagged with a severity;
keyword arguments become named fields:

```python
ic("cache miss", key="session:9f2", level="debug")
ic("connected", url=url, level="info")
ic("migration complete", level="success")
ic("retrying in 5s", attempt=2, level="warning")
ic("request failed", status=500, level="error")
ic("disk full", level="critical")
```

```
DEBUG  'cache miss', key: 'session:9f2'
INFO   'connected', url: 'https://api.internal'
OK     'migration complete'
WARN   'retrying in 5s', attempt: 2
ERROR  'request failed', status: 500
CRIT   'disk full'
```

Levels: `debug`, `info`, `success` (`ok`), `warning` (`warn`), `error`,
`critical`. An unknown level raises `ValueError`.

Two differences from `ic(x)`:

- the `ic| ` prefix is replaced by the severity tag
- the `>>> ` context arrow is dropped — a leveled line reads as a log record

Everything else is identical: file/line context still appears when the
expression isn't self-describing, multi-line values still hang off the first
line, and `ic.disable()` silences levels too. Output goes to stderr so it stays
out of your piped stdout.

### Fields work without a level

Keyword arguments are just named values, so this is fine too:

```python
ic("cache miss", key="session:9f2")
# ic| 'cache miss', key: 'session:9f2'
```

Three keyword names belong to the printer and are never treated as fields:
`level`, `includeContext` and `contextAbsPath`. Positional values are
unaffected.

`ic.format(msg, level="error")` returns the same line as a string without
printing it.

## 🧵 Inline usage

```python
result = ic(calculate(x))  # prints AND returns the value
```

## 🎨 One theme

LitPrinter ships a single, hand-tuned theme (`LitPrinterStyle`). It is applied
automatically to `ic()` values, `ic.print(..., highlight=True)` and tracebacks —
there is nothing to choose and nothing to configure.

The palette is deliberately quiet so long debugging sessions stay readable:
muted blue-gray for punctuation, calm cyan for names, warm green for strings,
soft orange for numbers, and strong red reserved for actual errors.

```python
from litprinter import LitPrinterStyle   # the only style, exposed for reference
```

## 💥 Beautiful tracebacks — installed automatically

Installing litprinter also installs the traceback handler, so **every** Python
process gets readable tracebacks with no setup:

```
── Traceback (most recent call last) ────────── 2026-10-02 11:00:00 ──────────

ZeroDivisionError: division by zero

  File "app.py", line 12, in divide
     10 │     payload = {"a": a, "b": b}
  ❱   12 │     return a / b

  Variables:
  a = 10    payload = {'a': 10, 'b': 0}  [dict]
  b = 0
```

Tune it at runtime:

```python
from litprinter import traceback

traceback.install(
    show_locals=True,
    extra_lines=3,
    suppress=["site-packages"],  # hide library frames
    max_frames=20,               # cap the stack
    locals_hide_sunder=True,     # hide _private locals
)

traceback.uninstall()  # back to the default handler
```

Opt out before Python starts:

```bash
LITPRINTER_NO_TRACEBACK=1 py app.py   # normal traceback, ic() still available
LITPRINTER_NO_AUTOLOAD=1 py app.py    # litprinter fully inert
```

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
ic("connected", url, level="info")
```

## 📚 API Reference

| API | Description |
|-----|-------------|
| `ic(*args, level=)` | Debug print, passthrough return, and the logger |
| `ic.print(*values, sep=, end=, file=, flush=, markup=, style=, highlight=)` | `print()` replacement with markup |
| `ic.configureOutput(...)` | Configure prefix, context, formatters, output |
| `ic.disable()` / `ic.enable()` | Toggle output (including leveled lines) |
| `ic.format(*args, level=)` | Format without printing |
| `ic.install()` / `ic.uninstall()` | (Un)register the builtins |
| `LitPrinterStyle` | The single built-in theme (a `pygments.style.Style`) |
| `argumentToString.register(Type)` | Custom value formatters |
| `traceback.install(...)` | Pretty tracebacks |

Aliases: `LIT`, `litprint`, `lit` all point at `ic`.

## 🗑️ Removed

- **0.6.0**: the level method family — `ic.log()`, `ic.debug()`, `ic.info()`,
  `ic.success()`, `ic.warning()` / `ic.warn()`, `ic.error()`, `ic.critical()`
  and the module-level `litprinter.log()`. Use `ic(msg, level="error")`.
  One entry point, one way to turn it off.
- **0.5.0**: the 19 bundled themes, `litprinter.styles`, `coloring.py`,
  `set_style()` / `get_style()` and `traceback.install(theme=...)`. There is a
  single built-in theme.
- **0.4.0**: the bundled Rich re-implementation — `Console`, `console`,
  `cprint`, `Panel`, `Box`, `Text`, `Span`, `Segment` and `Style`.
  `ic.print(markup=True)` covers the colored-output use case; use the real
  [Rich](https://github.com/Textualize/rich) for full console rendering.

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
