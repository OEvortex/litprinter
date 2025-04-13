"""
SYNTHWAVE Style - A retro 80s-inspired theme with neon purples and blues.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class SYNTHWAVE(Style):
    """
    SYNTHWAVE Style - A retro 80s-inspired theme with neon purples and blues.
    """
    background_color = "#241b36" # Deep purple background
    styles = {
        Text:                   "#f4ddff", # Light purple text
        Whitespace:             "#3b2d59", # Slightly lighter background
        Error:                  "#ff4499", # Hot pink for errors
        Other:                  "#f4ddff", # Light purple text
        Name:                   "#f4ddff", # Light purple text
        Name.Attribute:         "#36f9f6", # Neon cyan
        Name.Builtin:           "#ff8b39", # Orange
        Name.Builtin.Pseudo:    "#ff8b39", # Orange
        Name.Class:             "#fede5d", # Yellow
        Name.Constant:          "#ff8b39", # Orange
        Name.Decorator:         "#ff8b39", # Orange
        Name.Entity:            "#ff8b39", # Orange
        Name.Exception:         "#ff4499", # Hot pink
        Name.Function:          "#36f9f6", # Neon cyan
        Name.Property:          "#f4ddff", # Light purple text
        Name.Label:             "#f4ddff", # Light purple text
        Name.Namespace:         "#fede5d", # Yellow
        Name.Other:             "#f4ddff", # Light purple text
        Name.Tag:               "#ff4499", # Hot pink
        Name.Variable:          "#f4ddff", # Light purple text
        Name.Variable.Class:    "#f4ddff", # Light purple text
        Name.Variable.Global:   "#f4ddff", # Light purple text
        Name.Variable.Instance: "#f4ddff", # Light purple text
        String:                 "#ff8b39", # Orange
        String.Backtick:        "#ff8b39", # Orange
        String.Char:            "#ff8b39", # Orange
        String.Doc:             "#7b6d99", # Muted purple
        String.Double:          "#ff8b39", # Orange
        String.Escape:          "#ff4499", # Hot pink
        String.Heredoc:         "#ff8b39", # Orange
        String.Interpol:        "#ff4499", # Hot pink
        String.Other:           "#ff8b39", # Orange
        String.Regex:           "#ff8b39", # Orange
        String.Single:          "#ff8b39", # Orange
        String.Symbol:          "#ff8b39", # Orange
        Number:                 "#fede5d", # Yellow
        Number.Float:           "#fede5d", # Yellow
        Number.Hex:             "#fede5d", # Yellow
        Number.Integer:         "#fede5d", # Yellow
        Number.Integer.Long:    "#fede5d", # Yellow
        Number.Oct:             "#fede5d", # Yellow
        Keyword:                "#ff4499", # Hot pink
        Keyword.Constant:       "#fede5d", # Yellow
        Keyword.Declaration:    "#ff4499", # Hot pink
        Keyword.Namespace:      "#ff4499", # Hot pink
        Keyword.Pseudo:         "#ff4499", # Hot pink
        Keyword.Reserved:       "#ff4499", # Hot pink
        Keyword.Type:           "#36f9f6", # Neon cyan
        Generic:                "#f4ddff", # Light purple text
        Generic.Deleted:        "#ff4499 bg:#3b2d59", # Hot pink on slightly lighter background
        Generic.Emph:           "italic #f4ddff", # Italic light purple
        Generic.Error:          "#ff4499", # Hot pink
        Generic.Heading:        "bold #f4ddff", # Bold light purple
        Generic.Inserted:       "#36f9f6 bg:#3b2d59", # Neon cyan on slightly lighter background
        Generic.Output:         "#7b6d99", # Muted purple
        Generic.Prompt:         "#ff4499", # Hot pink
        Generic.Strong:         "bold #f4ddff", # Bold light purple
        Generic.Subheading:     "bold #36f9f6", # Bold neon cyan
        Generic.Traceback:      "#ff4499", # Hot pink
        Literal:                "#f4ddff", # Light purple text
        Literal.Date:           "#ff8b39", # Orange
        Comment:                "#7b6d99", # Muted purple
        Comment.Multiline:      "#7b6d99", # Muted purple
        Comment.Preproc:        "#ff4499", # Hot pink
        Comment.Single:         "#7b6d99", # Muted purple
        Comment.Special:        "bold #7b6d99", # Bold muted purple
        Operator:               "#36f9f6", # Neon cyan
        Operator.Word:          "#ff4499", # Hot pink
        Punctuation:            "#f4ddff", # Light purple text
    }
