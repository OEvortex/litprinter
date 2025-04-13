"""
NEON Style - Extremely bright, high-contrast colors on a black background.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class NEON(Style):
    """
    NEON Style - Extremely bright, high-contrast colors on a black background.
    """
    background_color = "#000000"  # Pure black background
    styles = {
        Text:                   "#ffffff",  # Pure white text
        Whitespace:             "#333333",  # Dark grey for whitespace
        Error:                  "#ff0055",  # Bright pink for errors
        Other:                  "#ffffff",  # Pure white text
        Name:                   "#ffffff",  # Pure white text
        Name.Attribute:         "#00ffff",  # Cyan
        Name.Builtin:           "#ff00ff",  # Magenta
        Name.Builtin.Pseudo:    "#ff00ff",  # Magenta
        Name.Class:             "#00ffff",  # Cyan
        Name.Constant:          "#ff00ff",  # Magenta
        Name.Decorator:         "#ffff00",  # Yellow
        Name.Entity:            "#ffff00",  # Yellow
        Name.Exception:         "#ff0055",  # Bright pink
        Name.Function:          "#00ffff",  # Cyan
        Name.Property:          "#ffffff",  # Pure white text
        Name.Label:             "#ffffff",  # Pure white text
        Name.Namespace:         "#ff00ff",  # Magenta
        Name.Other:             "#ffffff",  # Pure white text
        Name.Tag:               "#ff0055",  # Bright pink
        Name.Variable:          "#ffffff",  # Pure white text
        Name.Variable.Class:    "#ffffff",  # Pure white text
        Name.Variable.Global:   "#ffffff",  # Pure white text
        Name.Variable.Instance: "#ffffff",  # Pure white text
        String:                 "#00ff00",  # Bright green
        String.Backtick:        "#00ff00",  # Bright green
        String.Char:            "#00ff00",  # Bright green
        String.Doc:             "#00aa00",  # Darker green for docstrings
        String.Double:          "#00ff00",  # Bright green
        String.Escape:          "#ffff00",  # Yellow for escape sequences
        String.Heredoc:         "#00ff00",  # Bright green
        String.Interpol:        "#ffff00",  # Yellow for interpolated parts
        String.Other:           "#00ff00",  # Bright green
        String.Regex:           "#00ff00",  # Bright green
        String.Single:          "#00ff00",  # Bright green
        String.Symbol:          "#00ff00",  # Bright green
        Number:                 "#ffff00",  # Yellow
        Number.Float:           "#ffff00",  # Yellow
        Number.Hex:             "#ffff00",  # Yellow
        Number.Integer:         "#ffff00",  # Yellow
        Number.Integer.Long:    "#ffff00",  # Yellow
        Number.Oct:             "#ffff00",  # Yellow
        Keyword:                "#ff00ff",  # Magenta
        Keyword.Constant:       "#ff00ff",  # Magenta
        Keyword.Declaration:    "#ff00ff",  # Magenta
        Keyword.Namespace:      "#ff00ff",  # Magenta
        Keyword.Pseudo:         "#ff00ff",  # Magenta
        Keyword.Reserved:       "#ff00ff",  # Magenta
        Keyword.Type:           "#00ffff",  # Cyan
        Generic:                "#ffffff",  # Pure white text
        Generic.Deleted:        "#ff0055 bg:#330011",  # Bright pink on dark pink background
        Generic.Emph:           "italic #ffffff",  # Italic white
        Generic.Error:          "#ff0055",  # Bright pink
        Generic.Heading:        "bold #ffffff",  # Bold white
        Generic.Inserted:       "#00ff00 bg:#003300",  # Bright green on dark green background
        Generic.Output:         "#555555",  # Medium grey
        Generic.Prompt:         "#00ffff",  # Cyan
        Generic.Strong:         "bold #ffffff",  # Bold white
        Generic.Subheading:     "bold #00ffff",  # Bold cyan
        Generic.Traceback:      "#ff0055",  # Bright pink
        Literal:                "#ffffff",  # Pure white text
        Literal.Date:           "#00ff00",  # Bright green
        Comment:                "#555555",  # Medium grey
        Comment.Multiline:      "#555555",  # Medium grey
        Comment.Preproc:        "#ff00ff",  # Magenta
        Comment.Single:         "#555555",  # Medium grey
        Comment.Special:        "bold #555555",  # Bold medium grey
        Operator:               "#ffffff",  # Pure white text
        Operator.Word:          "#ff00ff",  # Magenta
        Punctuation:            "#ffffff",  # Pure white text
    }
