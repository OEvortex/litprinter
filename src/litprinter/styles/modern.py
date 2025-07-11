"""
MODERN Style - A high-contrast dark theme with blues, purples, and greens.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class MODERN(Style):
    """
    MODERN Style - A high-contrast dark theme with blues, purples, and greens.
    """
    background_color = "#1a1a1a"  # Very dark grey background
    styles = {
        Text:                   "#f8f8f2",  # Off-white text
        Whitespace:             "#2d2d2d",  # Slightly lighter background
        Error:                  "#ff5370",  # Bright red for errors
        Other:                  "#f8f8f2",  # Off-white text
        Name:                   "#f8f8f2",  # Off-white text
        Name.Attribute:         "#82aaff",  # Bright blue
        Name.Builtin:           "#c792ea",  # Purple
        Name.Builtin.Pseudo:    "#c792ea",  # Purple
        Name.Class:             "#82aaff",  # Bright blue
        Name.Constant:          "#c792ea",  # Purple
        Name.Decorator:         "#89ddff",  # Cyan
        Name.Entity:            "#89ddff",  # Cyan
        Name.Exception:         "#f07178",  # Coral
        Name.Function:          "#82aaff",  # Bright blue
        Name.Property:          "#f8f8f2",  # Off-white text
        Name.Label:             "#f8f8f2",  # Off-white text
        Name.Namespace:         "#c792ea",  # Purple
        Name.Other:             "#f8f8f2",  # Off-white text
        Name.Tag:               "#f07178",  # Coral
        Name.Variable:          "#f8f8f2",  # Off-white text
        Name.Variable.Class:    "#f8f8f2",  # Off-white text
        Name.Variable.Global:   "#f8f8f2",  # Off-white text
        Name.Variable.Instance: "#f8f8f2",  # Off-white text
        String:                 "#c3e88d",  # Green
        String.Backtick:        "#c3e88d",  # Green
        String.Char:            "#c3e88d",  # Green
        String.Doc:             "#546e7a",  # Grey-blue for docstrings
        String.Double:          "#c3e88d",  # Green
        String.Escape:          "#f78c6c",  # Orange for escape sequences
        String.Heredoc:         "#c3e88d",  # Green
        String.Interpol:        "#f78c6c",  # Orange for interpolated parts
        String.Other:           "#c3e88d",  # Green
        String.Regex:           "#89ddff",  # Cyan
        String.Single:          "#c3e88d",  # Green
        String.Symbol:          "#c3e88d",  # Green
        Number:                 "#f78c6c",  # Orange
        Number.Float:           "#f78c6c",  # Orange
        Number.Hex:             "#f78c6c",  # Orange
        Number.Integer:         "#f78c6c",  # Orange
        Number.Integer.Long:    "#f78c6c",  # Orange
        Number.Oct:             "#f78c6c",  # Orange
        Keyword:                "#c792ea",  # Purple
        Keyword.Constant:       "#c792ea",  # Purple
        Keyword.Declaration:    "#c792ea",  # Purple
        Keyword.Namespace:      "#c792ea",  # Purple
        Keyword.Pseudo:         "#c792ea",  # Purple
        Keyword.Reserved:       "#c792ea",  # Purple
        Keyword.Type:           "#ffcb6b",  # Yellow
        Generic:                "#f8f8f2",  # Off-white text
        Generic.Deleted:        "#ff5370 bg:#2d2d2d",  # Red on slightly lighter background
        Generic.Emph:           "italic #f8f8f2",  # Italic off-white
        Generic.Error:          "#ff5370",  # Red
        Generic.Heading:        "bold #f8f8f2",  # Bold off-white
        Generic.Inserted:       "#c3e88d bg:#2d2d2d",  # Green on slightly lighter background
        Generic.Output:         "#546e7a",  # Grey-blue
        Generic.Prompt:         "#82aaff",  # Bright blue
        Generic.Strong:         "bold #f8f8f2",  # Bold off-white
        Generic.Subheading:     "bold #82aaff",  # Bold bright blue
        Generic.Traceback:      "#ff5370",  # Red
        Literal:                "#f8f8f2",  # Off-white text
        Literal.Date:           "#c3e88d",  # Green
        Comment:                "#546e7a",  # Grey-blue
        Comment.Multiline:      "#546e7a",  # Grey-blue
        Comment.Preproc:        "#89ddff",  # Cyan
        Comment.Single:         "#546e7a",  # Grey-blue
        Comment.Special:        "bold #546e7a",  # Bold grey-blue
        Operator:               "#89ddff",  # Cyan
        Operator.Word:          "#c792ea",  # Purple
        Punctuation:            "#89ddff",  # Cyan
    }
