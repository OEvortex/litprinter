LitPrinter
==========

The most sophisticated debug printing library for Python with rich formatting, syntax highlighting, and beautiful tracebacks.

Turn your debugging experience from mundane to magnificent with color themes, context-aware output, smart formatting, and powerful traceback handling.

Installation
-----------

.. code-block:: bash

    pip install litprinter

This will install the required dependencies ``colorama`` and ``executing`` as well.

Basic Usage
----------

.. code-block:: python

    from litprinter import litprint, lit, cprint

    # Basic usage
    litprint("Hello, world!")
    # Output: LIT -> [script.py:3] in () >>> Hello, world!

    # Print to stdout with colors
    from litprinter.core import stdoutPrint
    litprint("Hello", outputFunction=print)            # plain
    litprint("Hello", outputFunction=stdoutPrint)       # colored

    # Print variables with their names
    x, y = 10, 20
    lit(x, y)
    # Output: LIT -> [script.py:7] in () >>> x: 10, y: 20

    # Rich-style printing with simple markup
    cprint("[red]Error:[/red] something went wrong")

Features
--------

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

For more information, see the `full documentation <https://github.com/OEvortex/litprinter>`_.
