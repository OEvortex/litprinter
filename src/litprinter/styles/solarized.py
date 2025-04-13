"""
SOLARIZED Style - Based on the popular Solarized color scheme with its distinctive palette.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class SOLARIZED(Style):
    """
    SOLARIZED Style - Based on the popular Solarized color scheme with its distinctive palette.
    This is the dark variant of Solarized.
    """
    background_color = "#002b36"  # Base03 (dark background)
    styles = {
        Text:                   "#839496",  # Base0 (primary content)
        Whitespace:             "#073642",  # Base02 (subtle highlights)
        Error:                  "#dc322f",  # Red
        Other:                  "#839496",  # Base0
        Name:                   "#839496",  # Base0
        Name.Attribute:         "#268bd2",  # Blue
        Name.Builtin:           "#859900",  # Green
        Name.Builtin.Pseudo:    "#859900",  # Green
        Name.Class:             "#268bd2",  # Blue
        Name.Constant:          "#6c71c4",  # Violet
        Name.Decorator:         "#cb4b16",  # Orange
        Name.Entity:            "#cb4b16",  # Orange
        Name.Exception:         "#dc322f",  # Red
        Name.Function:          "#268bd2",  # Blue
        Name.Property:          "#839496",  # Base0
        Name.Label:             "#839496",  # Base0
        Name.Namespace:         "#b58900",  # Yellow
        Name.Other:             "#839496",  # Base0
        Name.Tag:               "#268bd2",  # Blue
        Name.Variable:          "#cb4b16",  # Orange
        Name.Variable.Class:    "#268bd2",  # Blue
        Name.Variable.Global:   "#cb4b16",  # Orange
        Name.Variable.Instance: "#cb4b16",  # Orange
        String:                 "#2aa198",  # Cyan
        String.Backtick:        "#2aa198",  # Cyan
        String.Char:            "#2aa198",  # Cyan
        String.Doc:             "#586e75",  # Base01 (comments)
        String.Double:          "#2aa198",  # Cyan
        String.Escape:          "#cb4b16",  # Orange
        String.Heredoc:         "#2aa198",  # Cyan
        String.Interpol:        "#cb4b16",  # Orange
        String.Other:           "#2aa198",  # Cyan
        String.Regex:           "#2aa198",  # Cyan
        String.Single:          "#2aa198",  # Cyan
        String.Symbol:          "#2aa198",  # Cyan
        Number:                 "#d33682",  # Magenta
        Number.Float:           "#d33682",  # Magenta
        Number.Hex:             "#d33682",  # Magenta
        Number.Integer:         "#d33682",  # Magenta
        Number.Integer.Long:    "#d33682",  # Magenta
        Number.Oct:             "#d33682",  # Magenta
        Keyword:                "#859900",  # Green
        Keyword.Constant:       "#6c71c4",  # Violet
        Keyword.Declaration:    "#268bd2",  # Blue
        Keyword.Namespace:      "#859900",  # Green
        Keyword.Pseudo:         "#859900",  # Green
        Keyword.Reserved:       "#859900",  # Green
        Keyword.Type:           "#b58900",  # Yellow
        Generic:                "#839496",  # Base0
        Generic.Deleted:        "#dc322f bg:#073642",  # Red on Base02
        Generic.Emph:           "italic #839496",  # Italic Base0
        Generic.Error:          "#dc322f",  # Red
        Generic.Heading:        "bold #839496",  # Bold Base0
        Generic.Inserted:       "#859900 bg:#073642",  # Green on Base02
        Generic.Output:         "#586e75",  # Base01
        Generic.Prompt:         "#268bd2",  # Blue
        Generic.Strong:         "bold #839496",  # Bold Base0
        Generic.Subheading:     "bold #268bd2",  # Bold Blue
        Generic.Traceback:      "#dc322f",  # Red
        Literal:                "#839496",  # Base0
        Literal.Date:           "#2aa198",  # Cyan
        Comment:                "#586e75",  # Base01
        Comment.Multiline:      "#586e75",  # Base01
        Comment.Preproc:        "#cb4b16",  # Orange
        Comment.Single:         "#586e75",  # Base01
        Comment.Special:        "bold #586e75",  # Bold Base01
        Operator:               "#839496",  # Base0
        Operator.Word:          "#859900",  # Green
        Punctuation:            "#839496",  # Base0
    }
