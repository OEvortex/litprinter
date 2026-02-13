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

- **`core.py`**: `IceCreamDebugger` class - main debugging logic with frame inspection
- **`litprint.py`**: `_IceCreamWrapper` class - provides `ic(x)` callable with method access (`ic.configureOutput()`)
- **`__init__.py`**: Public API exports, auto-installs `ic` to builtins
- **`coloring.py`**: Pygments style definitions (TokyoNight, LitStyle, SolarizedDark, etc.)
- **`styles/`**: Additional theme modules (cyberpunk.py, dracula.py, nord.py, etc.)
- **`console.py`**: Rich-like Console class for styled output
- **`panel.py`**: Panel rendering with borders and padding
- **`traceback.py`**: Pretty traceback formatting

Core flow: `ic()` → `_IceCreamWrapper.__call__()` → `IceCreamDebugger._format()` → `_colorized_stderr_print()`

## Build and Test

Install for development:
```bash
uv sync --group dev
```

Run tests:
```bash
uv run pytest
```

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
