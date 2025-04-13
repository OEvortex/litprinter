"""
RETRO Style - Inspired by old-school terminal colors and early computing.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class RETRO(Style):
    """
    RETRO Style - Inspired by old-school terminal colors and early computing.
    """
    background_color = "#000000"  # Black background
    styles = {
        Text:                   "#00ff00",  # Bright green text (classic terminal)
        Whitespace:             "#003300",  # Dark green for whitespace
        Error:                  "#ff0000",  # Bright red for errors
        Other:                  "#00ff00",  # Bright green text
        Name:                   "#00ff00",  # Bright green text
        Name.Attribute:         "#ffff00",  # Yellow
        Name.Builtin:           "#00ffff",  # Cyan
        Name.Builtin.Pseudo:    "#00ffff",  # Cyan
        Name.Class:             "#ffff00",  # Yellow
        Name.Constant:          "#ff00ff",  # Magenta
        Name.Decorator:         "#ffff00",  # Yellow
        Name.Entity:            "#ffff00",  # Yellow
        Name.Exception:         "#ff0000",  # Bright red
        Name.Function:          "#ffff00",  # Yellow
        Name.Property:          "#00ff00",  # Bright green text
        Name.Label:             "#00ff00",  # Bright green text
        Name.Namespace:         "#ffff00",  # Yellow
        Name.Other:             "#00ff00",  # Bright green text
        Name.Tag:               "#00ffff",  # Cyan
        Name.Variable:          "#00ff00",  # Bright green text
        Name.Variable.Class:    "#00ff00",  # Bright green text
        Name.Variable.Global:   "#00ff00",  # Bright green text
        Name.Variable.Instance: "#00ff00",  # Bright green text
        String:                 "#ff00ff",  # Magenta
        String.Backtick:        "#ff00ff",  # Magenta
        String.Char:            "#ff00ff",  # Magenta
        String.Doc:             "#888888",  # Grey for docstrings
        String.Double:          "#ff00ff",  # Magenta
        String.Escape:          "#ffff00",  # Yellow for escape sequences
        String.Heredoc:         "#ff00ff",  # Magenta
        String.Interpol:        "#ffff00",  # Yellow for interpolated parts
        String.Other:           "#ff00ff",  # Magenta
        String.Regex:           "#ff00ff",  # Magenta
        String.Single:          "#ff00ff",  # Magenta
        String.Symbol:          "#ff00ff",  # Magenta
        Number:                 "#00ffff",  # Cyan
        Number.Float:           "#00ffff",  # Cyan
        Number.Hex:             "#00ffff",  # Cyan
        Number.Integer:         "#00ffff",  # Cyan
        Number.Integer.Long:    "#00ffff",  # Cyan
        Number.Oct:             "#00ffff",  # Cyan
        Keyword:                "#ffff00",  # Yellow
        Keyword.Constant:       "#00ffff",  # Cyan
        Keyword.Declaration:    "#ffff00",  # Yellow
        Keyword.Namespace:      "#ffff00",  # Yellow
        Keyword.Pseudo:         "#ffff00",  # Yellow
        Keyword.Reserved:       "#ffff00",  # Yellow
        Keyword.Type:           "#00ffff",  # Cyan
        Generic:                "#00ff00",  # Bright green text
        Generic.Deleted:        "#ff0000 bg:#330000",  # Red on dark red background
        Generic.Emph:           "italic #00ff00",  # Italic green
        Generic.Error:          "#ff0000",  # Bright red
        Generic.Heading:        "bold #00ff00",  # Bold green
        Generic.Inserted:       "#00ff00 bg:#003300",  # Green on dark green background
        Generic.Output:         "#888888",  # Grey
        Generic.Prompt:         "#00ffff",  # Cyan
        Generic.Strong:         "bold #00ff00",  # Bold green
        Generic.Subheading:     "bold #00ffff",  # Bold cyan
        Generic.Traceback:      "#ff0000",  # Bright red
        Literal:                "#00ff00",  # Bright green text
        Literal.Date:           "#ff00ff",  # Magenta
        Comment:                "#888888",  # Grey
        Comment.Multiline:      "#888888",  # Grey
        Comment.Preproc:        "#ffff00",  # Yellow
        Comment.Single:         "#888888",  # Grey
        Comment.Special:        "bold #888888",  # Bold grey
        Operator:               "#ffffff",  # White
        Operator.Word:          "#ffff00",  # Yellow
        Punctuation:            "#ffffff",  # White
    }
