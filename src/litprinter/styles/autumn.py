"""
AUTUMN Style - A warm theme with autumn colors like oranges, reds, and browns.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class AUTUMN(Style):
    """
    AUTUMN Style - A warm theme with autumn colors like oranges, reds, and browns.
    """
    background_color = "#2d2118"  # Dark brown background
    styles = {
        Text:                   "#f0e0c0",  # Light tan text
        Whitespace:             "#3d3128",  # Slightly lighter background
        Error:                  "#e05050",  # Bright red for errors
        Other:                  "#f0e0c0",  # Light tan text
        Name:                   "#f0e0c0",  # Light tan text
        Name.Attribute:         "#e6a264",  # Orange
        Name.Builtin:           "#d48c4b",  # Darker orange
        Name.Builtin.Pseudo:    "#d48c4b",  # Darker orange
        Name.Class:             "#e6a264",  # Orange
        Name.Constant:          "#b07050",  # Brown
        Name.Decorator:         "#e6a264",  # Orange
        Name.Entity:            "#e6a264",  # Orange
        Name.Exception:         "#e05050",  # Bright red
        Name.Function:          "#e6a264",  # Orange
        Name.Property:          "#f0e0c0",  # Light tan text
        Name.Label:             "#f0e0c0",  # Light tan text
        Name.Namespace:         "#d48c4b",  # Darker orange
        Name.Other:             "#f0e0c0",  # Light tan text
        Name.Tag:               "#d48c4b",  # Darker orange
        Name.Variable:          "#f0e0c0",  # Light tan text
        Name.Variable.Class:    "#f0e0c0",  # Light tan text
        Name.Variable.Global:   "#f0e0c0",  # Light tan text
        Name.Variable.Instance: "#f0e0c0",  # Light tan text
        String:                 "#a0c070",  # Olive green
        String.Backtick:        "#a0c070",  # Olive green
        String.Char:            "#a0c070",  # Olive green
        String.Doc:             "#7a6e5c",  # Muted brown for docstrings
        String.Double:          "#a0c070",  # Olive green
        String.Escape:          "#b07050",  # Brown for escape sequences
        String.Heredoc:         "#a0c070",  # Olive green
        String.Interpol:        "#b07050",  # Brown for interpolated parts
        String.Other:           "#a0c070",  # Olive green
        String.Regex:           "#a0c070",  # Olive green
        String.Single:          "#a0c070",  # Olive green
        String.Symbol:          "#a0c070",  # Olive green
        Number:                 "#c08040",  # Rust orange
        Number.Float:           "#c08040",  # Rust orange
        Number.Hex:             "#c08040",  # Rust orange
        Number.Integer:         "#c08040",  # Rust orange
        Number.Integer.Long:    "#c08040",  # Rust orange
        Number.Oct:             "#c08040",  # Rust orange
        Keyword:                "#d48c4b",  # Darker orange
        Keyword.Constant:       "#b07050",  # Brown
        Keyword.Declaration:    "#d48c4b",  # Darker orange
        Keyword.Namespace:      "#d48c4b",  # Darker orange
        Keyword.Pseudo:         "#d48c4b",  # Darker orange
        Keyword.Reserved:       "#d48c4b",  # Darker orange
        Keyword.Type:           "#e6a264",  # Orange
        Generic:                "#f0e0c0",  # Light tan text
        Generic.Deleted:        "#e05050 bg:#3d3128",  # Bright red on slightly lighter background
        Generic.Emph:           "italic #f0e0c0",  # Italic light tan
        Generic.Error:          "#e05050",  # Bright red
        Generic.Heading:        "bold #f0e0c0",  # Bold light tan
        Generic.Inserted:       "#a0c070 bg:#3d3128",  # Olive green on slightly lighter background
        Generic.Output:         "#7a6e5c",  # Muted brown
        Generic.Prompt:         "#e6a264",  # Orange
        Generic.Strong:         "bold #f0e0c0",  # Bold light tan
        Generic.Subheading:     "bold #e6a264",  # Bold orange
        Generic.Traceback:      "#e05050",  # Bright red
        Literal:                "#f0e0c0",  # Light tan text
        Literal.Date:           "#a0c070",  # Olive green
        Comment:                "#7a6e5c",  # Muted brown
        Comment.Multiline:      "#7a6e5c",  # Muted brown
        Comment.Preproc:        "#d48c4b",  # Darker orange
        Comment.Single:         "#7a6e5c",  # Muted brown
        Comment.Special:        "bold #7a6e5c",  # Bold muted brown
        Operator:               "#e6a264",  # Orange
        Operator.Word:          "#d48c4b",  # Darker orange
        Punctuation:            "#f0e0c0",  # Light tan text
    }
