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
import ast
import inspect
import pprint
import sys
import warnings
from datetime import datetime
import functools
from contextlib import contextmanager
from os.path import basename, realpath
from textwrap import dedent
try:
    import colorama  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    colorama = None

try:
    import executing
except ImportError as exc:  # pragma: no cover - required
    raise ImportError(
        "The 'executing' package is required for litprinter."
    ) from exc
from pygments import highlight
from pygments.formatters import Terminal256Formatter, HtmlFormatter
from pygments.lexers import PythonLexer as PyLexer, Python3Lexer as Py3Lexer
from pygments.token import Token
from typing import Any, List, Type, Optional, Dict, Callable
from .styles import (
    JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI,
    SOLARIZED, NORD, GITHUB, VSCODE, MATERIAL, RETRO, OCEAN, AUTUMN,
    SYNTHWAVE, FOREST, MONOCHROME, SUNSET, create_custom_style
)
import json

_absent = object()

def bindStaticVariable(name, value):
    def decorator(fn):
        setattr(fn, name, value)
        return fn
    return decorator

@bindStaticVariable('formatter', Terminal256Formatter(style=CYBERPUNK))
@bindStaticVariable(
    'lexer', Py3Lexer(ensurenl=False))
def colorize(s, color_style=None):
    if color_style is None:
        formatter = Terminal256Formatter(style=CYBERPUNK)  # Use CYBERPUNK as default
    elif isinstance(color_style, str):
        # Allow selecting style by name (case-insensitive)
        style_name = color_style.lower()
        if style_name == 'jarvis':
            formatter = Terminal256Formatter(style=JARVIS)
        elif style_name == 'rich':
            formatter = Terminal256Formatter(style=RICH)
        elif style_name == 'modern':
            formatter = Terminal256Formatter(style=MODERN)
        elif style_name == 'neon':
            formatter = Terminal256Formatter(style=NEON)
        elif style_name == 'cyberpunk':
            formatter = Terminal256Formatter(style=CYBERPUNK)
        elif style_name == 'dracula':
            formatter = Terminal256Formatter(style=DRACULA)
        elif style_name == 'monokai':
            formatter = Terminal256Formatter(style=MONOKAI)
        elif style_name == 'solarized':
            formatter = Terminal256Formatter(style=SOLARIZED)
        elif style_name == 'nord':
            formatter = Terminal256Formatter(style=NORD)
        elif style_name == 'github':
            formatter = Terminal256Formatter(style=GITHUB)
        elif style_name == 'vscode':
            formatter = Terminal256Formatter(style=VSCODE)
        elif style_name == 'material':
            formatter = Terminal256Formatter(style=MATERIAL)
        elif style_name == 'retro':
            formatter = Terminal256Formatter(style=RETRO)
        elif style_name == 'ocean':
            formatter = Terminal256Formatter(style=OCEAN)
        elif style_name == 'autumn':
            formatter = Terminal256Formatter(style=AUTUMN)
        elif style_name == 'synthwave':
            formatter = Terminal256Formatter(style=SYNTHWAVE)
        elif style_name == 'forest':
            formatter = Terminal256Formatter(style=FOREST)
        elif style_name == 'monochrome':
            formatter = Terminal256Formatter(style=MONOCHROME)
        elif style_name == 'sunset':
            formatter = Terminal256Formatter(style=SUNSET)
        else:
            # Try to use the string as a style name
            formatter = Terminal256Formatter(style=color_style)
    elif isinstance(color_style, dict):
        CustomStyle = create_custom_style('CustomStyle', color_style)
        formatter = Terminal256Formatter(style=CustomStyle)
    else:
        formatter = Terminal256Formatter(style=color_style)
    return highlight(s, colorize.lexer, formatter)

@contextmanager
def supportTerminalColorsInWindows():
    if colorama is not None:
        colorama.init()
        try:
            yield
        finally:
            colorama.deinit()
    else:
        yield

def stderrPrint(*args, sep=' ', end='\n', flush=False):
    print(*args, file=sys.stderr, sep=sep, end=end, flush=flush)

def isLiteral(s):
    try:
        ast.literal_eval(s)
    except Exception:
        return False
    return True

