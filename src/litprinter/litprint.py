"""
>>> from litprinter import litprint
>>>
>>> litprint("Hello, world!")
ic| "Hello, world!"
>>>
>>> def my_function(a, b):
...    litprint(a, b)
>>> my_function(1, 2)
ic| a: 1, b: 2

This module provides the 'litprint' function, which is an enhanced print function for
debugging purposes. It leverages the LITPrintDebugger class from 'core.py' and allows
for configurable prefix, output functions, and context inclusion. It's designed
to make debugging more straightforward by offering clear output with context information.
"""
from typing import Any, Callable
from .core import LITPrintDebugger

#: The main instance of LITPrintDebugger for enhanced printing.

# Wrapper to allow per-call context control
_LIT_INSTANCE = LITPrintDebugger()

import inspect
def _lit_wrapper(*args, **kwargs):
    # Allow per-call includeContext/contextAbsPath
    includeContext = kwargs.pop('includeContext', None)
    contextAbsPath = kwargs.pop('contextAbsPath', None)
    orig_includeContext = _LIT_INSTANCE.includeContext
    orig_contextAbsPath = _LIT_INSTANCE.contextAbsPath
    if includeContext is not None:
        _LIT_INSTANCE.includeContext = includeContext
    if contextAbsPath is not None:
        _LIT_INSTANCE.contextAbsPath = contextAbsPath
    try:
        # Use the original __call__, but pass the correct frame for context
        frame = inspect.currentframe()
        user_frame = frame.f_back
        # Patch: temporarily override inspect.currentframe to return user_frame
        orig_currentframe = inspect.currentframe
        inspect.currentframe = lambda: user_frame
        try:
            # If context is requested, call _format directly for correct arg names
            if _LIT_INSTANCE.includeContext:
                output = _LIT_INSTANCE._format(user_frame, *args)
                _LIT_INSTANCE.outputFunction(output)
                if not args:
                    return None
                elif len(args) == 1:
                    return args[0]
                else:
                    return args
            else:
                return _LIT_INSTANCE.__call__(*args, **kwargs)
        finally:
            inspect.currentframe = orig_currentframe
    finally:
        _LIT_INSTANCE.includeContext = orig_includeContext
        _LIT_INSTANCE.contextAbsPath = orig_contextAbsPath

LIT = _lit_wrapper
litprint = _lit_wrapper
ic = _lit_wrapper
