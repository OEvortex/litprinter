"""
SUNSET Style - A warm theme with oranges, reds, and purples reminiscent of a sunset.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class SUNSET(Style):
    """
    SUNSET Style - A warm theme with oranges, reds, and purples reminiscent of a sunset.
    """
    background_color = "#282233"  # Dark purple-blue background
    styles = {
        Text:                   "#f8e8e0",  # Light peach text
        Whitespace:             "#382a43",  # Slightly lighter background
        Error:                  "#ff5555",  # Bright red for errors
        Other:                  "#f8e8e0",  # Light peach text
        Name:                   "#f8e8e0",  # Light peach text
        Name.Attribute:         "#ffb380",  # Light orange
        Name.Builtin:           "#ff8080",  # Salmon
        Name.Builtin.Pseudo:    "#ff8080",  # Salmon
        Name.Class:             "#ffb380",  # Light orange
        Name.Constant:          "#c991e1",  # Light purple
        Name.Decorator:         "#ffb380",  # Light orange
        Name.Entity:            "#ffb380",  # Light orange
        Name.Exception:         "#ff5555",  # Bright red
        Name.Function:          "#ffb380",  # Light orange
        Name.Property:          "#f8e8e0",  # Light peach text
        Name.Label:             "#f8e8e0",  # Light peach text
        Name.Namespace:         "#ff8080",  # Salmon
        Name.Other:             "#f8e8e0",  # Light peach text
        Name.Tag:               "#ff8080",  # Salmon
        Name.Variable:          "#f8e8e0",  # Light peach text
        Name.Variable.Class:    "#f8e8e0",  # Light peach text
        Name.Variable.Global:   "#f8e8e0",  # Light peach text
        Name.Variable.Instance: "#f8e8e0",  # Light peach text
        String:                 "#ffd073",  # Golden yellow
        String.Backtick:        "#ffd073",  # Golden yellow
        String.Char:            "#ffd073",  # Golden yellow
        String.Doc:             "#a18daf",  # Muted purple for docstrings
        String.Double:          "#ffd073",  # Golden yellow
        String.Escape:          "#c991e1",  # Light purple for escape sequences
        String.Heredoc:         "#ffd073",  # Golden yellow
        String.Interpol:        "#c991e1",  # Light purple for interpolated parts
        String.Other:           "#ffd073",  # Golden yellow
        String.Regex:           "#ffd073",  # Golden yellow
        String.Single:          "#ffd073",  # Golden yellow
        String.Symbol:          "#ffd073",  # Golden yellow
        Number:                 "#c991e1",  # Light purple
        Number.Float:           "#c991e1",  # Light purple
        Number.Hex:             "#c991e1",  # Light purple
        Number.Integer:         "#c991e1",  # Light purple
        Number.Integer.Long:    "#c991e1",  # Light purple
        Number.Oct:             "#c991e1",  # Light purple
        Keyword:                "#ff8080",  # Salmon
        Keyword.Constant:       "#c991e1",  # Light purple
        Keyword.Declaration:    "#ff8080",  # Salmon
        Keyword.Namespace:      "#ff8080",  # Salmon
        Keyword.Pseudo:         "#ff8080",  # Salmon
        Keyword.Reserved:       "#ff8080",  # Salmon
        Keyword.Type:           "#ffb380",  # Light orange
        Generic:                "#f8e8e0",  # Light peach text
        Generic.Deleted:        "#ff5555 bg:#382a43",  # Bright red on slightly lighter background
        Generic.Emph:           "italic #f8e8e0",  # Italic light peach
        Generic.Error:          "#ff5555",  # Bright red
        Generic.Heading:        "bold #f8e8e0",  # Bold light peach
        Generic.Inserted:       "#ffd073 bg:#382a43",  # Golden yellow on slightly lighter background
        Generic.Output:         "#a18daf",  # Muted purple
        Generic.Prompt:         "#ffb380",  # Light orange
        Generic.Strong:         "bold #f8e8e0",  # Bold light peach
        Generic.Subheading:     "bold #ffb380",  # Bold light orange
        Generic.Traceback:      "#ff5555",  # Bright red
        Literal:                "#f8e8e0",  # Light peach text
        Literal.Date:           "#ffd073",  # Golden yellow
        Comment:                "#a18daf",  # Muted purple
        Comment.Multiline:      "#a18daf",  # Muted purple
        Comment.Preproc:        "#ff8080",  # Salmon
        Comment.Single:         "#a18daf",  # Muted purple
        Comment.Special:        "bold #a18daf",  # Bold muted purple
        Operator:               "#ffb380",  # Light orange
        Operator.Word:          "#ff8080",  # Salmon
        Punctuation:            "#f8e8e0",  # Light peach text
    }
