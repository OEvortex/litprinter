"""
NORD Style - Based on the Nord color scheme with its arctic, bluish colors.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class NORD(Style):
    """
    NORD Style - Based on the Nord color scheme with its arctic, bluish colors.
    """
    background_color = "#2e3440"  # Nord0 (polar night)
    styles = {
        Text:                   "#d8dee9",  # Nord4 (snow storm)
        Whitespace:             "#3b4252",  # Nord1 (darker polar night)
        Error:                  "#bf616a",  # Nord11 (aurora red)
        Other:                  "#d8dee9",  # Nord4
        Name:                   "#d8dee9",  # Nord4
        Name.Attribute:         "#8fbcbb",  # Nord7 (frost)
        Name.Builtin:           "#81a1c1",  # Nord9 (frost)
        Name.Builtin.Pseudo:    "#81a1c1",  # Nord9
        Name.Class:             "#8fbcbb",  # Nord7
        Name.Constant:          "#5e81ac",  # Nord10 (frost)
        Name.Decorator:         "#88c0d0",  # Nord8 (frost)
        Name.Entity:            "#88c0d0",  # Nord8
        Name.Exception:         "#bf616a",  # Nord11
        Name.Function:          "#88c0d0",  # Nord8
        Name.Property:          "#d8dee9",  # Nord4
        Name.Label:             "#d8dee9",  # Nord4
        Name.Namespace:         "#81a1c1",  # Nord9
        Name.Other:             "#d8dee9",  # Nord4
        Name.Tag:               "#81a1c1",  # Nord9
        Name.Variable:          "#d8dee9",  # Nord4
        Name.Variable.Class:    "#8fbcbb",  # Nord7
        Name.Variable.Global:   "#81a1c1",  # Nord9
        Name.Variable.Instance: "#d8dee9",  # Nord4
        String:                 "#a3be8c",  # Nord14 (aurora green)
        String.Backtick:        "#a3be8c",  # Nord14
        String.Char:            "#a3be8c",  # Nord14
        String.Doc:             "#616e88",  # Blend of Nord2 and Nord3 (for comments)
        String.Double:          "#a3be8c",  # Nord14
        String.Escape:          "#ebcb8b",  # Nord13 (aurora yellow)
        String.Heredoc:         "#a3be8c",  # Nord14
        String.Interpol:        "#ebcb8b",  # Nord13
        String.Other:           "#a3be8c",  # Nord14
        String.Regex:           "#ebcb8b",  # Nord13 (aurora yellow)
        String.Single:          "#a3be8c",  # Nord14
        String.Symbol:          "#a3be8c",  # Nord14
        Number:                 "#b48ead",  # Nord15 (aurora purple)
        Number.Float:           "#b48ead",  # Nord15
        Number.Hex:             "#b48ead",  # Nord15
        Number.Integer:         "#b48ead",  # Nord15
        Number.Integer.Long:    "#b48ead",  # Nord15
        Number.Oct:             "#b48ead",  # Nord15
        Keyword:                "#81a1c1",  # Nord9
        Keyword.Constant:       "#5e81ac",  # Nord10
        Keyword.Declaration:    "#81a1c1",  # Nord9
        Keyword.Namespace:      "#81a1c1",  # Nord9
        Keyword.Pseudo:         "#81a1c1",  # Nord9
        Keyword.Reserved:       "#81a1c1",  # Nord9
        Keyword.Type:           "#8fbcbb",  # Nord7
        Generic:                "#d8dee9",  # Nord4
        Generic.Deleted:        "#bf616a bg:#3b4252",  # Nord11 on Nord1
        Generic.Emph:           "italic #d8dee9",  # Italic Nord4
        Generic.Error:          "#bf616a",  # Nord11
        Generic.Heading:        "bold #d8dee9",  # Bold Nord4
        Generic.Inserted:       "#a3be8c bg:#3b4252",  # Nord14 on Nord1
        Generic.Output:         "#4c566a",  # Nord3
        Generic.Prompt:         "#88c0d0",  # Nord8
        Generic.Strong:         "bold #d8dee9",  # Bold Nord4
        Generic.Subheading:     "bold #88c0d0",  # Bold Nord8
        Generic.Traceback:      "#bf616a",  # Nord11
        Literal:                "#d8dee9",  # Nord4
        Literal.Date:           "#a3be8c",  # Nord14
        Comment:                "#616e88",  # Blend of Nord2 and Nord3
        Comment.Multiline:      "#616e88",  # Blend of Nord2 and Nord3
        Comment.Preproc:        "#5e81ac",  # Nord10
        Comment.Single:         "#616e88",  # Blend of Nord2 and Nord3
        Comment.Special:        "bold #616e88",  # Bold blend of Nord2 and Nord3
        Operator:               "#81a1c1",  # Nord9
        Operator.Word:          "#81a1c1",  # Nord9
        Punctuation:            "#d8dee9",  # Nord4
    }
