import re
import sys
from typing import Iterable, List
from .colors import Colors

# Regular expression to match simple markup like [red]text[/red]
_MARKUP_RE = re.compile(r"\[(\/)?([a-zA-Z_]+)\]")

# Mapping of color/style names to ANSI codes
_STYLE_MAP = {name.lower(): getattr(Colors, name) for name in dir(Colors) if name.isupper()}


def _parse_markup(text: str) -> str:
    """Parse simple color markup in *text* and return ANSI formatted string."""
    result: List[str] = []
    stack: List[str] = []
    pos = 0
    for match in _MARKUP_RE.finditer(text):
        result.append(text[pos:match.start()])
        closing, tag = match.groups()
        tag = tag.lower()
        if closing:
            if stack and stack[-1] == tag:
                stack.pop()
                result.append(Colors.RESET)
            else:
                # unmatched closing tag, keep it literal
                result.append(match.group(0))
        else:
            ansi = _STYLE_MAP.get(tag)
            if ansi:
                stack.append(tag)
                result.append(ansi)
            else:
                result.append(match.group(0))
        pos = match.end()
    result.append(text[pos:])
    if stack:
        result.append(Colors.RESET)
    return "".join(result)


def cprint(
    *objects: Iterable,
    sep: str = " ",
    end: str = "\n",
    file=sys.stdout,
    flush: bool = False,
) -> None:
    """Print objects with simple Rich-like markup support.

    Use syntax like ``[red]error[/red]`` or ``[bold]bold text[/bold]``. Unknown
    tags are printed literally.
    """
    text = sep.join(str(o) for o in objects)
    formatted = _parse_markup(text)
    print(formatted, file=file, end=end, flush=flush)

