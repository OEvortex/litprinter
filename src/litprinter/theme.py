#!/usr/bin/env python3
"""
LitPrinter Theme

The single syntax-highlighting style used by every litprinter surface: ``ic()``
values, ``ic.print(..., highlight=True)`` and the traceback renderer.

The palette is tuned for long debugging sessions: low-chroma blues for
structure, a warm accent for values, and reserved red/yellow/green that only
appear on things that are actually wrong. It is deliberately closer to
readable-editor themes than to "loud" ones.

Author: OEvortex <koulabhay25@gmail.com>
License: MIT
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

__all__ = ['LitPrinterStyle', 'STYLE']


class LitPrinterStyle(Style):
    """The one and only litprinter theme.

    Structure (punctuation, whitespace, operators) is muted blue-gray so it
    recedes; identifiers are a calm cyan; strings are warm and easy to scan;
    numbers get a soft green; errors get the only strong red.
    """

    background_color = '#11131a'
    highlight_color = '#1f2330'

    # Palette
    FG = '#c9d1d9'
    MUTED = '#6b7280'
    COMMENT = '#5c6470'
    KEYWORD = '#c792ea'
    NAME = '#82aaff'
    FUNCTION = '#82aaff'
    CLASS = '#ffcb6b'
    STRING = '#c3e88d'
    NUMBER = '#f78c6c'
    OPERATOR = '#89ddff'
    PUNCTUATION = '#7c8798'
    CONSTANT = '#f78c6c'
    BUILTIN = '#82aaff'
    ERROR = '#ff5370'
    GENERIC = '#c3e88d'
    DELETED = '#ff5370'
    INSERTED = '#c3e88d'
    HEADING = '#82aaff'

    styles = {
        Text: FG,
        Whitespace: '#4b5563',
        Comment: COMMENT,
        Comment.Preproc: KEYWORD,
        Comment.Special: KEYWORD,
        Keyword: KEYWORD,
        Keyword.Constant: CONSTANT,
        Keyword.Type: CLASS,
        Name: NAME,
        Name.Attribute: FUNCTION,
        Name.Builtin: BUILTIN,
        Name.Builtin.Pseudo: KEYWORD,
        Name.Class: CLASS,
        Name.Constant: CONSTANT,
        Name.Decorator: FUNCTION,
        Name.Exception: ERROR,
        Name.Function: FUNCTION,
        Name.Function.Magic: FUNCTION,
        Name.Namespace: KEYWORD,
        Name.Tag: KEYWORD,
        Name.Variable: NAME,
        Name.Variable.Class: NAME,
        Name.Variable.Global: NAME,
        Name.Variable.Instance: NAME,
        Literal: STRING,
        String: STRING,
        String.Affix: KEYWORD,
        String.Delimiter: '#a3be8c',
        String.Doc: COMMENT,
        String.Escape: OPERATOR,
        String.Interpol: OPERATOR,
        String.Other: STRING,
        String.Regex: '#f78c6c',
        Number: NUMBER,
        Number.Bin: NUMBER,
        Number.Float: NUMBER,
        Number.Hex: NUMBER,
        Number.Integer: NUMBER,
        Number.Integer.Long: NUMBER,
        Number.Oct: NUMBER,
        Operator: OPERATOR,
        Operator.Word: KEYWORD,
        Punctuation: PUNCTUATION,
        Generic: GENERIC,
        Generic.Deleted: DELETED,
        Generic.Emph: 'italic',
        Generic.Error: ERROR,
        Generic.Heading: HEADING,
        Generic.Inserted: INSERTED,
        Generic.Output: MUTED,
        Generic.Prompt: 'bold #82aaff',
        Generic.Strong: 'bold',
        Generic.Subheading: KEYWORD,
        Generic.Traceback: MUTED,
        Error: ERROR,
        Other: MUTED,
    }


#: Shared instance used by the formatter and the traceback renderer.
STYLE = LitPrinterStyle
