"""
>>> from litprinter.core import LITPrintDebugger
>>>
>>> debugger = LITPrintDebugger(prefix="DEBUG >>> ")
>>> debugger("Hello", "world!")
DEBUG >>> [__main__.py:3] in () >>> Hello, world!
>>> debugger.format("Formatted output")
'DEBUG >>> [__main__.py:5] in () >>> Formatted output'
>>>
This module contains the core logic for the litprint and lit functions.
It includes the LITPrintDebugger class, which is responsible for formatting
and outputting debug information, source code analysis for variable
names, colorizing output, and configurable options.
"""
#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
from contextlib import contextmanager
from os.path import basename, realpath
from textwrap import dedent
import ast
import inspect
import pprint
import sys
import warnings
import functools
import json

try:
    import colorama
except ImportError:  # pragma: no cover - optional dependency
    colorama = None

try:
    import executing
except ImportError as exc:  # pragma: no cover - required
    raise ImportError(
        "The 'executing' package is required for litprinter."
    ) from exc
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer as PyLexer, Python3Lexer as Py3Lexer
from typing import Any, List, Type, Optional, Dict, Callable
from .coloring import CyberpunkStyle

_absent = object()

def bindStaticVariable(name, value):
    def decorator(fn):
        setattr(fn, name, value)
        return fn
    return decorator

@bindStaticVariable('formatter', Terminal256Formatter(style=CyberpunkStyle))
@bindStaticVariable(
    'lexer', Py3Lexer(ensurenl=False))
def colorize(s):
    self = colorize
    return highlight(s, self.lexer, self.formatter)

@contextmanager
def supportTerminalColorsInWindows():
    colorama.init()
    yield
    colorama.deinit()

def stderrPrint(*args):
    print(*args, file=sys.stderr)

def isLiteral(s):
    try:
        ast.literal_eval(s)
    except Exception:
        return False
    return True

def colorizedStderrPrint(s):
    colored = colorize(s)
    with supportTerminalColorsInWindows():
        stderrPrint(colored)

def styledLitPrint(s):
    colored = colorize(s)
    with supportTerminalColorsInWindows():
        stderrPrint(colored)

DEFAULT_PREFIX = 'LIT| '
DEFAULT_LINE_WRAP_WIDTH = 70
DEFAULT_CONTEXT_DELIMITER = '- '
DEFAULT_OUTPUT_FUNCTION = colorizedStderrPrint
DEFAULT_ARG_TO_STRING_FUNCTION = pprint.pformat
NO_SOURCE_AVAILABLE_WARNING_MESSAGE = (
    'Failed to access the underlying source code for analysis. Was litprint() '
    'invoked in a REPL (e.g. from the command line), a frozen application '
    '(e.g. packaged with PyInstaller), or did the underlying source code '
    'change during execution?')

def callOrValue(obj):
    return obj() if callable(obj) else obj

class Source(executing.Source):
    def get_text_with_indentation(self, node):
        result = self.asttokens().get_text(node)
        if '\n' in result:
            result = ' ' * node.first_token.start[1] + result
            result = dedent(result)
        result = result.strip()
        return result

def prefixLines(prefix, s, startAtLine=0):
    lines = s.splitlines()
    for i in range(startAtLine, len(lines)):
        lines[i] = prefix + lines[i]
    return lines

def prefixFirstLineIndentRemaining(prefix, s):
    indent = ' ' * len(prefix)
    lines = prefixLines(indent, s, startAtLine=1)
    lines[0] = prefix + lines[0]
    return lines

def formatPair(prefix, arg, value):
    if arg is _absent:
        argLines = []
        valuePrefix = prefix
    else:
        argLines = prefixFirstLineIndentRemaining(prefix, arg)
        valuePrefix = argLines[-1] + ': '

    looksLikeAString = (value[0] + value[-1]) in ["''", '""']
    if looksLikeAString:
        valueLines = prefixLines(' ', value, startAtLine=1)
        value = '\n'.join(valueLines)

    valueLines = prefixFirstLineIndentRemaining(valuePrefix, value)
    lines = argLines[:-1] + valueLines
    return '\n'.join(lines)

