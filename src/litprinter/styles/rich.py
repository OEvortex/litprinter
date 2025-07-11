"""
RICH Style - Inspired by the Rich library's default theme.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class RICH(Style):
    """
    RICH Style - Inspired by the Rich library's default theme.
    """
    background_color = "#202020"  # Dark background
    styles = {
        Text:                   "#d0d0d0",  # Light grey text
        Whitespace:             "#404040",  # Slightly lighter background
        Error:                  "#ff5555",  # Bright red for errors
        Other:                  "#d0d0d0",  # Light grey text
        Name:                   "#d0d0d0",  # Light grey text
        Name.Attribute:         "#7dd3fc",  # Light blue
        Name.Builtin:           "#ff9e64",  # Orange
        Name.Builtin.Pseudo:    "#ff9e64",  # Orange
        Name.Class:             "#7dd3fc",  # Light blue
        Name.Constant:          "#bb9af7",  # Purple
        Name.Decorator:         "#ff9e64",  # Orange
        Name.Entity:            "#ff9e64",  # Orange
        Name.Exception:         "#f7768e",  # Pink
        Name.Function:          "#7dd3fc",  # Light blue
        Name.Property:          "#d0d0d0",  # Light grey text
        Name.Label:             "#d0d0d0",  # Light grey text
        Name.Namespace:         "#ff9e64",  # Orange
        Name.Other:             "#d0d0d0",  # Light grey text
        Name.Tag:               "#f7768e",  # Pink
        Name.Variable:          "#d0d0d0",  # Light grey text
        Name.Variable.Class:    "#d0d0d0",  # Light grey text
        Name.Variable.Global:   "#d0d0d0",  # Light grey text
        Name.Variable.Instance: "#d0d0d0",  # Light grey text
        String:                 "#9ece6a",  # Green
        String.Backtick:        "#9ece6a",  # Green
        String.Char:            "#9ece6a",  # Green
        String.Doc:             "#6a9955",  # Darker green for docstrings
        String.Double:          "#9ece6a",  # Green
        String.Escape:          "#ff9e64",  # Orange for escape sequences
        String.Heredoc:         "#9ece6a",  # Green
        String.Interpol:        "#ff9e64",  # Orange for interpolated parts
        String.Other:           "#9ece6a",  # Green
        String.Regex:           "#9ece6a",  # Green
        String.Single:          "#9ece6a",  # Green
        String.Symbol:          "#9ece6a",  # Green
        Number:                 "#bb9af7",  # Purple
        Number.Float:           "#bb9af7",  # Purple
        Number.Hex:             "#bb9af7",  # Purple
        Number.Integer:         "#bb9af7",  # Purple
        Number.Integer.Long:    "#bb9af7",  # Purple
        Number.Oct:             "#bb9af7",  # Purple
        Keyword:                "#f7768e",  # Pink
        Keyword.Constant:       "#bb9af7",  # Purple
        Keyword.Declaration:    "#f7768e",  # Pink
        Keyword.Namespace:      "#f7768e",  # Pink
        Keyword.Pseudo:         "#f7768e",  # Pink
        Keyword.Reserved:       "#f7768e",  # Pink
        Keyword.Type:           "#7dd3fc",  # Light blue
        Generic:                "#d0d0d0",  # Light grey text
        Generic.Deleted:        "#f7768e bg:#3f3f3f",  # Pink on slightly lighter background
        Generic.Emph:           "italic #d0d0d0",  # Italic light grey
        Generic.Error:          "#f7768e",  # Pink
        Generic.Heading:        "bold #d0d0d0",  # Bold light grey
        Generic.Inserted:       "#9ece6a bg:#3f3f3f",  # Green on slightly lighter background
        Generic.Output:         "#6a9955",  # Darker green
        Generic.Prompt:         "#7dd3fc",  # Light blue
        Generic.Strong:         "bold #d0d0d0",  # Bold light grey
        Generic.Subheading:     "bold #7dd3fc",  # Bold light blue
        Generic.Traceback:      "#f7768e",  # Pink
        Literal:                "#d0d0d0",  # Light grey text
        Literal.Date:           "#9ece6a",  # Green
        Comment:                "#6a9955",  # Darker green
        Comment.Multiline:      "#6a9955",  # Darker green
        Comment.Preproc:        "#ff9e64",  # Orange
        Comment.Single:         "#6a9955",  # Darker green
        Comment.Special:        "bold #6a9955",  # Bold darker green
        Operator:               "#d0d0d0",  # Light grey text
        Operator.Word:          "#f7768e",  # Pink
        Punctuation:            "#d0d0d0",  # Light grey text
    }
