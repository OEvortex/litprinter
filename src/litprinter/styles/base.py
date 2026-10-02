"""
Shared Pygments imports for every style module in this package.

The 19 theme modules import their tokens from here so the palette stays
consistent and each theme file only declares what it customises.
"""

from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Other,
    Punctuation,
    String,
    Text,
    Whitespace,
)

__all__ = [
    "Style",
    "Comment",
    "Error",
    "Generic",
    "Keyword",
    "Literal",
    "Name",
    "Number",
    "Operator",
    "Other",
    "Punctuation",
    "String",
    "Text",
    "Whitespace",
]