def singledispatch(func):
    func = functools.singledispatch(func)
    closure = dict(zip(func.register.__code__.co_freevars,
                       func.register.__closure__))
    registry = closure['registry'].cell_contents
    dispatch_cache = closure['dispatch_cache'].cell_contents
    def unregister(cls):
        del registry[cls]
        dispatch_cache.clear()
    func.unregister = unregister
    return func

@singledispatch
def argumentToString(obj):
    s = DEFAULT_ARG_TO_STRING_FUNCTION(obj)
    s = s.replace('\\n', '\n')
    return s

@argumentToString.register(str)
def _(obj):
    if '\n' in obj:
        return "'''" + obj + "'''"
    return "'" + obj.replace('\\', '\\\\') + "'"

class LITPrintDebugger:
    _pairDelimiter = ', '
    lineWrapWidth = DEFAULT_LINE_WRAP_WIDTH
    contextDelimiter = DEFAULT_CONTEXT_DELIMITER
    
    def __init__(self, prefix=DEFAULT_PREFIX,
                 outputFunction=DEFAULT_OUTPUT_FUNCTION,
                 argToStringFunction=argumentToString, includeContext=False,
                 contextAbsPath=False):
        self.enabled = True
        self.prefix = prefix
        self.includeContext = includeContext
        self.outputFunction = outputFunction
        self.argToStringFunction = argToStringFunction
        self.contextAbsPath = contextAbsPath

    def __call__(self, *args):
        if self.enabled:
            callFrame = inspect.currentframe().f_back
            self.outputFunction(self._format(callFrame, *args))

        if not args:
            passthrough = None
        elif len(args) == 1:
            passthrough = args[0]
        else:
            passthrough = args
        return passthrough

    def format(self, *args):
        callFrame = inspect.currentframe().f_back
        out = self._format(callFrame, *args)
        return out

    def _format(self, callFrame, *args):
        prefix = callOrValue(self.prefix)
        context = self._formatContext(callFrame)
        if not args:
            time = self._formatTime()
            out = prefix + context + time
        else:
            if self.includeContext:
                # Format: LIT| [script.py:3] in calculate_total() >>> a: 10, b: 20
                # prefix should be 'LIT| '
                # context: '[script.py:3] in calculate_total()'
                # delimiter: ' >>> '
                # args: 'a: 10, b: 20'
                # Compose output accordingly
                # If user set a custom prefix, use it, else default to 'LIT| '
                used_prefix = prefix if prefix.strip() else 'LIT| '
                context_str = self._formatContext(callFrame)
                args_str = self._formatArgs(callFrame, '', '', args)
                # Remove any prefix/context from args_str
                if args_str.startswith(prefix):
                    args_str = args_str[len(prefix):]
                if args_str.startswith(context_str):
                    args_str = args_str[len(context_str):]
                if args_str.startswith(self.contextDelimiter):
                    args_str = args_str[len(self.contextDelimiter):]
                out = f"{used_prefix}[{context_str}] >>> {args_str.strip()}"
            else:
                if not self.includeContext:
                    context = ''
                out = self._formatArgs(
                    callFrame, prefix, context, args)
        return out

    def _formatArgs(self, callFrame, prefix, context, args):
        callNode = Source.executing(callFrame).node
        if callNode is not None:
            source = Source.for_frame(callFrame)
            sanitizedArgStrs = [
                source.get_text_with_indentation(arg)
                for arg in callNode.args]
        else:
            warnings.warn(
                NO_SOURCE_AVAILABLE_WARNING_MESSAGE,
                category=RuntimeWarning, stacklevel=4)
            sanitizedArgStrs = [_absent] * len(args)
        
        pairs = list(zip(sanitizedArgStrs, args))
        out = self._constructArgumentOutput(prefix, context, pairs)
        return out

    def _constructArgumentOutput(self, prefix, context, pairs):
        def argPrefix(arg):
            return '%s: ' % arg

        pairs = [(arg, self.argToStringFunction(val)) for arg, val in pairs]
        pairStrs = [
            val if (isLiteral(arg) or arg is _absent)
            else (argPrefix(arg) + val)
            for arg, val in pairs]

        allArgsOnOneLine = self._pairDelimiter.join(pairStrs)
        multilineArgs = len(allArgsOnOneLine.splitlines()) > 1
        contextDelimiter = self.contextDelimiter if context else ''
        allPairs = prefix + context + contextDelimiter + allArgsOnOneLine
        firstLineTooLong = len(allPairs.splitlines()[0]) > self.lineWrapWidth

        if multilineArgs or firstLineTooLong:
            if context:
                lines = [prefix + context] + [
                    formatPair(len(prefix) * ' ', arg, value)
                    for arg, value in pairs
                ]
            else:
                argLines = [
                    formatPair('', arg, value)
                    for arg, value in pairs
                ]
                lines = prefixFirstLineIndentRemaining(prefix, '\n'.join(argLines))
        else:
            lines = [prefix + context + contextDelimiter + allArgsOnOneLine]
        return '\n'.join(lines)

    def _formatContext(self, callFrame):
        filename, lineNumber, parentFunction = self._getContext(callFrame)
        if parentFunction != '<module>':
            parentFunction = f'{parentFunction}()'
        # Only return 'script.py:3] in calculate_total()' (no brackets)
        context = f"{filename}:{lineNumber} in {parentFunction}"
        return context

    def _formatTime(self):
        now = datetime.now()
        formatted = now.strftime('%H:%M:%S.%f')[:-3]
        return ' at %s' % formatted

    def _getContext(self, callFrame):
        frameInfo = inspect.getframeinfo(callFrame)
        lineNumber = frameInfo.lineno
        parentFunction = frameInfo.function
        filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
        return filepath, lineNumber, parentFunction

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def configureOutput(self, prefix=_absent, outputFunction=_absent,
                        argToStringFunction=_absent, includeContext=_absent,
                        contextAbsPath=_absent):
        noParameterProvided = all(
            v is _absent for k, v in locals().items() if k != 'self')
        if noParameterProvided:
            raise TypeError('configureOutput() missing at least one argument')

        if prefix is not _absent:
            self.prefix = prefix
        if outputFunction is not _absent:
            self.outputFunction = outputFunction
        if argToStringFunction is not _absent:
            self.argToStringFunction = argToStringFunction
        if includeContext is not _absent:
            self.includeContext = includeContext
        if contextAbsPath is not _absent:
            self.contextAbsPath = contextAbsPath

