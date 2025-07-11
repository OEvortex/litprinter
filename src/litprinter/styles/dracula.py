"""
DRACULA Style - A popular dark theme with a distinct purple and cyan palette.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class DRACULA(Style):
    """
    DRACULA Style - A popular dark theme with a distinct purple and cyan palette.
    """
    background_color = "#282a36"  # Dark background
    styles = {
        Text:                   "#f8f8f2",  # Light grey text
        Whitespace:             "#44475a",  # Slightly lighter background
        Error:                  "#ff5555",  # Red for errors
        Other:                  "#f8f8f2",  # Light grey text
        Name:                   "#f8f8f2",  # Light grey text
        Name.Attribute:         "#50fa7b",  # Green
        Name.Builtin:           "#8be9fd",  # Cyan
        Name.Builtin.Pseudo:    "#8be9fd",  # Cyan
        Name.Class:             "#8be9fd",  # Cyan
        Name.Constant:          "#bd93f9",  # Purple
        Name.Decorator:         "#50fa7b",  # Green
        Name.Entity:            "#50fa7b",  # Green
        Name.Exception:         "#ff5555",  # Red
        Name.Function:          "#50fa7b",  # Green
        Name.Property:          "#f8f8f2",  # Light grey text
        Name.Label:             "#f8f8f2",  # Light grey text
        Name.Namespace:         "#ff79c6",  # Pink
        Name.Other:             "#f8f8f2",  # Light grey text
        Name.Tag:               "#ff79c6",  # Pink
        Name.Variable:          "#f8f8f2",  # Light grey text
        Name.Variable.Class:    "#f8f8f2",  # Light grey text
        Name.Variable.Global:   "#f8f8f2",  # Light grey text
        Name.Variable.Instance: "#f8f8f2",  # Light grey text
        String:                 "#f1fa8c",  # Yellow
        String.Backtick:        "#f1fa8c",  # Yellow
        String.Char:            "#f1fa8c",  # Yellow
        String.Doc:             "#6272a4",  # Comment blue for docstrings
        String.Double:          "#f1fa8c",  # Yellow
        String.Escape:          "#ff79c6",  # Pink for escape sequences
        String.Heredoc:         "#f1fa8c",  # Yellow
        String.Interpol:        "#ff79c6",  # Pink for interpolated parts
        String.Other:           "#f1fa8c",  # Yellow
        String.Regex:           "#f1fa8c",  # Yellow
        String.Single:          "#f1fa8c",  # Yellow
        String.Symbol:          "#f1fa8c",  # Yellow
        Number:                 "#bd93f9",  # Purple
        Number.Float:           "#bd93f9",  # Purple
        Number.Hex:             "#bd93f9",  # Purple
        Number.Integer:         "#bd93f9",  # Purple
        Number.Integer.Long:    "#bd93f9",  # Purple
        Number.Oct:             "#bd93f9",  # Purple
        Keyword:                "#ff79c6",  # Pink
        Keyword.Constant:       "#bd93f9",  # Purple
        Keyword.Declaration:    "#8be9fd",  # Cyan
        Keyword.Namespace:      "#ff79c6",  # Pink
        Keyword.Pseudo:         "#ff79c6",  # Pink
        Keyword.Reserved:       "#ff79c6",  # Pink
        Keyword.Type:           "#8be9fd",  # Cyan
        Generic:                "#f8f8f2",  # Light grey text
        Generic.Deleted:        "#ff5555 bg:#44475a",  # Red on slightly lighter background
        Generic.Emph:           "italic #f8f8f2",  # Italic light grey
        Generic.Error:          "#ff5555",  # Red
        Generic.Heading:        "bold #f8f8f2",  # Bold light grey
        Generic.Inserted:       "#50fa7b bg:#44475a",  # Green on slightly lighter background
        Generic.Output:         "#6272a4",  # Comment blue
        Generic.Prompt:         "#8be9fd",  # Cyan
        Generic.Strong:         "bold #f8f8f2",  # Bold light grey
        Generic.Subheading:     "bold #8be9fd",  # Bold cyan
        Generic.Traceback:      "#ff5555",  # Red
        Literal:                "#f8f8f2",  # Light grey text
        Literal.Date:           "#f1fa8c",  # Yellow
        Comment:                "#6272a4",  # Comment blue
        Comment.Multiline:      "#6272a4",  # Comment blue
        Comment.Preproc:        "#ff79c6",  # Pink
        Comment.Single:         "#6272a4",  # Comment blue
        Comment.Special:        "bold #6272a4",  # Bold comment blue
        Operator:               "#ff79c6",  # Pink
        Operator.Word:          "#ff79c6",  # Pink
        Punctuation:            "#f8f8f2",  # Light grey text
    }
