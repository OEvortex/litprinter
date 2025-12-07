#!/usr/bin/env python3
"""
LitPrinter Builtins Module

Provides functions to install litprinter functions into Python builtins,
making them available globally without imports.

Usage:
    from litprinter import install, uninstall
    
    install()  # Now ic() works globally without import!
    
    # In any file, without import:
    ic(x)
    
    uninstall()  # Remove from builtins

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

from typing import Optional

_builtins = __import__('builtins')


def install(ic: str = 'ic') -> None:
    """Install ic to Python builtins for global access.
    
    After calling this function, ic() will be available globally
    without needing to import it.
    
    Args:
        ic: Name for the ic function in builtins (default: 'ic').
    
    Example:
        >>> from litprinter import install
        >>> install()
        >>> # Now in any file, without import:
        >>> ic(x)  # Works!
    """
    import litprinter
    setattr(_builtins, ic, litprinter.ic)


def uninstall(ic: str = 'ic') -> None:
    """Remove ic from Python builtins.
    
    Args:
        ic: Name of the function to remove (default: 'ic').
    
    Example:
        >>> from litprinter import uninstall
        >>> uninstall()
        >>> ic(x)  # NameError: name 'ic' is not defined
    """
    if hasattr(_builtins, ic):
        delattr(_builtins, ic)


# ============================================================================
# Exports
# ============================================================================

__all__ = ['install', 'uninstall']