# Register special formatters for common types
@argumentToString.register(type)
def _format_type(obj, **kwargs):
    """Format type objects nicely"""
    module = obj.__module__
    name = obj.__name__
    if module == 'builtins':
        return f"<class '{name}'>"
    return f"<class '{module}.{name}'>"

@argumentToString.register(Exception)
def _format_exception(obj, **kwargs):
    """Format exceptions with traceback info"""
    return f"<{obj.__class__.__name__}: {str(obj)}>"

@argumentToString.register(bytes)
def _format_bytes(obj, **kwargs):
    """Format bytes objects"""
    if len(obj) > 50:
        return f"<bytes of length {len(obj)}>"
    try:
        return f"b'{obj.decode('utf-8')}'"
    except UnicodeDecodeError:
        return f"<bytes of length {len(obj)}>"

@argumentToString.register(dict)
def _format_dict(obj, **kwargs):
    """Format dictionary objects with better structure"""
    if len(obj) > 50:
        return f"<dict with {len(obj)} items>"

    try:
        # For empty dict
        if not obj:
            return "{}"

        # For small dicts with simple values, keep on one line
        if len(obj) <= 3 and all(isinstance(k, (str, int, float, bool)) and
                               isinstance(v, (str, int, float, bool))
                               for k, v in obj.items()):
            items = ["{!r}: {!r}".format(k, v) for k, v in obj.items()]
            return "{{ {} }}".format(", ".join(items))

        # For larger or complex dicts, format with indentation
        lines = []
        # Sort keys for consistent output
        for k in sorted(obj.keys(), key=str):
            v = obj[k]
            # Format the value
            formatted_val = argumentToString(v, **kwargs)

            # Handle multiline values
            if '\n' in formatted_val:
                # Indent multiline values
                indented_val = formatted_val.replace('\n', '\n    ')
                lines.append(f"  {k!r}: {indented_val}")
            else:
                lines.append(f"  {k!r}: {formatted_val}")

        return "{\n" + "\n".join(lines) + "\n}"
    except Exception:
        # Fall back to json for any errors
        try:
            return json.dumps(obj, indent=2, sort_keys=True, default=str)
        except:
            return f"<dict with {len(obj)} items>"

