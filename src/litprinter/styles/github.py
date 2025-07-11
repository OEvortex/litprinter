"""
GITHUB Style - Based on GitHub's light theme for a familiar look.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class GITHUB(Style):
    """
    GITHUB Style - Based on GitHub's light theme for a familiar look.
    """
    background_color = "#ffffff"  # White background
    styles = {
        Text:                   "#24292e",  # GitHub's default text color
        Whitespace:             "#e1e4e8",  # Light grey for whitespace
        Error:                  "#d73a49",  # GitHub's red
        Other:                  "#24292e",  # Default text
        Name:                   "#24292e",  # Default text
        Name.Attribute:         "#005cc5",  # GitHub's blue
        Name.Builtin:           "#6f42c1",  # GitHub's purple
        Name.Builtin.Pseudo:    "#6f42c1",  # GitHub's purple
        Name.Class:             "#6f42c1",  # GitHub's purple
        Name.Constant:          "#005cc5",  # GitHub's blue
        Name.Decorator:         "#6f42c1",  # GitHub's purple
        Name.Entity:            "#6f42c1",  # GitHub's purple
        Name.Exception:         "#d73a49",  # GitHub's red
        Name.Function:          "#6f42c1",  # GitHub's purple
        Name.Property:          "#24292e",  # Default text
        Name.Label:             "#24292e",  # Default text
        Name.Namespace:         "#6f42c1",  # GitHub's purple
        Name.Other:             "#24292e",  # Default text
        Name.Tag:               "#22863a",  # GitHub's green
        Name.Variable:          "#e36209",  # GitHub's orange
        Name.Variable.Class:    "#e36209",  # GitHub's orange
        Name.Variable.Global:   "#e36209",  # GitHub's orange
        Name.Variable.Instance: "#e36209",  # GitHub's orange
        String:                 "#032f62",  # GitHub's blue for strings
        String.Backtick:        "#032f62",  # GitHub's blue for strings
        String.Char:            "#032f62",  # GitHub's blue for strings
        String.Doc:             "#6a737d",  # GitHub's grey for comments
        String.Double:          "#032f62",  # GitHub's blue for strings
        String.Escape:          "#005cc5",  # GitHub's blue
        String.Heredoc:         "#032f62",  # GitHub's blue for strings
        String.Interpol:        "#005cc5",  # GitHub's blue
        String.Other:           "#032f62",  # GitHub's blue for strings
        String.Regex:           "#032f62",  # GitHub's blue for strings
        String.Single:          "#032f62",  # GitHub's blue for strings
        String.Symbol:          "#032f62",  # GitHub's blue for strings
        Number:                 "#005cc5",  # GitHub's blue
        Number.Float:           "#005cc5",  # GitHub's blue
        Number.Hex:             "#005cc5",  # GitHub's blue
        Number.Integer:         "#005cc5",  # GitHub's blue
        Number.Integer.Long:    "#005cc5",  # GitHub's blue
        Number.Oct:             "#005cc5",  # GitHub's blue
        Keyword:                "#d73a49",  # GitHub's red
        Keyword.Constant:       "#005cc5",  # GitHub's blue
        Keyword.Declaration:    "#d73a49",  # GitHub's red
        Keyword.Namespace:      "#d73a49",  # GitHub's red
        Keyword.Pseudo:         "#d73a49",  # GitHub's red
        Keyword.Reserved:       "#d73a49",  # GitHub's red
        Keyword.Type:           "#d73a49",  # GitHub's red
        Generic:                "#24292e",  # Default text
        Generic.Deleted:        "#b31d28 bg:#ffeef0",  # GitHub's red on light red
        Generic.Emph:           "italic #24292e",  # Italic default text
        Generic.Error:          "#b31d28",  # GitHub's dark red
        Generic.Heading:        "bold #24292e",  # Bold default text
        Generic.Inserted:       "#22863a bg:#f0fff4",  # GitHub's green on light green
        Generic.Output:         "#6a737d",  # GitHub's grey
        Generic.Prompt:         "#005cc5",  # GitHub's blue
        Generic.Strong:         "bold #24292e",  # Bold default text
        Generic.Subheading:     "bold #005cc5",  # Bold blue
        Generic.Traceback:      "#b31d28",  # GitHub's dark red
        Literal:                "#24292e",  # Default text
        Literal.Date:           "#032f62",  # GitHub's blue for strings
        Comment:                "#6a737d",  # GitHub's grey for comments
        Comment.Multiline:      "#6a737d",  # GitHub's grey for comments
        Comment.Preproc:        "#d73a49",  # GitHub's red
        Comment.Single:         "#6a737d",  # GitHub's grey for comments
        Comment.Special:        "bold #6a737d",  # Bold grey for special comments
        Operator:               "#d73a49",  # GitHub's red
        Operator.Word:          "#d73a49",  # GitHub's red
        Punctuation:            "#24292e",  # Default text
    }
