"""
VSCODE Style - Based on VS Code's default dark theme.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class VSCODE(Style):
    """
    VS Code Theme - Based on VS Code's default dark theme.
    """
    background_color = "#1e1e1e"  # VS Code dark theme background
    styles = {
        Text:                   "#d4d4d4",  # VS Code default text
        Whitespace:             "#3e3e42",  # Slightly lighter than background
        Error:                  "#f44747",  # VS Code error red
        Other:                  "#d4d4d4",  # Default text
        Name:                   "#d4d4d4",  # Default text
        Name.Attribute:         "#9cdcfe",  # VS Code light blue
        Name.Builtin:           "#569cd6",  # VS Code blue
        Name.Builtin.Pseudo:    "#569cd6",  # VS Code blue
        Name.Class:             "#4ec9b0",  # VS Code teal
        Name.Constant:          "#4fc1ff",  # VS Code bright blue
        Name.Decorator:         "#dcdcaa",  # VS Code yellow
        Name.Entity:            "#dcdcaa",  # VS Code yellow
        Name.Exception:         "#f44747",  # VS Code error red
        Name.Function:          "#dcdcaa",  # VS Code yellow
        Name.Property:          "#9cdcfe",  # VS Code light blue
        Name.Label:             "#9cdcfe",  # VS Code light blue
        Name.Namespace:         "#4ec9b0",  # VS Code teal
        Name.Other:             "#d4d4d4",  # Default text
        Name.Tag:               "#569cd6",  # VS Code blue
        Name.Variable:          "#9cdcfe",  # VS Code light blue
        Name.Variable.Class:    "#9cdcfe",  # VS Code light blue
        Name.Variable.Global:   "#9cdcfe",  # VS Code light blue
        Name.Variable.Instance: "#9cdcfe",  # VS Code light blue
        String:                 "#ce9178",  # VS Code orange/brown
        String.Backtick:        "#ce9178",  # VS Code orange/brown
        String.Char:            "#ce9178",  # VS Code orange/brown
        String.Doc:             "#608b4e",  # VS Code green
        String.Double:          "#ce9178",  # VS Code orange/brown
        String.Escape:          "#d7ba7d",  # VS Code light orange
        String.Heredoc:         "#ce9178",  # VS Code orange/brown
        String.Interpol:        "#d7ba7d",  # VS Code light orange
        String.Other:           "#ce9178",  # VS Code orange/brown
        String.Regex:           "#d16969",  # VS Code red/orange
        String.Single:          "#ce9178",  # VS Code orange/brown
        String.Symbol:          "#ce9178",  # VS Code orange/brown
        Number:                 "#b5cea8",  # VS Code light green
        Number.Float:           "#b5cea8",  # VS Code light green
        Number.Hex:             "#b5cea8",  # VS Code light green
        Number.Integer:         "#b5cea8",  # VS Code light green
        Number.Integer.Long:    "#b5cea8",  # VS Code light green
        Number.Oct:             "#b5cea8",  # VS Code light green
        Keyword:                "#c586c0",  # VS Code purple
        Keyword.Constant:       "#569cd6",  # VS Code blue
        Keyword.Declaration:    "#569cd6",  # VS Code blue
        Keyword.Namespace:      "#c586c0",  # VS Code purple
        Keyword.Pseudo:         "#c586c0",  # VS Code purple
        Keyword.Reserved:       "#c586c0",  # VS Code purple
        Keyword.Type:           "#569cd6",  # VS Code blue
        Generic:                "#d4d4d4",  # Default text
        Generic.Deleted:        "#f44747 bg:#3e3e42",  # VS Code error red on darker background
        Generic.Emph:           "italic #d4d4d4",  # Italic default text
        Generic.Error:          "#f44747",  # VS Code error red
        Generic.Heading:        "bold #d4d4d4",  # Bold default text
        Generic.Inserted:       "#b5cea8 bg:#3e3e42",  # VS Code light green on darker background
        Generic.Output:         "#808080",  # VS Code grey
        Generic.Prompt:         "#569cd6",  # VS Code blue
        Generic.Strong:         "bold #d4d4d4",  # Bold default text
        Generic.Subheading:     "bold #569cd6",  # Bold blue
        Generic.Traceback:      "#f44747",  # VS Code error red
        Literal:                "#d4d4d4",  # Default text
        Literal.Date:           "#ce9178",  # VS Code orange/brown
        Comment:                "#608b4e",  # VS Code green
        Comment.Multiline:      "#608b4e",  # VS Code green
        Comment.Preproc:        "#c586c0",  # VS Code purple
        Comment.Single:         "#608b4e",  # VS Code green
        Comment.Special:        "bold #608b4e",  # Bold green
        Operator:               "#d4d4d4",  # Default text
        Operator.Word:          "#c586c0",  # VS Code purple
        Punctuation:            "#d4d4d4",  # Default text
    }