@argumentToString.register(set)
@argumentToString.register(frozenset)
def _format_set(obj, **kwargs):
    """Format set and frozenset objects"""
    if len(obj) > 20:
        return f"<{obj.__class__.__name__} with {len(obj)} items>"
    try:
        # Sort items for consistent output
        sorted_items = sorted(obj, key=str)
        items = [argumentToString(x, **kwargs) for x in sorted_items]

        # For small sets, keep them on one line
        if len(obj) <= 5:
            return f"{{{', '.join(items)}}}"

        # For larger sets, format with one item per line for better readability
        formatted_items = ',\n  '.join(items)
        return "{{\n  {}\n}}".format(formatted_items)
    except Exception:
        return f"<{obj.__class__.__name__} with {len(obj)} items>"

# Additional formatters for better display
@argumentToString.register(list)
def _format_list(obj, **kwargs):
    """Format list objects with better structure"""
    if len(obj) > 50:
        return f"<list with {len(obj)} items>"

    try:
        # For empty list
        if not obj:
            return "[]"

        # For small lists with simple values, keep on one line
        if len(obj) <= 5 and all(isinstance(x, (str, int, float, bool)) for x in obj):
            items = [repr(x) for x in obj]
            return "[{}]".format(", ".join(items))

        # For larger or complex lists, format with indentation
        items = []
        for x in obj:
            # Format the value
            formatted_val = argumentToString(x, **kwargs)

            # Handle multiline values
            if '\n' in formatted_val:
                # Indent multiline values
                indented_val = formatted_val.replace('\n', '\n  ')
                items.append(f"  {indented_val}")
            else:
                items.append(f"  {formatted_val}")

        return "[\n" + "\n".join(items) + "\n]"
    except Exception:
        return f"<list with {len(obj)} items>"

@argumentToString.register(tuple)
def _format_tuple(obj, **kwargs):
    """Format tuple objects with better structure"""
    if len(obj) > 50:
        return f"<tuple with {len(obj)} items>"

    try:
        # For empty tuple
        if not obj:
            return "()"

        # For single item tuple, ensure trailing comma
        if len(obj) == 1:
            return f"({argumentToString(obj[0], **kwargs)},)"

        # For small tuples with simple values, keep on one line
        if len(obj) <= 5 and all(isinstance(x, (str, int, float, bool)) for x in obj):
            items = [repr(x) for x in obj]
            return "({})".format(", ".join(items))

        # For larger or complex tuples, format with indentation
        items = []
        for x in obj:
            # Format the value
            formatted_val = argumentToString(x, **kwargs)

            # Handle multiline values
            if '\n' in formatted_val:
                # Indent multiline values
                indented_val = formatted_val.replace('\n', '\n  ')
                items.append(f"  {indented_val}")
            else:
                items.append(f"  {formatted_val}")

        return "(\n" + "\n".join(items) + "\n)"
    except Exception:
        return f"<tuple with {len(obj)} items>"
