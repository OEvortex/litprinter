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
from .litprint import *
from .core import LITPrintDebugger, argumentToString
from .builtins import install, uninstall
from .coloring import *
from . import traceback
from .console import *
try:
    from .panel import *
except ImportError:
    # Panel module may not be available in all environments
    pass

__version__ = '0.2.1'
