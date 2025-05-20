"""
>>> from litprinter import lit
>>>
>>> lit("Hello, world!")
LIT -> [__main__.py:3] in () >>> Hello, world!
>>>
>>> def my_function(a, b):
...    lit(a, b)
>>> my_function(1, 2)
LIT -> [__main__.py:6] in my_function() >>> a: 1, b: 2

This module provides the 'lit' function, which is an enhanced print function for
debugging purposes. It leverages the LITPrintDebugger class from 'core.py' and allows
for configurable prefix, output functions, and context inclusion. It's designed
to make debugging more straightforward by offering clear output with context information.
"""
import inspect
from .core import LITPrintDebugger, argumentToString, DEFAULT_PREFIX
from typing import Any, List, Type, Optional

def lit(
    *args,
    prefix: Optional[str] = None,
    outputFunction: Optional[Any] = None,
    argToStringFunction: Optional[Any] = None,
    includeContext: bool = True,
    contextAbsPath: bool = False,
    log_file: Optional[str] = None,
    color_style: Optional[Any] = None,
    disable_colors: bool = False,
    contextDelimiter: Optional[str] = None,
    log_timestamp: bool = False,
    sep: str = ' ',
    end: str = '\n',
    style: str = 'default',
    filter_types: Optional[List[Type]] = None,
    flush: bool = False,
    pprint_options: Optional[dict] = None,
    rich_styles: Optional[dict] = None,
    **kwargs
):
    """
    Prints the given arguments with enhanced formatting and debugging capabilities.

    Args:
        *args: The arguments to print.
        prefix (str, optional): A prefix to add to the output. Defaults to 'LIT -> '.
        outputFunction (callable, optional): A function to use for output. Defaults to colorizedStderrPrint.
        argToStringFunction (callable, optional): A function to convert arguments to strings. Defaults to argumentToString.
        includeContext (bool, optional): Whether to include context information (filename, line number, function name). Defaults to True.
        contextAbsPath (bool, optional): Whether to use absolute paths for context information. Defaults to False.
        log_file (str, optional): A file to log the output to. Defaults to None.
        color_style (Any, optional): A color style to use for the output. Defaults to None.
        disable_colors (bool, optional): Whether to disable colors in the output. Defaults to False.
        contextDelimiter (str, optional): A delimiter to use for context information. Defaults to '- '.
        log_timestamp (bool, optional): Whether to include a timestamp in the log file. Defaults to False.
        sep (str, optional): The separator between arguments. Defaults to ' '.
        end (str, optional): The end-of-line character. Defaults to '\n'.
        style (str, optional): The output style ('default' or 'json'). Defaults to 'default'.
        filter_types (List[Type], optional): A list of types to filter arguments by. Defaults to None.
        flush (bool, optional): Whether to force the output to be written to the console immediately. Defaults to False.
        pprint_options (dict, optional): Options to pass to pprint.pformat. Defaults to None.
        rich_styles (dict, optional): Options to pass to rich for styling. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the LITPrintDebugger constructor.
    
    Returns:
        The arguments passed to the function, allowing it to be used inline in expressions.
    """
    debugger = LITPrintDebugger(**kwargs,
        prefix=prefix if prefix is not None else DEFAULT_PREFIX,
        outputFunction=outputFunction,
        argToStringFunction=argToStringFunction if argToStringFunction is not None else argumentToString,
        includeContext=includeContext,
        contextAbsPath=contextAbsPath,
        log_file=log_file,
        color_style=color_style,
        disable_colors=disable_colors,
        contextDelimiter=contextDelimiter,
        log_timestamp=log_timestamp,
        style=style,
        filter_types=filter_types,
        flush=flush,
        pprint_options=pprint_options,
        rich_styles=rich_styles
    )
    
    # Return the arguments for easy integration into existing code
    if not args:
        return None
    elif len(args) == 1:
        passthrough = args[0]
    else:
        passthrough = args
        
    # Format and output
    formatted_output = debugger._format(inspect.currentframe().f_back, *args)
    if debugger.disable_colors:
        from .core import stderrPrint
        stderrPrint(formatted_output, sep=sep, end=end, flush=flush)
    else:
        if debugger.outputFunction is print:
            from .core import stdoutPrint
            stdoutPrint(formatted_output, debugger.color_style, sep=sep, end=end, flush=flush)
        else:
            debugger.outputFunction(formatted_output, debugger.color_style, sep=sep, end=end, flush=flush)
        
    return passthrough

