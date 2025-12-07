#!/usr/bin/env python3
"""
LitPrinter Builtins Module

Provides functions to install litprinter functions into Python builtins,
making them available globally without imports.

Usage:
    from litprinter.builtins import install, uninstall
    
    install()  # Now ic() and litprint() work globally
    
    ic(x)  # Works without import!
    
    uninstall()  # Remove from builtins

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

try:
    import builtins as _builtins
except ImportError:
    import __builtin__ as _builtins  # Python 2 compatibility

from .litprint import ic, LIT, litprint, configureOutput, enable, disable


def install(
    ic_name: str = 'ic',
    lit_name: str = 'LIT',
    litprint_name: str = 'litprint',
    install_helpers: bool = True,
) -> None:
    """Install litprinter functions into Python builtins.
    
    After calling this function, ic(), LIT(), and litprint() will be
    available globally without needing to import them.
    
    Args:
        ic_name: Name for the ic function in builtins (default: 'ic').
                 Set to None or '' to skip.
        lit_name: Name for the LIT function in builtins (default: 'LIT').
                  Set to None or '' to skip.
        litprint_name: Name for litprint function (default: 'litprint').
                       Set to None or '' to skip.
        install_helpers: Whether to also install enable/disable/configureOutput.
    
    Example:
        >>> from litprinter.builtins import install
        >>> install()
        >>> ic(42)  # Works globally now!
        ic| 42
    """
    # Install main functions
    if ic_name:
        setattr(_builtins, ic_name, ic)
    
    if lit_name:
        setattr(_builtins, lit_name, LIT)
    
    if litprint_name:
        setattr(_builtins, litprint_name, litprint)
    
    # Install helper functions
    if install_helpers:
        setattr(_builtins, 'ic_configure', configureOutput)
        setattr(_builtins, 'ic_enable', enable)
        setattr(_builtins, 'ic_disable', disable)


def uninstall(
    ic_name: str = 'ic',
    lit_name: str = 'LIT', 
    litprint_name: str = 'litprint',
    uninstall_helpers: bool = True,
) -> None:
    """Remove litprinter functions from Python builtins.
    
    Args:
        ic_name: Name of ic function to remove.
        lit_name: Name of LIT function to remove.
        litprint_name: Name of litprint function to remove.
        uninstall_helpers: Whether to also remove helper functions.
    
    Example:
        >>> from litprinter.builtins import uninstall
        >>> uninstall()
        >>> ic(42)  # NameError: name 'ic' is not defined
    """
    # Remove main functions
    for name in [ic_name, lit_name, litprint_name]:
        if name and hasattr(_builtins, name):
            delattr(_builtins, name)
    
    # Remove helper functions
    if uninstall_helpers:
        for name in ['ic_configure', 'ic_enable', 'ic_disable']:
            if hasattr(_builtins, name):
                delattr(_builtins, name)


# ============================================================================
# Exports
# ============================================================================

__all__ = ['install', 'uninstall']
