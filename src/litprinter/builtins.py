#!/usr/bin/env python3
"""
LitPrinter Builtins

Install and remove litprinter's globals from Python's builtins.

Importing :mod:`litprinter` already registers ``ic`` (and the ``LIT`` /
``litprint`` / ``lit`` aliases), so these helpers are only needed after an
explicit :func:`uninstall`, or to register the printer under a second name.

Usage::

    from litprinter import install, uninstall

    uninstall()          # remove ic, LIT, litprint and lit
    ic(1)                # NameError
    install()            # put them back
    install('dbg')       # or register under a different name
"""

import builtins

#: The globals litprinter registers on import.
DEFAULT_NAMES = ('ic', 'LIT', 'litprint', 'lit')


def install(name: str = 'ic') -> None:
    """Register the litprinter globals in builtins.

    Args:
        name: Register the printer under this name. Defaults to ``'ic'``.

    Note:
        Importing litprinter already registers ``ic``, ``LIT``, ``litprint``
        and ``lit``, so calling this is only needed after :func:`uninstall`,
        or to expose the printer under an extra name such as ``install('dbg')``.
    """
    import litprinter

    setattr(builtins, name, litprinter.ic)


def uninstall(name: str = 'ic') -> None:
    """Remove a litprinter global from builtins.

    Args:
        name: The builtin to remove. Defaults to ``'ic'``. Pass ``'*'`` to
            remove every name in :data:`DEFAULT_NAMES`.
    """
    if name == '*':
        for key in DEFAULT_NAMES:
            delattr(builtins, key) if hasattr(builtins, key) else None
        return
    if hasattr(builtins, name):
        delattr(builtins, name)


__all__ = ['install', 'uninstall', 'DEFAULT_NAMES']
