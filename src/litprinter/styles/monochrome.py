"""
MONOCHROME Style - A minimalist black and white theme with shades of grey.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class MONOCHROME(Style):
    """
    MONOCHROME Style - A minimalist black and white theme with shades of grey.
    """
    background_color = "#ffffff"  # White background
    styles = {
        Text:                   "#000000",  # Black text
        Whitespace:             "#eeeeee",  # Light grey for whitespace
        Error:                  "#000000 bg:#ffdddd",  # Black on light red background
        Other:                  "#000000",  # Black text
        Name:                   "#000000",  # Black text
        Name.Attribute:         "#555555",  # Dark grey
        Name.Builtin:           "#000000 bold",  # Bold black
        Name.Builtin.Pseudo:    "#000000 bold",  # Bold black
        Name.Class:             "#000000 bold",  # Bold black
        Name.Constant:          "#000000 bold",  # Bold black
        Name.Decorator:         "#555555",  # Dark grey
        Name.Entity:            "#555555",  # Dark grey
        Name.Exception:         "#000000 bold",  # Bold black
        Name.Function:          "#000000 bold",  # Bold black
        Name.Property:          "#000000",  # Black text
        Name.Label:             "#000000",  # Black text
        Name.Namespace:         "#000000 bold",  # Bold black
        Name.Other:             "#000000",  # Black text
        Name.Tag:               "#000000 bold",  # Bold black
        Name.Variable:          "#000000",  # Black text
        Name.Variable.Class:    "#000000",  # Black text
        Name.Variable.Global:   "#000000",  # Black text
        Name.Variable.Instance: "#000000",  # Black text
        String:                 "#000000 italic",  # Italic black
        String.Backtick:        "#000000 italic",  # Italic black
        String.Char:            "#000000 italic",  # Italic black
        String.Doc:             "#777777",  # Medium grey for docstrings
        String.Double:          "#000000 italic",  # Italic black
        String.Escape:          "#555555",  # Dark grey for escape sequences
        String.Heredoc:         "#000000 italic",  # Italic black
        String.Interpol:        "#555555",  # Dark grey for interpolated parts
        String.Other:           "#000000 italic",  # Italic black
        String.Regex:           "#000000 italic",  # Italic black
        String.Single:          "#000000 italic",  # Italic black
        String.Symbol:          "#000000 italic",  # Italic black
        Number:                 "#000000",  # Black text
        Number.Float:           "#000000",  # Black text
        Number.Hex:             "#000000",  # Black text
        Number.Integer:         "#000000",  # Black text
        Number.Integer.Long:    "#000000",  # Black text
        Number.Oct:             "#000000",  # Black text
        Keyword:                "#000000 bold",  # Bold black
        Keyword.Constant:       "#000000 bold",  # Bold black
        Keyword.Declaration:    "#000000 bold",  # Bold black
        Keyword.Namespace:      "#000000 bold",  # Bold black
        Keyword.Pseudo:         "#000000 bold",  # Bold black
        Keyword.Reserved:       "#000000 bold",  # Bold black
        Keyword.Type:           "#000000 bold",  # Bold black
        Generic:                "#000000",  # Black text
        Generic.Deleted:        "#000000 bg:#ffdddd",  # Black on light red background
        Generic.Emph:           "#000000 italic",  # Italic black
        Generic.Error:          "#000000 bg:#ffdddd",  # Black on light red background
        Generic.Heading:        "#000000 bold",  # Bold black
        Generic.Inserted:       "#000000 bg:#ddffdd",  # Black on light green background
        Generic.Output:         "#777777",  # Medium grey
        Generic.Prompt:         "#000000 bold",  # Bold black
        Generic.Strong:         "#000000 bold",  # Bold black
        Generic.Subheading:     "#000000 bold",  # Bold black
        Generic.Traceback:      "#000000 bg:#ffdddd",  # Black on light red background
        Literal:                "#000000",  # Black text
        Literal.Date:           "#000000 italic",  # Italic black
        Comment:                "#777777",  # Medium grey
        Comment.Multiline:      "#777777",  # Medium grey
        Comment.Preproc:        "#555555",  # Dark grey
        Comment.Single:         "#777777",  # Medium grey
        Comment.Special:        "#777777 bold",  # Bold medium grey
        Operator:               "#000000",  # Black text
        Operator.Word:          "#000000 bold",  # Bold black
        Punctuation:            "#000000",  # Black text
    }
