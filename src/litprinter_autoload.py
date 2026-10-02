"""Autoload helper for LitPrinter's .pth file.

The companion ``litprinter_autoload.pth`` is processed by ``site.py`` and
executes ``import litprinter_autoload``.  This module intentionally swallows
import failures so a broken environment never breaks every Python startup.
"""

from __future__ import annotations

import os

_DISABLE_ENV = "LITPRINTER_NO_AUTOLOAD"

if os.environ.get(_DISABLE_ENV, "").lower() not in {"1", "true", "yes", "on"}:
    try:
        import litprinter  # noqa: F401
    except Exception:
        # Never let autoload break Python startup.  Explicit imports of
        # litprinter will still surface the original exception.
        pass
