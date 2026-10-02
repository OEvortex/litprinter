# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-10-02

LitPrinter is now one focused tool for terminal output: a debug printer, a
`print()` replacement, a logger and pretty tracebacks, all in one consistent
look with a single built-in theme. This release squashes the earlier
0.3.4/0.3.5/0.4.x/0.5.x/0.6.x work into one release.

### Added

**Printing**
- `ic.print(*values, sep=, end=, file=, flush=, markup=, style=, color=, highlight=)`
  — drop-in `print()` replacement with inline markup
- `litprinter.markup` with `render_markup`, `strip_markup`, `supports_color`
- Markup tags: `bold`, `dim`, `italic`, `underline`, `strike`, `reverse`,
  `blink`, 16 colors (`[red]`, `[bright_red]`, …), backgrounds (`[on_blue]`, …),
  `#hex` and `rgb(r,g,b)` values, closed with `[/]`
- `litprinter.print` alias, so `from litprinter import print` works

**Logging through ic()**
- `ic(*values, level=...)` tags a line with a severity: `debug`, `info`,
  `success`/`ok`, `warning`/`warn`, `error`, `critical`. An unknown level raises
  `ValueError` listing the valid names and leaves debugger state untouched.
- Named fields: keyword arguments other than `level`, `includeContext` and
  `contextAbsPath` print as `name: value` pairs, so logging reads the way it is
  normally written — `ic("retrying", attempt=2, level="warning")`. Fields
  honour `argumentToString` and `pairDelimiter`, and never affect the return
  value, so `result = ic(calculate(x), step=i)` still returns `calculate(x)`.
- `ic.format(*values, level=..., **fields)` returns the same line as a string
  without printing it.
- Output goes to stderr so piped stdout stays clean; `ic.disable()` silences
  leveled lines too.

**Debugging**
- `contextMode` (`'auto' | 'always' | 'never'`) plus per-call
  `includeContext=True/False`
- Automatic context detection: `file:line` is only shown when the expression
  is not self-explanatory. Bare names, literals and f-strings stay clean;
  calls, subscripts, attributes and operators get context.
- `ic.install()` / `ic.uninstall()`, plus `litprinter.install` / `uninstall`
  (which now round-trip all four registered names)
- `pairDelimiter` option in `configureOutput()`

**Rendering** (new `render.py`)
- The prefix and file/line context are dimmed, variable names get their own
  colour, and values are syntax highlighted automatically
- Multi-line values hang off the first line instead of restarting at column 0,
  and the indent accounts for the prefix *and* the context column
- A leveled line replaces the `ic| ` prefix with the severity tag and drops the
  `>>> ` context arrow, so it reads as a log record

**Tracebacks**
- Installed automatically for every Python process by the `.pth` autoloader, so
  readable tracebacks work with no setup. Opt out with
  `LITPRINTER_NO_TRACEBACK=1`, or disable litprinter entirely with
  `LITPRINTER_NO_AUTOLOAD=1`. Both are best-effort and can never break
  interpreter startup.
- Rich-style `── Traceback (most recent call last) ──` header with a timestamp,
  a thinner separator rule, and library frames dimmed and tagged `[library]` so
  your own frames stand out
- `install()` now honours `suppress=`, `max_frames=`, `locals_hide_sunder=`;
  `max_frames` reports how many frames it dropped, and `max_frames=0` truncates

