"""
This module defines color styles for the output of the litprint and lit functions.
It includes several predefined color schemes and the ability to create custom styles.
"""
from pygments.style import Style
from pygments.token import (
    Text, Name, Error, Other,
    String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace,
    Punctuation)


__all__ = ["CyberpunkStyle"]

# Cyberpunk: Neon blue, pink, green on dark blue/purple background
class CyberpunkStyle(Style):
    """
    CYBERPUNK Style - Dark blue/purple background with neon pink, blue, and green highlights.
    """
    background_color = "#0c0c16"  # Dark blue-purple background
    styles = {
        Text:                   "#f0f0ff",  # Light blue-white text
        Whitespace:             "#1a1a2a",  # Slightly lighter background
        Error:                  "#ff2e97",  # Neon pink for errors
        Other:                  "#f0f0ff",  # Light blue-white text
        Name:                   "#f0f0ff",  # Light blue-white text
        Name.Attribute:         "#00ffd9",  # Neon teal
        Name.Builtin:           "#ff2e97",  # Neon pink
        Name.Builtin.Pseudo:    "#ff2e97",  # Neon pink
        Name.Class:             "#00ffd9",  # Neon teal
        Name.Constant:          "#ff2e97",  # Neon pink
        Name.Decorator:         "#fffc58",  # Neon yellow
        Name.Entity:            "#fffc58",  # Neon yellow
        Name.Exception:         "#ff2e97",  # Neon pink
        Name.Function:          "#00ffd9",  # Neon teal
        Name.Property:          "#f0f0ff",  # Light blue-white text
        Name.Label:             "#f0f0ff",  # Light blue-white text
        Name.Namespace:         "#ff2e97",  # Neon pink
        Name.Other:             "#f0f0ff",  # Light blue-white text
        Name.Tag:               "#ff2e97",  # Neon pink
        Name.Variable:          "#f0f0ff",  # Light blue-white text
        Name.Variable.Class:    "#f0f0ff",  # Light blue-white text
        Name.Variable.Global:   "#f0f0ff",  # Light blue-white text
        Name.Variable.Instance: "#f0f0ff",  # Light blue-white text
        String:                 "#00ff6e",  # Neon green
        String.Backtick:        "#00ff6e",  # Neon green
        String.Char:            "#00ff6e",  # Neon green
        String.Doc:             "#3d5a70",  # Muted blue for docstrings
        String.Double:          "#00ff6e",  # Neon green
        String.Escape:          "#fffc58",  # Neon yellow for escape sequences
        String.Heredoc:         "#00ff6e",  # Neon green
        String.Interpol:        "#fffc58",  # Neon yellow for interpolated parts
        String.Other:           "#00ff6e",  # Neon green
        String.Regex:           "#00ff6e",  # Neon green
        String.Single:          "#00ff6e",  # Neon green
        String.Symbol:          "#00ff6e",  # Neon green
        Number:                 "#fffc58",  # Neon yellow
        Number.Float:           "#fffc58",  # Neon yellow
        Number.Hex:             "#fffc58",  # Neon yellow
        Number.Integer:         "#fffc58",  # Neon yellow
        Number.Integer.Long:    "#fffc58",  # Neon yellow
        Number.Oct:             "#fffc58",  # Neon yellow
        Keyword:                "#ff2e97",  # Neon pink
        Keyword.Constant:       "#ff2e97",  # Neon pink
        Keyword.Declaration:    "#ff2e97",  # Neon pink
        Keyword.Namespace:      "#ff2e97",  # Neon pink
        Keyword.Pseudo:         "#ff2e97",  # Neon pink
        Keyword.Reserved:       "#ff2e97",  # Neon pink
        Keyword.Type:           "#00ffd9",  # Neon teal
        Generic:                "#f0f0ff",  # Light blue-white text
        Generic.Deleted:        "#ff2e97 bg:#1a1a2a",  # Neon pink on slightly lighter background
        Generic.Emph:           "italic #f0f0ff",  # Italic light blue-white
        Generic.Error:          "#ff2e97",  # Neon pink
        Generic.Heading:        "bold #f0f0ff",  # Bold light blue-white
        Generic.Inserted:       "#00ff6e bg:#1a1a2a",  # Neon green on slightly lighter background
        Generic.Output:         "#3d5a70",  # Muted blue
        Generic.Prompt:         "#00ffd9",  # Neon teal
        Generic.Strong:         "bold #f0f0ff",  # Bold light blue-white
        Generic.Subheading:     "bold #00ffd9",  # Bold neon teal
        Generic.Traceback:      "#ff2e97",  # Neon pink
        Literal:                "#f0f0ff",  # Light blue-white text
        Literal.Date:           "#00ff6e",  # Neon green
        Comment:                "#3d5a70",  # Muted blue
        Comment.Multiline:      "#3d5a70",  # Muted blue
        Comment.Preproc:        "#ff2e97",  # Neon pink
        Comment.Single:         "#3d5a70",  # Muted blue
        Comment.Special:        "bold #3d5a70",  # Bold muted blue
        Operator:               "#00ffd9",  # Neon teal
        Operator.Word:          "#ff2e97",  # Neon pink
        Punctuation:            "#f0f0ff",  # Light blue-white text
    }
