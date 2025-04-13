"""
MONOKAI Style - A classic dark theme known for its vibrant green, pink, and blue colors.
"""
from litprinter.styles.base import (
    Style, Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


class MONOKAI(Style):
    """
    MONOKAI Style - A classic dark theme known for its vibrant green, pink, and blue colors.
    """
    background_color = "#272822"  # Dark background
    styles = {
        Text:                   "#f8f8f2",  # Off-white text
        Whitespace:             "#3b3a32",  # Slightly lighter grey for subtle whitespace
        Error:                  "#f92672",  # Bright pink for errors
        Other:                  "#f8f8f2",  # Default text
        Name:                   "#f8f8f2",  # Off-white for general names
        Name.Attribute:         "#a6e22e",  # Bright green for attributes
        Name.Builtin:           "#66d9ef",  # Bright cyan for builtins
        Name.Builtin.Pseudo:    "#66d9ef",  # Bright cyan for pseudo builtins
        Name.Class:             "#a6e22e",  # Bright green for class names
        Name.Constant:          "#ae81ff",  # Purple for constants
        Name.Decorator:         "#a6e22e",  # Bright green for decorators
        Name.Entity:            "#a6e22e",  # Bright green for HTML/XML entities
        Name.Exception:         "#f92672",  # Bright pink for exceptions
        Name.Function:          "#a6e22e",  # Bright green for functions
        Name.Property:          "#f8f8f2",  # Off-white for properties
        Name.Label:             "#f8f8f2",  # Off-white for labels
        Name.Namespace:         "#f8f8f2",  # Off-white for namespaces
        Name.Other:             "#f8f8f2",  # Off-white for other names
        Name.Tag:               "#f92672",  # Bright pink for HTML/XML tags
        Name.Variable:          "#f8f8f2",  # Off-white for variables
        Name.Variable.Class:    "#a6e22e",  # Bright green for class variables ('cls', 'self')
        Name.Variable.Global:   "#f8f8f2",  # Off-white for global variables
        Name.Variable.Instance: "#fd971f",  # Orange for instance variables
        String:                 "#e6db74",  # Yellow for strings
        String.Backtick:        "#e6db74",  # Yellow for backtick strings
        String.Char:            "#e6db74",  # Yellow for character literals
        String.Doc:             "#75715e",  # Grey for docstrings (like comments)
        String.Double:          "#e6db74",  # Yellow for double-quoted strings
        String.Escape:          "#ae81ff",  # Purple for escape sequences
        String.Heredoc:         "#e6db74",  # Yellow for heredoc strings
        String.Interpol:        "#ae81ff",  # Purple for interpolated parts (f-strings)
        String.Other:           "#e6db74",  # Yellow for other string types
        String.Regex:           "#e6db74",  # Yellow for regexes
        String.Single:          "#e6db74",  # Yellow for single-quoted strings
        String.Symbol:          "#e6db74",  # Yellow for symbols
        Number:                 "#ae81ff",  # Purple for numbers
        Number.Float:           "#ae81ff",  # Purple for floats
        Number.Hex:             "#ae81ff",  # Purple for hex numbers
        Number.Integer:         "#ae81ff",  # Purple for integers
        Number.Integer.Long:    "#ae81ff",  # Purple for long integers
        Number.Oct:             "#ae81ff",  # Purple for octal numbers
        Keyword:                "#f92672",  # Bright pink for keywords
        Keyword.Constant:       "#66d9ef",  # Bright cyan for keyword constants (True, False, None)
        Keyword.Declaration:    "#66d9ef",  # Bright cyan for declaration keywords (def, class)
        Keyword.Namespace:      "#f92672",  # Bright pink for import/from
        Keyword.Pseudo:         "#ae81ff",  # Purple for pseudo keywords
        Keyword.Reserved:       "#f92672",  # Bright pink for reserved words
        Keyword.Type:           "#66d9ef",  # Bright cyan for type keywords (int, str)
        Generic:                "#f8f8f2",  # Generic text
        Generic.Deleted:        "#f92672 bg:#3b3a32",  # Bright pink for deleted lines (diff)
        Generic.Emph:           "italic #f8f8f2",  # Italic off-white for emphasis
        Generic.Error:          "#f92672",  # Bright pink for generic errors
        Generic.Heading:        "bold #f8f8f2",  # Bold off-white for headings
        Generic.Inserted:       "#a6e22e bg:#3b3a32",  # Bright green for inserted lines (diff)
        Generic.Output:         "#49483e",  # Darker grey for program output
        Generic.Prompt:         "#a6e22e",  # Bright green for prompts
        Generic.Strong:         "bold #f8f8f2",  # Bold off-white for strong emphasis
        Generic.Subheading:     "bold #a6e22e",  # Bold bright green for subheadings
        Generic.Traceback:      "#f92672",  # Bright pink for tracebacks
        Literal:                "#ae81ff",  # Purple for literals (e.g., numbers within code)
        Literal.Date:           "#e6db74",  # Yellow for dates
        Comment:                "#75715e",  # Grey for comments
        Comment.Multiline:      "#75715e",  # Grey for multiline comments
        Comment.Preproc:        "#f92672",  # Bright pink for preprocessor comments
        Comment.Single:         "#75715e",  # Grey for single-line comments
        Comment.Special:        "bold italic #75715e",  # Bold italic grey for special comments
        Operator:               "#f92672",  # Bright pink for operators
        Operator.Word:          "#f92672",  # Bright pink for word operators (and, or, not)
        Punctuation:            "#f8f8f2",  # Off-white for punctuation
    }