**Packaging and tooling**
- Linux autoload: the `.pth` is a valid `import` line and is installed into
  site-packages (not the wheel's `.data/data` directory); editable installs get
  the same behaviour
- Fixed missing `README.md` metadata on case-sensitive filesystems
- Vendored `.typeshed/` so `ic`, `LIT`, `litprint` and `lit` are typed as real
  builtins for ty, pyright/Pylance and mypy (hover docs, completions, no
  "name not defined" errors)
- `py.typed` so type checkers use the inline annotations
- Test suite: 95 tests across `ic()`, `ic.print()`, levels and fields, markup,
  builtins and tracebacks

### Changed

- Module-level `ic()` calls no longer print an `in <module>` suffix; the
  context is just `file:line` (e.g. `ic| [test.py:15] >>> add(5, 3): 8`).
  Inside functions the `in name()` suffix is still added.
- One theme: the new `theme.py` provides `LitPrinterStyle`, a quiet palette
  tuned for long debugging sessions, shared by `ic()`, `ic.print(highlight=True)`
  and tracebacks. Roughly 2400 lines of bundled themes were deleted.
- `ic()` and `ic.print()` now share one colour-detection path, so `NO_COLOR`,
  `FORCE_COLOR` and `TERM=dumb` behave identically for both.
- Pygments, colorama, executing and asttokens are now plain imports rather than
  optional-import guards — they are all declared dependencies
- `litprinter.colors` trimmed to the ANSI helpers actually used
- README and docs rewritten around `ic()`, `ic.print()`, logging and the
  auto-installed traceback

### Fixed

- `colorama.init()` was being called on every platform. It wraps
  `sys.stdout`/`sys.stderr` and strips ANSI codes whenever the stream is not a
  TTY, so all highlighting was silently lost when output was piped to a file or
  captured. It is now only used on Windows.
- `traceback.install()` documented that it returns the previous hook but
  returned a different function depending on the branch taken.
- Markup parsing: `on_gray`/`on_grey`/`bright_gray`/`bright_grey` raised
  `KeyError`; an unmatched `[/]` was dropped; `[]` was treated as markup;
  `install()`/`uninstall()` did not round-trip all four registered names; and
  a bad `theme=` recorded an invalid value instead of falling back.

### Removed

- The level method family — `ic.log()`, `ic.debug()`, `ic.info()`,
  `ic.success()`, `ic.warning()` / `ic.warn()`, `ic.error()`, `ic.critical()`
  and module-level `litprinter.log()`. Use `ic(msg, level="error")`. One
  entry point means one thing to type and one thing to turn off.
- The 19 bundled themes (`litprinter.styles`), the 5 styles in `coloring.py`,
  `set_style()` / `get_style()` and `traceback.install(theme=...)`. There is now
  exactly one theme.
- Bundled Rich re-implementation: `Console`, `console`, `cprint`, `Panel`,
  `Box`, `Text`, `Span`, `Segment`, `Style`, plus the dead
  `clearStyleCache`, `getStyleCacheInfo`, `isTerminalCapable` and
  `DEFAULT_LINE_WRAP_WIDTH` helpers. Use `ic.print()` for colored output, or
  the real Rich package for panels and full console rendering.
- Rich console protocol hooks on `PrettyTraceback` (`__rich_console__`,
  `__rich_measure__`)
- Dead `word_wrap` and `locals_max_length` traceback options, which were
  accepted but never applied

## [0.3.3] - 2025-12-08

### Fixed

- ModuleNotFoundError in `litprinter_autoload.pth` by wrapping import in try-except
- Fixed type checkings in codebase

## [0.3.0] - 2025-12-07



### 🚀 Major Release: IceCream + Rich Fusion



This release transforms LitPrinter into a true fusion of IceCream debugging and Rich-style formatting.



### Added



#### IceCream-Compatible API

- Full `ic()` function with IceCream-compatible behavior

- `ic.configureOutput()` for runtime configuration

- `ic.disable()` and `ic.enable()` for toggling output

- `ic.format()` for formatting without printing

- Per-call context override with `includeContext` parameter

- Aliases: `LIT`, `litprint`, `lit` all point to `ic`



#### Color Themes

- **SolarizedDark**: IceCream-compatible theme (now default)

- **LitStyle**: Vibrant modern theme with brighter colors

- **CyberpunkStyle**: Neon pink, teal, and green

- **MonokaiStyle**: Classic code editor theme

- `set_style()` function to switch themes at runtime

- `get_style()` function to get current theme



#### Rich-Style Features

- `Segment` class for styled text representation

- `Style` class for style composition and parsing

- `Text` class with styled spans and markup support

- `Box` class with 12+ predefined border styles

- `Console` class with `print()`, `log()`, `rule()`, `status()` methods

- `Panel` class with `fit()` classmethod and Rich protocols



#### Traceback Enhancements

- Frame suppression with `suppress` parameter

- `max_frames` to limit displayed frames

- `from_exception()` classmethod

- `__rich_console__` and `__rich_measure__` protocols

- `Traceback` alias for `PrettyTraceback`



#### Infrastructure

- Dynamic versioning from `__init__.py`

- Added `asttokens` dependency for better source extraction

- Updated Python version support (3.8-3.13)



### Changed

- Complete rewrite of `core.py` with clean `IceCreamDebugger` class

- Simplified `litprint.py` with `_IceCreamWrapper`

- Fixed duplicate code in `builtins.py`

- Default style changed to SolarizedDark for IceCream compatibility



### Removed

- Deleted unused `_core_functions.py`

- Removed legacy code patterns



## [0.2.1] - 2025-04-10



### Fixed

- Module import issues

- Panel rendering edge cases



## [0.2.0] - 2025-04-05



### Added

- Initial public release

- Variable inspection with expression display

- Return value handling for inline usage

- Support for custom formatters for specific data types

- Execution context tracking

- Rich-like colorized output with multiple themes (JARVIS, RICH, MODERN, NEON, CYBERPUNK)

- Better JSON formatting with indent=2 by default

- Advanced pretty printing for complex data structures with smart truncation

- Clickable file paths in supported terminals and editors (VSCode compatible)

- Enhanced visual formatting with better spacing and separators

- Special formatters for common types (Exception, bytes, set, frozenset, etc.)

- Smart object introspection for custom classes

- Logging capabilities with timestamp and log levels