def colorizedStderrPrint(s, color_style=None, sep=' ', end='\n', flush=False):
    colored = colorize(s, color_style)
    with supportTerminalColorsInWindows():
        stderrPrint(colored, sep=sep, end=end, flush=flush)


def stdoutPrint(s, color_style=None, sep=' ', end='\n', flush=False):
    """Print to stdout with optional color support."""
    if color_style is not None:
        s = colorize(s, color_style)
        with supportTerminalColorsInWindows():
            print(s, sep=sep, end=end, flush=flush)
    else:
        print(s, sep=sep, end=end, flush=flush)

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
    if isinstance(value, str) and len(value) > LITPrintDebugger.lineWrapWidth:
        valueLines = []
        for i in range(0, len(value), LITPrintDebugger.lineWrapWidth):
            valueLines.extend(prefixFirstLineIndentRemaining(valuePrefix, value[i:i+LITPrintDebugger.lineWrapWidth]))
            valuePrefix = ' ' * len(valuePrefix)
        lines = argLines[:-1] + valueLines
    else:
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
def argumentToString(obj, **kwargs):
    """
    Convert an object to a string representation.
    This function can be extended for custom types using the register decorator.

    Example:
    @argumentToString.register(numpy.ndarray)
    def _(obj):
        return f"ndarray, shape={obj.shape}, dtype={obj.dtype}"
    """
    if isinstance(obj, str):
        # For strings, handle special formatting
        if len(obj) > 100 and '\n' in obj:
            # For multiline strings, format with proper indentation
            lines = obj.splitlines()
            if len(lines) > 10:
                # Truncate very long multiline strings
                return '\n'.join(lines[:5] + ['...'] + lines[-5:])
            return obj
        elif len(obj) > 100:
            # Truncate very long single-line strings
            return obj[:97] + '...'
        return obj

    # Handle different types with better formatting
    if isinstance(obj, dict):
        try:
            if len(obj) > 50:
                # For very large dicts, show summary
                return f"<dict with {len(obj)} items>"
            # Use json.dumps with indent=2 for better readability
            return json.dumps(obj, indent=2, sort_keys=True, default=str)
        except (TypeError, ValueError):
            pass

    if isinstance(obj, (list, tuple)):
        try:
            if len(obj) > 50:
                # For very large lists/tuples, show summary
                return f"<{obj.__class__.__name__} with {len(obj)} items>"
            # Format lists and tuples with json for better readability
            return json.dumps(obj, indent=2, default=str)
        except (TypeError, ValueError):
            pass

    # Handle special types
    if hasattr(obj, '__dict__') and not isinstance(obj, type):
        # For objects with __dict__, show attributes
        attrs = {}
        for key, value in obj.__dict__.items():
            if not key.startswith('_'):
                try:
                    # Limit attribute value length for readability
                    str_val = str(value)
                    if len(str_val) > 50:
                        str_val = str_val[:47] + '...'
                    attrs[key] = str_val
                except Exception:
                    attrs[key] = "<error in __str__>"

        if attrs:
            try:
                return f"<{obj.__class__.__name__} {json.dumps(attrs, indent=2, default=str)}>"
            except (TypeError, ValueError):
                pass

    # Try general JSON serialization
    try:
        return json.dumps(obj, indent=2, default=str)
    except (TypeError, ValueError):
        # Fall back to pprint for complex objects
        try:
            return pprint.pformat(obj, indent=2, width=100, **kwargs)
        except Exception:
            # Last resort for objects that cause errors in pprint
            return f"<{obj.__class__.__name__} at {hex(id(obj))}>"

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

