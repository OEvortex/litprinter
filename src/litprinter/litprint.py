#!/usr/bin/env python3
"""
LitPrinter - IceCream-compatible Debug Printing

This module provides ic-style debug printing with Rich formatting.
It's a drop-in replacement for IceCream with additional features.

Usage:
    from litprinter import ic
    
    x = 42
    ic(x)  # Output: ic| x: 42
    
    # Configure output
    ic.configureOutput(prefix='DEBUG| ')
    
    # Enable/disable
    ic.disable()
    ic.enable()
    
    # Format without printing
    s = ic.format(x)

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

import inspect
from typing import Any, Callable, Optional, Union

from .core import IceCreamDebugger, argumentToString, _colorized_stderr_print, set_style, get_style


# ============================================================================
# Module-level IC Instance
# ============================================================================

class _IceCreamWrapper:
    """Wrapper class that provides both callable and method access.
    
    This allows:
        ic(x)  # Call like a function
        ic.configureOutput(...)  # Access methods
        ic.disable() / ic.enable()  # Toggle
    """
    
    def __init__(self):
        self._debugger = IceCreamDebugger()
    
    def __call__(self, *args, includeContext: Optional[bool] = None, 
                 contextAbsPath: Optional[bool] = None) -> Any:
        """Debug print arguments and return them.
        
        Args:
            *args: Values to debug print.
            includeContext: Override context setting for this call.
            contextAbsPath: Override path setting for this call.
            
        Returns:
            None if no args, single arg if one arg, tuple if multiple.
        """
        # Save original settings for per-call overrides
        orig_context = self._debugger._includeContext
        orig_abs_path = self._debugger._contextAbsPath
        
        try:
            # Apply per-call overrides
            if includeContext is not None:
                self._debugger._includeContext = includeContext
            if contextAbsPath is not None:
                self._debugger._contextAbsPath = contextAbsPath
            
            if not self._debugger.enabled:
                # Return passthrough even when disabled
                if not args:
                    return None
                elif len(args) == 1:
                    return args[0]
                else:
                    return args
            
            # Get the caller's frame
            call_frame = inspect.currentframe().f_back
            
            # Format and output
            output = self._debugger._format(call_frame, *args)
            self._debugger._outputFunction(output)
            
            # Return passthrough
            if not args:
                return None
            elif len(args) == 1:
                return args[0]
            else:
                return args
                
        finally:
            # Restore original settings
            self._debugger._includeContext = orig_context
            self._debugger._contextAbsPath = orig_abs_path
    
    def format(self, *args) -> str:
        """Format arguments without printing.
        
        Args:
            *args: Values to format.
            
        Returns:
            Formatted string.
        """
        call_frame = inspect.currentframe().f_back
        return self._debugger._format(call_frame, *args)
    
    def configureOutput(
        self,
        prefix: Union[str, Callable[[], str], None] = None,
        outputFunction: Optional[Callable[[str], None]] = None,
        argToStringFunction: Optional[Callable[[Any], str]] = None,
        includeContext: Optional[bool] = None,
        contextAbsPath: Optional[bool] = None,
    ) -> None:
        """Configure output settings.
        
        Args:
            prefix: Prefix string or callable returning prefix.
            outputFunction: Function to call with formatted output.
            argToStringFunction: Function to convert args to strings.
            includeContext: Whether to show file/line/function.
            contextAbsPath: Whether to use absolute paths.
        """
        self._debugger.configureOutput(
            prefix=prefix,
            outputFunction=outputFunction,
            argToStringFunction=argToStringFunction,
            includeContext=includeContext,
            contextAbsPath=contextAbsPath,
        )
    
    def enable(self) -> None:
        """Enable debug output."""
        self._debugger.enable()
    
    def disable(self) -> None:
        """Disable debug output."""
        self._debugger.disable()
    
    @property
    def enabled(self) -> bool:
        """Check if debugging is enabled."""
        return self._debugger.enabled
    
    def __repr__(self) -> str:
        return f"<ic enabled={self.enabled}>"


# ============================================================================
# Module-level Instances and Aliases
# ============================================================================

# The main ic instance
ic = _IceCreamWrapper()

# Aliases for compatibility
LIT = ic
litprint = ic
lit = ic

# Module-level convenience functions
def configureOutput(
    prefix: Union[str, Callable[[], str], None] = None,
    outputFunction: Optional[Callable[[str], None]] = None,
    argToStringFunction: Optional[Callable[[Any], str]] = None,
    includeContext: Optional[bool] = None,
    contextAbsPath: Optional[bool] = None,
) -> None:
    """Configure the global ic output settings.
    
    Args:
        prefix: Prefix string or callable.
        outputFunction: Output function.
        argToStringFunction: Argument formatting function.
        includeContext: Whether to include context.
        contextAbsPath: Whether to use absolute paths.
    """
    ic.configureOutput(
        prefix=prefix,
        outputFunction=outputFunction,
        argToStringFunction=argToStringFunction,
        includeContext=includeContext,
        contextAbsPath=contextAbsPath,
    )


def enable() -> None:
    """Enable debug output globally."""
    ic.enable()


def disable() -> None:
    """Disable debug output globally."""
    ic.disable()


def format(*args) -> str:
    """Format arguments without printing.
    
    Args:
        *args: Values to format.
        
    Returns:
        Formatted string.
    """
    call_frame = inspect.currentframe().f_back
    return ic._debugger._format(call_frame, *args)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Main instance
    'ic',
    # Aliases
    'LIT',
    'litprint', 
    'lit',
    # Functions
    'configureOutput',
    'enable',
    'disable',
    'format',
    # Core exports
    'argumentToString',
    'IceCreamDebugger',
]
