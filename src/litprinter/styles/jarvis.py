"""
JARVIS Style - A Tron-inspired theme with black background and vibrant cyan/green/magenta highlights.
"""
from .base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class JARVIS(Style):
    """
    JARVIS Style - A Tron-inspired theme with black background and vibrant cyan/green/magenta highlights.
    """
    background_color = "#000000"
    styles = {
        Text:                   "#ffffff",
        Whitespace:             "#222222", # Slightly visible whitespace
        Error:                  "#ff0000", # Bright red for errors
        Other:                  "#ffffff", # Default text
        Name:                   "#00ffff", # Cyan for names
        Name.Attribute:         "#ffffff",
        Name.Builtin:           "#00ff00",
        Name.Builtin.Pseudo:    "#00ff00",
        Name.Class:             "#00ff00",
        Name.Constant:          "#ffff00",
        Name.Decorator:         "#ff8800",
        Name.Entity:            "#ff8800",
        Name.Exception:         "#ff8800",
        Name.Function:          "#00ff00",
        Name.Property:          "#00ff00",
        Name.Label:             "#ffffff",
        Name.Namespace:         "#ffff00",
        Name.Other:             "#ffffff",
        Name.Tag:               "#00ff88",
        Name.Variable:          "#ff8800",
        Name.Variable.Class:    "#00ff00",
        Name.Variable.Global:   "#00ff00",
        Name.Variable.Instance: "#00ff00",
        String:                 "#88ff00",
        String.Backtick:        "#88ff00",
        String.Char:            "#88ff00",
        String.Char:            "#88ff00",
        String.Doc:             "#88ff00", # Docstrings same as strings
        String.Double:          "#88ff00",
        String.Escape:          "#ff8800", # Orange for escape sequences
        String.Heredoc:         "#88ff00",
        String.Interpol:        "#ff8800", # Orange for interpolated parts
        String.Other:           "#88ff00",
        String.Regex:           "#88ff00", # Regexes same as strings
        String.Single:          "#88ff00",
        String.Symbol:          "#88ff00", # Symbols same as strings
        Number:                 "#0088ff",
        Number.Float:           "#0088ff",
        Number.Hex:             "#0088ff",
        Number.Integer:         "#0088ff",
        Number.Integer.Long:    "#0088ff",
        Number.Oct:             "#0088ff",
        Keyword:                "#ff00ff",
        Keyword.Constant:       "#ff00ff", # Keyword constants same as keywords
        Keyword.Declaration:    "#ff00ff", # Declarations same as keywords
        Keyword.Namespace:      "#ff8800", # Orange for namespace keywords (e.g., import)
        Keyword.Pseudo:         "#ff8800", # Orange for pseudo keywords
        Keyword.Reserved:       "#ff00ff", # Reserved words same as keywords
        Keyword.Type:           "#ff00ff", # Type keywords same as keywords
        Generic:                "#ffffff", # Generic text
        Generic.Deleted:        "#ff0000 bg:#440000", # Red for deleted lines (diff)
        Generic.Emph:           "italic #ffffff", # Italic white for emphasis
        Generic.Error:          "#ff0000", # Red for generic errors
        Generic.Heading:        "bold #ffffff", # Bold white for headings
        Generic.Inserted:       "#00ff00 bg:#004400", # Green for inserted lines (diff)
        Generic.Output:         "#444444", # Dark grey for program output
        Generic.Prompt:         "#00ffff", # Cyan for prompts
        Generic.Strong:         "bold #ffffff", # Bold white for strong emphasis
        Generic.Subheading:     "bold #00ff88", # Bold teal for subheadings
        Generic.Traceback:      "#ff0000", # Red for tracebacks
        Literal:                "#ffffff", # White for literals
        Literal.Date:           "#88ff00", # Lime green for dates
        Comment:                "#888888", # Grey for comments
        Comment.Multiline:      "#888888",
        Comment.Preproc:        "#ff8800", # Orange for preprocessor comments
        Comment.Single:         "#888888",
        Comment.Special:        "bold #888888", # Bold grey for special comments (e.g., TODO)
        Operator:               "#ffffff", # White for operators
        Operator.Word:          "#ff00ff", # Magenta for word operators (e.g., 'in', 'and')
        Punctuation:            "#ffffff", # White for punctuation
    }
