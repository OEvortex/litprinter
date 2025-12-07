# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