class LITPrintDebugger:
    _pairDelimiter = ', '
    lineWrapWidth = DEFAULT_LINE_WRAP_WIDTH
    contextDelimiter = DEFAULT_CONTEXT_DELIMITER
    global_enabled = True

    def __init__(self, prefix: str = DEFAULT_PREFIX,
                 outputFunction: Any = DEFAULT_OUTPUT_FUNCTION,
                 argToStringFunction: Any = argumentToString, includeContext: bool = True,
                 contextAbsPath: bool = False, log_file: Optional[str] = None, color_style: Optional[Any] = None,
                 disable_colors: bool = False, contextDelimiter: str = DEFAULT_CONTEXT_DELIMITER,
                 log_timestamp: bool = False, style: str = 'default', filter_types: Optional[List[Type]] = None, flush: bool = False,
                 pprint_options: Optional[dict] = None, rich_styles: Optional[dict] = None):
        self.enabled = True
        self.prefix = prefix
        self.includeContext = includeContext
        self.outputFunction = outputFunction if outputFunction is not None else DEFAULT_OUTPUT_FUNCTION
        self.argToStringFunction = argToStringFunction
        self.contextAbsPath = contextAbsPath
        self.log_file = log_file
        self.color_style = color_style
        self.disable_colors = disable_colors
        self.contextDelimiter = contextDelimiter if contextDelimiter is not None else ''
        self.log_timestamp = log_timestamp
        self.style = style
        self.filter_types = filter_types
        self.flush = flush
        self.pprint_options = pprint_options if pprint_options is not None else {}
        self.rich_styles = rich_styles if rich_styles is not None else {}
        self._formatters: Dict[Type, Callable] = {}

    def __call__(self, *args):
        """
        Call the debugger with arguments to print them.
        Returns the arguments for easy integration into existing code.
        """
        if self.enabled and LITPrintDebugger.global_enabled:
            callFrame = inspect.currentframe().f_back
            formatted_output = self._format(callFrame, *args)
            if self.disable_colors:
                stderrPrint(formatted_output, flush=self.flush)
            else:
                self.outputFunction(formatted_output, self.color_style)
            if self.log_file:
                self._log_output(formatted_output)

        # Return the arguments for easy integration into existing code
        if not args:
            passthrough = None
        elif len(args) == 1:
            passthrough = args[0]
        else:
            passthrough = args
        return passthrough

    def format(self, *args):
        """
        Format the arguments without printing them.
        Returns the formatted string.
        """
        callFrame = inspect.currentframe().f_back
        out = self._format(callFrame, *args)
        return out

    def _format(self, callFrame, *args):
        prefix = callOrValue(self.prefix)
        context = self._formatContext(callFrame) if self.includeContext else ''
        if not args:
            time = self._formatTime()
            out = prefix + context + time
        else:
            out = self._formatArgs(
                callFrame, prefix, context, args)
        if not context:
            self.contextDelimiter = ''
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
        if self.filter_types:
            pairs = [(arg, val) for arg, val in pairs if any(isinstance(val, t) for t in self.filter_types)]
        out = self._constructArgumentOutput(prefix, context, pairs)
        return out

    def _constructArgumentOutput(self, prefix, context, pairs):
        def argPrefix(arg):
            return '%s: ' % arg

        # Process values with better formatting
        processed_pairs = []
        for arg, val in pairs:
            # Format the value with proper indentation for multi-line output
            formatted_val = self.argToStringFunction(val, **self.pprint_options)
            processed_pairs.append((arg, formatted_val))

        pairs = processed_pairs

        if len(pairs) == 0:
            return prefix + context

        # Add visual separator for better readability
        # Use a more prominent separator with better spacing
        separator = " │ " if context else " "

        # For single value output
        if len(pairs) == 1:
            arg, val = pairs[0]
            if arg is _absent or isLiteral(arg):
                # For simple values
                return prefix + context + separator + val
            else:
                # For named values with better formatting for multiline output
                if '\n' in val:
                    # For multiline values, add a line break after the name
                    # and indent the value for better readability
                    indented_val = '\n  ' + val.replace('\n', '\n  ')
                    return prefix + context + separator + argPrefix(arg) + indented_val
                else:
                    # For single line values
                    return prefix + context + separator + argPrefix(arg) + val

        # Format multiple arguments
        pairStrs = []
        max_arg_len = 0

        # First pass to determine the maximum argument name length for alignment
        for arg, _ in pairs:
            if not (isLiteral(arg) or arg is _absent):
                max_arg_len = max(max_arg_len, len(str(arg)))

        # Second pass to format each pair with proper alignment
        for arg, val in pairs:
            if isLiteral(arg) or arg is _absent:
                pairStrs.append(val)
            else:
                # Check if value is multiline
                if '\n' in val:
                    # For multiline values, add a line break after the name
                    # and indent the value for better readability
                    indented_val = '\n  ' + val.replace('\n', '\n  ')
                    pairStrs.append(f"{arg:{max_arg_len}}: {indented_val}")
                else:
                    # For single line values, align the colons
                    pairStrs.append(f"{arg:{max_arg_len}}: {val}")

        # Join with clear separator and better spacing
        if any('\n' in s for s in pairStrs):
            # If any value is multiline, put each pair on a new line for better readability
            joined = '\n  '.join(pairStrs)
            allArgsOnOneLine = f"\n  {joined}"
        else:
            # For simple values, keep them on one line with comma separation
            allArgsOnOneLine = ",  ".join(pairStrs)

        contextDelimiter = self.contextDelimiter if context else ''

        return prefix + context + contextDelimiter + separator + allArgsOnOneLine

    def _formatContext(self, callFrame):
        filename, lineNumber, parentFunction = self._getContext(callFrame)
        if parentFunction == "<module>":
            parentFunction = "()"
        else:
            parentFunction = '%s()' % parentFunction

        # Format for clickable links in supported terminals
        if self.contextAbsPath:
            # Use format that VSCode and other editors recognize as clickable
            # This format creates a clickable link in most modern terminals and editors
            # Format: file:line:column
            context = '%s:%s:%s in %s' % (filename, lineNumber, 1, parentFunction)
        else:
            # For relative paths, still make them clickable but with brackets for better visibility
            context = '[%s:%s] in %s' % (filename, lineNumber, parentFunction)

        return context

    def _formatTime(self):
        now = datetime.now()
        formatted = now.strftime('%H:%M:%S.%f')[:-3]
        return ' at %s' % formatted

    def _getContext(self, callFrame):
        frames = inspect.stack()

        # Start from the frame where _getContext is called (which is 2 frames back)
        for frame_info in frames[2:]:
            if frame_info.function not in ['_formatContext', '_format', 'lit', 'litprint', 'log']: # Skip litprint internals
                lineNumber = frame_info.lineno
                parentFunction = frame_info.function
                filepath = (realpath if self.contextAbsPath else basename)(frame_info.filename)
                return filepath, lineNumber, parentFunction

        # If no other frame is found, return module information
        frameInfo = inspect.getframeinfo(callFrame)
        lineNumber = frameInfo.lineno
        parentFunction = frameInfo.function
        filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
        return filepath, lineNumber, parentFunction

    def enable(self):
        """Enable the debugger"""
        self.enabled = True

    def disable(self):
        """Disable the debugger"""
        self.enabled = False

    @classmethod
    def enable_globally(cls):
        """Enable all debugger instances"""
        cls.global_enabled = True

    @classmethod
    def disable_globally(cls):
        """Disable all debugger instances"""
        cls.global_enabled = False

    def register_formatter(self, cls: Type, formatter: Callable):
        """Register a custom formatter for a specific type"""
        self._formatters[cls] = formatter

    def unregister_formatter(self, cls: Type):
        """Unregister a custom formatter"""
        if cls in self._formatters:
            del self._formatters[cls]

    def _log_output(self, output):
        with open(self.log_file, 'a') as f:
            if self.log_timestamp:
                now = datetime.now()
                formatted = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                f.write(f'[{formatted}] {output}\n')
            else:
                f.write(output + '\n')

    def configureOutput(self, prefix=None, outputFunction=None, argToStringFunction=None,
                        includeContext=None, contextAbsPath=None):
        """
        Configure the output format and behavior.

        Args:
            prefix: String or function that returns a string to prefix output
            outputFunction: Function to handle output (default: print to stderr)
            argToStringFunction: Function to convert arguments to strings
            includeContext: Whether to include file, line, and function context
            contextAbsPath: Whether to use absolute paths in context
        """
        if prefix is not None:
            self.prefix = prefix
        if outputFunction is not None:
            self.outputFunction = outputFunction
        if argToStringFunction is not None:
            self.argToStringFunction = argToStringFunction
        if includeContext is not None:
            self.includeContext = includeContext
        if contextAbsPath is not None:
            self.contextAbsPath = contextAbsPath


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
