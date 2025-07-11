"""
OCEAN Style - A calming theme with blues and teals reminiscent of the ocean.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class OCEAN(Style):
    """
    OCEAN Style - A calming theme with blues and teals reminiscent of the ocean.
    """
    background_color = "#0f2d3d"  # Deep ocean blue background
    styles = {
        Text:                   "#e0f0ff",  # Light blue-white text
        Whitespace:             "#1e3d4d",  # Slightly lighter background
        Error:                  "#ff5a5a",  # Coral red for errors
        Other:                  "#e0f0ff",  # Light blue-white text
        Name:                   "#e0f0ff",  # Light blue-white text
        Name.Attribute:         "#88ddff",  # Bright cyan
        Name.Builtin:           "#5fb3b3",  # Teal
        Name.Builtin.Pseudo:    "#5fb3b3",  # Teal
        Name.Class:             "#88ddff",  # Bright cyan
        Name.Constant:          "#c2c2ff",  # Light purple
        Name.Decorator:         "#5fb3b3",  # Teal
        Name.Entity:            "#5fb3b3",  # Teal
        Name.Exception:         "#ff5a5a",  # Coral red
        Name.Function:          "#88ddff",  # Bright cyan
        Name.Property:          "#e0f0ff",  # Light blue-white text
        Name.Label:             "#e0f0ff",  # Light blue-white text
        Name.Namespace:         "#c2c2ff",  # Light purple
        Name.Other:             "#e0f0ff",  # Light blue-white text
        Name.Tag:               "#5fb3b3",  # Teal
        Name.Variable:          "#e0f0ff",  # Light blue-white text
        Name.Variable.Class:    "#e0f0ff",  # Light blue-white text
        Name.Variable.Global:   "#e0f0ff",  # Light blue-white text
        Name.Variable.Instance: "#e0f0ff",  # Light blue-white text
        String:                 "#98e6c6",  # Seafoam green
        String.Backtick:        "#98e6c6",  # Seafoam green
        String.Char:            "#98e6c6",  # Seafoam green
        String.Doc:             "#7a9cb2",  # Muted blue for docstrings
        String.Double:          "#98e6c6",  # Seafoam green
        String.Escape:          "#c2c2ff",  # Light purple for escape sequences
        String.Heredoc:         "#98e6c6",  # Seafoam green
        String.Interpol:        "#c2c2ff",  # Light purple for interpolated parts
        String.Other:           "#98e6c6",  # Seafoam green
        String.Regex:           "#98e6c6",  # Seafoam green
        String.Single:          "#98e6c6",  # Seafoam green
        String.Symbol:          "#98e6c6",  # Seafoam green
        Number:                 "#c2c2ff",  # Light purple
        Number.Float:           "#c2c2ff",  # Light purple
        Number.Hex:             "#c2c2ff",  # Light purple
        Number.Integer:         "#c2c2ff",  # Light purple
        Number.Integer.Long:    "#c2c2ff",  # Light purple
        Number.Oct:             "#c2c2ff",  # Light purple
        Keyword:                "#5fb3b3",  # Teal
        Keyword.Constant:       "#c2c2ff",  # Light purple
        Keyword.Declaration:    "#5fb3b3",  # Teal
        Keyword.Namespace:      "#5fb3b3",  # Teal
        Keyword.Pseudo:         "#5fb3b3",  # Teal
        Keyword.Reserved:       "#5fb3b3",  # Teal
        Keyword.Type:           "#88ddff",  # Bright cyan
        Generic:                "#e0f0ff",  # Light blue-white text
        Generic.Deleted:        "#ff5a5a bg:#1e3d4d",  # Coral red on slightly lighter background
        Generic.Emph:           "italic #e0f0ff",  # Italic light blue-white
        Generic.Error:          "#ff5a5a",  # Coral red
        Generic.Heading:        "bold #e0f0ff",  # Bold light blue-white
        Generic.Inserted:       "#98e6c6 bg:#1e3d4d",  # Seafoam green on slightly lighter background
        Generic.Output:         "#7a9cb2",  # Muted blue
        Generic.Prompt:         "#88ddff",  # Bright cyan
        Generic.Strong:         "bold #e0f0ff",  # Bold light blue-white
        Generic.Subheading:     "bold #88ddff",  # Bold bright cyan
        Generic.Traceback:      "#ff5a5a",  # Coral red
        Literal:                "#e0f0ff",  # Light blue-white text
        Literal.Date:           "#98e6c6",  # Seafoam green
        Comment:                "#7a9cb2",  # Muted blue
        Comment.Multiline:      "#7a9cb2",  # Muted blue
        Comment.Preproc:        "#5fb3b3",  # Teal
        Comment.Single:         "#7a9cb2",  # Muted blue
        Comment.Special:        "bold #7a9cb2",  # Bold muted blue
        Operator:               "#88ddff",  # Bright cyan
        Operator.Word:          "#5fb3b3",  # Teal
        Punctuation:            "#e0f0ff",  # Light blue-white text
    }
