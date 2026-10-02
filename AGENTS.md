# Project Guidelines

LitPrinter is a Python debug printing library combining IceCream-style debugging with Rich-style formatting.

## Code Style

- **Line length**: 88 characters
- **Formatting/Linting**: ruff (replaces black, isort, flake8)
- **Type checking**: ty (faster alternative to mypy)

Run formatting:
```bash
uv run ruff format .
uv run ruff check .
uv run ty check .
```

Key patterns:
- Use `functools.singledispatch` for `argumentToString` in `core.py` to register type-specific formatters
- The single theme `theme.py` subclasses `pygments.style.Style`
- Use `_` prefix for private module-level functions (e.g., `_colorize`, `_create_formatter`)

## Architecture

- **`litprint.py`**: `_IceCreamWrapper` — the `ic(x)` callable (debug print,
  print, and logging via `level=`) plus `ic.print()` and `ic.configureOutput()`
- **`core.py`**: `IceCreamDebugger` — argument formatting
  (`argumentToString`), source-expression extraction, context resolution,
  syntax highlighting and the `LOG_LEVELS` / `render_level_prefix()` severity
  tags used by `ic(..., level=)`. There is no per-level API.
- **`markup.py`**: inline `[bold red]...[/]` markup → ANSI, used by `ic.print()`
- **`builtins.py`**: `install()` / `uninstall()` for the builtins registration
- **`render.py`**: turns a debug record into a styled line — dimmed
  prefix/context, coloured names, auto-aligned multi-line values
- **`colors.py`**: the ANSI escape sequences used by markup, render and
  tracebacks
- **`theme.py`**: `LitPrinterStyle`, the one and only Pygments theme
- **`traceback.py`**: pretty tracebacks (`install()` / `uninstall()`), installed
  automatically by `litprinter_autoload.py`
- **`../litprinter_autoload.py`**: executed by the `.pth` at interpreter
  startup; registers `ic` and installs the traceback hook
- **`py.typed`**: PEP 561 marker; `.typeshed/` also declares `ic` as a builtin
  so editors show it like `print()`

Core flow: `ic()` → `_IceCreamWrapper.__call__()` → `IceCreamDebugger._format()` → `_colorized_stderr_print()`

## Removed in 0.4.0

- The level methods (`ic.log`, `ic.debug`, `ic.info`, `ic.success`,
  `ic.warning`, `ic.warn`, `ic.error`, `ic.critical`) and module-level `log()`.
  Do not add them back — `ic(msg, level=...)` is the only logging surface, so
  there is exactly one thing to disable and one thing to type.
- `styles/` (19 themes) and `coloring.py` (5 more), along with `set_style()` /
  `get_style()` and `traceback.install(theme=...)`. One theme remains:
  `LitPrinterStyle` in `theme.py`. Do not add themes back.
- `console.py`, `panel.py`, `box.py`, `text.py`, `segment.py` and `style.py`
  plus their public exports (`Console`, `Panel`, `Box`, `Text`, `Span`,
  `Segment`, `Style`). Do not reintroduce a Rich re-implementation —
  `ic.print()` covers colored output.

## Build and Test

Install for development:
```bash
uv sync --extra dev
```

Run tests:
```bash
uv run pytest
```

`test.py` is a manual smoke script (run `py test.py` to eyeball real terminal
output), not part of the pytest suite.

Package is in `src/litprinter/` (see `package-dir` in pyproject.toml).

## Project Conventions

- **IceCream compatibility**: `ic` must support `configureOutput()`, `enable()`, `disable()`, `format()` - see `litprint.py`
- **Auto-install to builtins**: `ic` is added to Python builtins in `__init__.py` for zero-import usage
- **Return passthrough**: `ic(x)` returns the value(s) passed to it for inline usage: `result = ic(calculate(x))`
- **Singledispatch formatters**: Register custom formatters using `@argumentToString.register(MyType)`
- **Theme**: one theme only (`LitPrinterStyle` in `theme.py`); there is no `set_style()`
- **One entry point**: `ic()` is the only way to output anything. Severity goes
  through `ic(..., level=...)`, which swaps the `ic| ` prefix for the tag and
  sets `context_arrow=False` in the renderer
- **Fields vs. reserved keywords**: `level`, `includeContext` and
  `contextAbsPath` are keyword-only printer settings. Every other keyword
  argument is a named field appended as `name: value`. Fields are printed
  output, not values: `ic(calc(x), step=i)` returns `calc(x)`.

## Integration Points

- **Dependencies**: `pygments`, `colorama`, `executing`, `asttokens`
- **Dev dependencies**: `pytest`, `pytest-cov`, `ruff`, `ty`

## Static analysis notes

`ic` is injected into `builtins` at runtime, which type checkers cannot see.
The repo therefore ships `.typeshed/` (wired up via `[tool.ty.environment]`,
`[tool.pyright]` and `[tool.mypy]`) plus `[tool.ruff] builtins = [...]`, so
`ic` resolves as a real builtin. Add new `ic` methods to
`.typeshed/stdlib/builtins.pyi` when you add them.