def log(
    *args,
    level: str = "debug",
    prefix: Optional[str] = None,
    outputFunction: Optional[Any] = None,
    argToStringFunction: Optional[Any] = None,
    includeContext: bool = True,
    contextAbsPath: bool = False,
    log_file: Optional[str] = None,
    color_style: Optional[Any] = None,
    disable_colors: bool = False,
    contextDelimiter: Optional[str] = None,
    log_timestamp: bool = False,
    sep: str = ' ',
    end: str = '\n',
    style: str = 'default',
    filter_types: Optional[List[Type]] = None,
    flush: bool = False,
    pprint_options: Optional[dict] = None,
    rich_styles: Optional[dict] = None,
    **kwargs
):
    """
    Logs the given arguments with enhanced formatting and debugging capabilities.

    Args:
        *args: The arguments to print.
        level (str, optional): The log level (debug, info, warning, error). Defaults to "debug".
        prefix (str, optional): A prefix to add to the output. Defaults to 'LIT -> '.
        outputFunction (callable, optional): A function to use for output. Defaults to colorizedStderrPrint.
        argToStringFunction (callable, optional): A function to convert arguments to strings. Defaults to argumentToString.
        includeContext (bool, optional): Whether to include context information (filename, line number, function name). Defaults to True.
        contextAbsPath (bool, optional): Whether to use absolute paths for context information. Defaults to False.
        log_file (str, optional): A file to log the output to. Defaults to None.
        color_style (Any, optional): A color style to use for the output. Defaults to None.
        disable_colors (bool, optional): Whether to disable colors in the output. Defaults to False.
        contextDelimiter (str, optional): A delimiter to use for context information. Defaults to '- '.
        log_timestamp (bool, optional): Whether to include a timestamp in the log file. Defaults to False.
        sep (str, optional): The separator between arguments. Defaults to ' '.
        end (str, optional): The end-of-line character. Defaults to '\n'.
        style (str, optional): The output style ('default' or 'json'). Defaults to 'default'.
        filter_types (List[Type], optional): A list of types to filter arguments by. Defaults to None.
        flush (bool, optional): Whether to force the output to be written to the console immediately. Defaults to False.
        pprint_options (dict, optional): Options to pass to pprint.pformat. Defaults to None.
        rich_styles (dict, optional): Options to pass to rich for styling. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the LITPrintDebugger constructor.
    
    Returns:
        The arguments passed to the function, allowing it to be used inline in expressions.
    """
    debugger = LITPrintDebugger(**kwargs,
        prefix=prefix if prefix is not None else f"[{level.upper()}] " + DEFAULT_PREFIX,
        outputFunction=outputFunction,
        argToStringFunction=argToStringFunction if argToStringFunction is not None else argumentToString,
        includeContext=includeContext,
        contextAbsPath=contextAbsPath,
        log_file=log_file,
        color_style=color_style,
        disable_colors=disable_colors,
        contextDelimiter=contextDelimiter,
        log_timestamp=log_timestamp,
        style=style,
        filter_types=filter_types,
        flush=flush,
        pprint_options=pprint_options,
        rich_styles=rich_styles
    )
    
    # Return the arguments for easy integration into existing code
    if not args:
        return None
    elif len(args) == 1:
        passthrough = args[0]
    else:
        passthrough = args
        
    # Format and output
    formatted_output = debugger._format(inspect.currentframe().f_back, *args)
    if debugger.disable_colors:
        from .core import stderrPrint
        stderrPrint(formatted_output, sep=sep, end=end, flush=flush)
    else:
        if debugger.outputFunction is print:
            from .core import stdoutPrint
            stdoutPrint(formatted_output, debugger.color_style, sep=sep, end=end, flush=flush)
        else:
            debugger.outputFunction(formatted_output, debugger.color_style, sep=sep, end=end, flush=flush)
        
    return passthrough

# Aliases for compatibility with icecream
ic = lit
format = lit.format if hasattr(lit, 'format') else None
