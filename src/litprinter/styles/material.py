"""
MATERIAL Style - Based on Material Design colors for a modern look.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class MATERIAL(Style):
    """
    Material Theme - Based on Material Design colors for a modern look.
    """
    background_color = "#263238"  # Material dark background
    styles = {
        Text:                   "#eeffff",  # Material light text
        Whitespace:             "#37474f",  # Material darker blue-grey
        Error:                  "#ff5370",  # Material red
        Other:                  "#eeffff",  # Default text
        Name:                   "#eeffff",  # Default text
        Name.Attribute:         "#82aaff",  # Material blue
        Name.Builtin:           "#89ddff",  # Material cyan
        Name.Builtin.Pseudo:    "#89ddff",  # Material cyan
        Name.Class:             "#ffcb6b",  # Material yellow
        Name.Constant:          "#f78c6c",  # Material orange
        Name.Decorator:         "#82aaff",  # Material blue
        Name.Entity:            "#82aaff",  # Material blue
        Name.Exception:         "#ff5370",  # Material red
        Name.Function:          "#82aaff",  # Material blue
        Name.Property:          "#eeffff",  # Default text
        Name.Label:             "#eeffff",  # Default text
        Name.Namespace:         "#ffcb6b",  # Material yellow
        Name.Other:             "#eeffff",  # Default text
        Name.Tag:               "#f07178",  # Material coral
        Name.Variable:          "#eeffff",  # Default text
        Name.Variable.Class:    "#eeffff",  # Default text
        Name.Variable.Global:   "#eeffff",  # Default text
        Name.Variable.Instance: "#eeffff",  # Default text
        String:                 "#c3e88d",  # Material green
        String.Backtick:        "#c3e88d",  # Material green
        String.Char:            "#c3e88d",  # Material green
        String.Doc:             "#546e7a",  # Material blue-grey
        String.Double:          "#c3e88d",  # Material green
        String.Escape:          "#f78c6c",  # Material orange
        String.Heredoc:         "#c3e88d",  # Material green
        String.Interpol:        "#f78c6c",  # Material orange
        String.Other:           "#c3e88d",  # Material green
        String.Regex:           "#89ddff",  # Material cyan
        String.Single:          "#c3e88d",  # Material green
        String.Symbol:          "#c3e88d",  # Material green
        Number:                 "#f78c6c",  # Material orange
        Number.Float:           "#f78c6c",  # Material orange
        Number.Hex:             "#f78c6c",  # Material orange
        Number.Integer:         "#f78c6c",  # Material orange
        Number.Integer.Long:    "#f78c6c",  # Material orange
        Number.Oct:             "#f78c6c",  # Material orange
        Keyword:                "#c792ea",  # Material purple
        Keyword.Constant:       "#89ddff",  # Material cyan
        Keyword.Declaration:    "#c792ea",  # Material purple
        Keyword.Namespace:      "#c792ea",  # Material purple
        Keyword.Pseudo:         "#c792ea",  # Material purple
        Keyword.Reserved:       "#c792ea",  # Material purple
        Keyword.Type:           "#ffcb6b",  # Material yellow
        Generic:                "#eeffff",  # Default text
        Generic.Deleted:        "#ff5370 bg:#37474f",  # Material red on darker background
        Generic.Emph:           "italic #eeffff",  # Italic default text
        Generic.Error:          "#ff5370",  # Material red
        Generic.Heading:        "bold #eeffff",  # Bold default text
        Generic.Inserted:       "#c3e88d bg:#37474f",  # Material green on darker background
        Generic.Output:         "#546e7a",  # Material blue-grey
        Generic.Prompt:         "#82aaff",  # Material blue
        Generic.Strong:         "bold #eeffff",  # Bold default text
        Generic.Subheading:     "bold #82aaff",  # Bold blue
        Generic.Traceback:      "#ff5370",  # Material red
        Literal:                "#eeffff",  # Default text
        Literal.Date:           "#c3e88d",  # Material green
        Comment:                "#546e7a",  # Material blue-grey
        Comment.Multiline:      "#546e7a",  # Material blue-grey
        Comment.Preproc:        "#89ddff",  # Material cyan
        Comment.Single:         "#546e7a",  # Material blue-grey
        Comment.Special:        "bold #546e7a",  # Bold blue-grey
        Operator:               "#89ddff",  # Material cyan
        Operator.Word:          "#c792ea",  # Material purple
        Punctuation:            "#89ddff",  # Material cyan
    }
