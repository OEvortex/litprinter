"""
FOREST Style - A theme with various shades of green and brown, inspired by forests.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class FOREST(Style):
    """
    FOREST Style - A theme with various shades of green and brown, inspired by forests.
    """
    background_color = "#1c2a1c"  # Dark forest green background
    styles = {
        Text:                   "#d8e8d8",  # Light green-white text
        Whitespace:             "#2c3a2c",  # Slightly lighter background
        Error:                  "#e55c5c",  # Red for errors
        Other:                  "#d8e8d8",  # Light green-white text
        Name:                   "#d8e8d8",  # Light green-white text
        Name.Attribute:         "#a0d0a0",  # Medium green
        Name.Builtin:           "#70a070",  # Darker green
        Name.Builtin.Pseudo:    "#70a070",  # Darker green
        Name.Class:             "#a0d0a0",  # Medium green
        Name.Constant:          "#d0b080",  # Light brown
        Name.Decorator:         "#a0d0a0",  # Medium green
        Name.Entity:            "#a0d0a0",  # Medium green
        Name.Exception:         "#e55c5c",  # Red
        Name.Function:          "#a0d0a0",  # Medium green
        Name.Property:          "#d8e8d8",  # Light green-white text
        Name.Label:             "#d8e8d8",  # Light green-white text
        Name.Namespace:         "#70a070",  # Darker green
        Name.Other:             "#d8e8d8",  # Light green-white text
        Name.Tag:               "#70a070",  # Darker green
        Name.Variable:          "#d8e8d8",  # Light green-white text
        Name.Variable.Class:    "#d8e8d8",  # Light green-white text
        Name.Variable.Global:   "#d8e8d8",  # Light green-white text
        Name.Variable.Instance: "#d8e8d8",  # Light green-white text
        String:                 "#b0d090",  # Light olive green
        String.Backtick:        "#b0d090",  # Light olive green
        String.Char:            "#b0d090",  # Light olive green
        String.Doc:             "#6a8a6a",  # Muted green for docstrings
        String.Double:          "#b0d090",  # Light olive green
        String.Escape:          "#d0b080",  # Light brown for escape sequences
        String.Heredoc:         "#b0d090",  # Light olive green
        String.Interpol:        "#d0b080",  # Light brown for interpolated parts
        String.Other:           "#b0d090",  # Light olive green
        String.Regex:           "#b0d090",  # Light olive green
        String.Single:          "#b0d090",  # Light olive green
        String.Symbol:          "#b0d090",  # Light olive green
        Number:                 "#d0b080",  # Light brown
        Number.Float:           "#d0b080",  # Light brown
        Number.Hex:             "#d0b080",  # Light brown
        Number.Integer:         "#d0b080",  # Light brown
        Number.Integer.Long:    "#d0b080",  # Light brown
        Number.Oct:             "#d0b080",  # Light brown
        Keyword:                "#70a070",  # Darker green
        Keyword.Constant:       "#d0b080",  # Light brown
        Keyword.Declaration:    "#70a070",  # Darker green
        Keyword.Namespace:      "#70a070",  # Darker green
        Keyword.Pseudo:         "#70a070",  # Darker green
        Keyword.Reserved:       "#70a070",  # Darker green
        Keyword.Type:           "#a0d0a0",  # Medium green
        Generic:                "#d8e8d8",  # Light green-white text
        Generic.Deleted:        "#e55c5c bg:#2c3a2c",  # Red on slightly lighter background
        Generic.Emph:           "italic #d8e8d8",  # Italic light green-white
        Generic.Error:          "#e55c5c",  # Red
        Generic.Heading:        "bold #d8e8d8",  # Bold light green-white
        Generic.Inserted:       "#b0d090 bg:#2c3a2c",  # Light olive green on slightly lighter background
        Generic.Output:         "#6a8a6a",  # Muted green
        Generic.Prompt:         "#a0d0a0",  # Medium green
        Generic.Strong:         "bold #d8e8d8",  # Bold light green-white
        Generic.Subheading:     "bold #a0d0a0",  # Bold medium green
        Generic.Traceback:      "#e55c5c",  # Red
        Literal:                "#d8e8d8",  # Light green-white text
        Literal.Date:           "#b0d090",  # Light olive green
        Comment:                "#6a8a6a",  # Muted green
        Comment.Multiline:      "#6a8a6a",  # Muted green
        Comment.Preproc:        "#70a070",  # Darker green
        Comment.Single:         "#6a8a6a",  # Muted green
        Comment.Special:        "bold #6a8a6a",  # Bold muted green
        Operator:               "#a0d0a0",  # Medium green
        Operator.Word:          "#70a070",  # Darker green
        Punctuation:            "#d8e8d8",  # Light green-white text
    }
