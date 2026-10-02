"""Startup hook for LitPrinter.

A ``litprinter_autoload.pth`` file is installed next to this module, so
CPython's ``site`` executes ``import litprinter_autoload`` for **every**
interpreter start. That is what makes ``ic()`` available everywhere with no
import, and what installs the pretty traceback handler.

Everything here is best-effort and must never break a Python process: any
failure is swallowed.

Environment variables
---------------------
``LITPRINTER_NO_AUTOLOAD=1``
    Skip everything. ``ic()`` is not added to builtins and the default
    traceback handler is left alone.
``LITPRINTER_NO_TRACEBACK=1``
    Still register ``ic()``, but leave ``sys.excepthook`` untouched.
"""

import os


def _disabled(name: str) -> bool:
    """True when the named environment variable opts out.

    Any non-empty value counts, so ``LITPRINTER_NO_TRACEBACK=1`` and
    ``LITPRINTER_NO_TRACEBACK=please`` both work.
    """
    return bool(os.environ.get(name, '').strip())


if not _disabled('LITPRINTER_NO_AUTOLOAD'):
    try:
        import litprinter  # noqa: F401  (registers ic in builtins)
    except Exception:
        # A broken install must never stop Python from starting.
        pass
    else:
        if not _disabled('LITPRINTER_NO_TRACEBACK'):
            try:
                litprinter.traceback.install(show_locals=True)
            except Exception:
                pass
