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
- Pygments styles inherit from `pygments.style.Style` in `styles/base.py`
- Use `_` prefix for private module-level functions (e.g., `_colorize`, `_create_formatter`)

## Architecture

- **`litprint.py`**: `_IceCreamWrapper` — the `ic(x)` callable plus
  `ic.print()`, `ic.log()`, level shortcuts and `ic.configureOutput()`
- **`core.py`**: `IceCreamDebugger` — argument formatting
  (`argumentToString`), source-expression extraction, context resolution and
  syntax highlighting
- **`markup.py`**: inline `[bold red]...[/]` markup → ANSI, used by `ic.print()`
- **`builtins.py`**: `install()` / `uninstall()` for the builtins registration
- **`colors.py`**: the ANSI escape sequences used by markup and tracebacks
- **`coloring.py`**: Pygments styles for `ic()` output (`set_style()`)
- **`styles/`**: the 19 Pygments themes used by `traceback.install(theme=...)`
- **`traceback.py`**: pretty tracebacks (`install()` / `uninstall()`)
- **`py.typed`**: PEP 561 marker; `.typeshed/` also declares `ic` as a builtin
  so editors show it like `print()`

Core flow: `ic()` → `_IceCreamWrapper.__call__()` → `IceCreamDebugger._format()` → `_colorized_stderr_print()`

## Removed in 0.4.0

`console.py`, `panel.py`, `box.py`, `text.py`, `segment.py` and `style.py` were
deleted along with their public exports (`Console`, `Panel`, `Box`, `Text`,
`Span`, `Segment`, `Style`). Do not reintroduce a Rich re-implementation —
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
- **Themes**: Pygments styles in `styles/*.py` inherit from `pygments.style.Style`

## Integration Points

- **Dependencies**: `pygments`, `colorama`, `executing`, `asttokens`
- **Dev dependencies**: `pytest`, `pytest-cov`, `ruff`, `ty`

## Static analysis notes

`ic` is injected into `builtins` at runtime, which type checkers cannot see.
The repo therefore ships `.typeshed/` (wired up via `[tool.ty.environment]`,
`[tool.pyright]` and `[tool.mypy]`) plus `[tool.ruff] builtins = [...]`, so
`ic` resolves as a real builtin. Add new `ic` methods to
`.typeshed/stdlib/builtins.pyi` when you add them.
