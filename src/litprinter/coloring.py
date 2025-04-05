"""
>>> from litprinter.coloring import JARVIS
>>>
>>> print(JARVIS.styles)
{<Token.Text: 0>: '#ffffff', <Token.Whitespace: 1>: '#222222', <Token.Error: 2>: '#ff0000', ...}
>>> from litprinter.coloring import create_custom_style
>>> colors = {<Token.Text>: "#ff00ff"}
>>> custom_style = create_custom_style("MyCustomStyle", colors)
>>> print(custom_style.styles)
{<Token.Text: 0>: '#ff00ff'}

This module defines color styles for the output of the litprint and lit functions.
It includes several predefined color schemes (JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI)
and the ability to create custom styles using the create_custom_style function.
"""
from pygments.style import Style
from pygments.token import (
    Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation)

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

# Rich-inspired vibrant color scheme
class RICH(Style):
    """
    RICH Style - Inspired by the Rich library's default theme, offering good contrast and readability.
    """
    background_color = "#000000"
    styles = {
        Text:                   "#f8f8f2", # Off-white (like Dracula)
        Whitespace:             "#3d3d3d", # Dark grey, slightly visible
        Error:                  "#ff5555",
        Other:                  "#f8f8f2",
        Name:                   "#8be9fd",
        Name.Attribute:         "#50fa7b",
        Name.Builtin:           "#ff79c6",
        Name.Builtin.Pseudo:    "#ff79c6",
        Name.Class:             "#8be9fd",
        Name.Constant:          "#bd93f9",
        Name.Decorator:         "#f1fa8c",
        Name.Entity:            "#f1fa8c",
        Name.Exception:         "#ff5555",
        Name.Function:          "#50fa7b",
        Name.Property:          "#50fa7b",
        Name.Label:             "#f8f8f2",
        Name.Namespace:         "#f1fa8c",
        Name.Other:             "#f8f8f2",
        Name.Tag:               "#ff79c6",
        Name.Variable:          "#f8f8f2",
        Name.Variable.Class:    "#8be9fd",
        Name.Variable.Global:   "#bd93f9",
        Name.Variable.Instance: "#f8f8f2",
        String:                 "#f1fa8c",
        String.Backtick:        "#f1fa8c",
        String.Char:            "#f1fa8c",
        String.Char:            "#f1fa8c",
        String.Doc:             "#f1fa8c", # Docstrings same as strings
        String.Double:          "#f1fa8c",
        String.Escape:          "#ff79c6", # Pink for escape sequences
        String.Heredoc:         "#f1fa8c",
        String.Interpol:        "#ff79c6", # Pink for interpolated parts
        String.Other:           "#f1fa8c",
        String.Regex:           "#f1fa8c", # Regexes same as strings
        String.Single:          "#f1fa8c",
        String.Symbol:          "#f1fa8c", # Symbols same as strings
        Number:                 "#bd93f9",
        Number.Float:           "#bd93f9",
        Number.Hex:             "#bd93f9",
        Number.Integer:         "#bd93f9",
        Number.Integer.Long:    "#bd93f9",
        Number.Oct:             "#bd93f9",
        Keyword:                "#ff79c6",
        Keyword.Constant:       "#ff79c6",
        Keyword.Declaration:    "#ff79c6",
        Keyword.Namespace:      "#ff79c6",
        Keyword.Pseudo:         "#ff79c6",
        Keyword.Reserved:       "#ff79c6",
        Keyword.Type:           "#8be9fd", # Cyan for type keywords
        Generic:                "#f8f8f2", # Generic text
        Generic.Deleted:        "#ff5555 bg:#441111", # Soft red for deleted lines
        Generic.Emph:           "italic #f8f8f2", # Italic off-white for emphasis
        Generic.Error:          "#ff5555", # Soft red for generic errors
        Generic.Heading:        "bold #f8f8f2", # Bold off-white for headings
        Generic.Inserted:       "#50fa7b bg:#114411", # Green for inserted lines
        Generic.Output:         "#44475a", # Dracula-like grey for output
        Generic.Prompt:         "#ff79c6", # Pink for prompts
        Generic.Strong:         "bold #f8f8f2", # Bold off-white for strong emphasis
        Generic.Subheading:     "bold #8be9fd", # Bold cyan for subheadings
        Generic.Traceback:      "#ff5555", # Soft red for tracebacks
        Literal:                "#f8f8f2", # Off-white for literals
        Literal.Date:           "#f1fa8c", # Yellow for dates
        Comment:                "#6272a4", # Dracula-like purple-grey for comments
        Comment.Multiline:      "#6272a4",
        Comment.Preproc:        "#ff79c6", # Pink for preprocessor comments
        Comment.Single:         "#6272a4",
        Comment.Special:        "bold #6272a4", # Bold purple-grey for special comments
        Operator:               "#ff79c6", # Pink for operators
        Operator.Word:          "#ff79c6", # Pink for word operators
        Punctuation:            "#f8f8f2", # Off-white for punctuation
    }

# Modern dark theme with high contrast
class MODERN(Style):
    """
    MODERN Style - A high-contrast dark theme with blues, purples, and greens.
    """
    background_color = "#1a1a1a" # Very dark grey background
    styles = {
        Text:                   "#e0e0e0", # Light grey text
        Whitespace:             "#333333", # Dark grey, slightly visible
        Error:                  "#ff3333",
        Other:                  "#e0e0e0",
        Name:                   "#61afef",
        Name.Attribute:         "#e0e0e0",
        Name.Builtin:           "#c678dd",
        Name.Builtin.Pseudo:    "#c678dd",
        Name.Class:             "#e5c07b",
        Name.Constant:          "#d19a66",
        Name.Decorator:         "#61afef",
        Name.Entity:            "#61afef",
        Name.Exception:         "#e06c75",
        Name.Function:          "#61afef",
        Name.Property:          "#61afef",
        Name.Label:             "#e0e0e0",
        Name.Namespace:         "#e5c07b",
        Name.Other:             "#e0e0e0",
        Name.Tag:               "#e06c75",
        Name.Variable:          "#e06c75",
        Name.Variable.Class:    "#e5c07b",
        Name.Variable.Global:   "#e06c75",
        Name.Variable.Instance: "#e06c75",
        String:                 "#98c379",
        String.Backtick:        "#98c379",
        String.Char:            "#98c379",
        String.Char:            "#98c379",
        String.Doc:             "#98c379", # Docstrings same as strings
        String.Double:          "#98c379",
        String.Escape:          "#56b6c2", # Teal for escape sequences
        String.Heredoc:         "#98c379",
        String.Interpol:        "#56b6c2", # Teal for interpolated parts
        String.Other:           "#98c379",
        String.Regex:           "#98c379", # Regexes same as strings
        String.Single:          "#98c379",
        String.Symbol:          "#98c379", # Symbols same as strings
        Number:                 "#d19a66",
        Number.Float:           "#d19a66",
        Number.Hex:             "#d19a66",
        Number.Integer:         "#d19a66",
        Number.Integer.Long:    "#d19a66",
        Number.Oct:             "#d19a66",
        Keyword:                "#c678dd",
        Keyword.Constant:       "#c678dd",
        Keyword.Declaration:    "#c678dd",
        Keyword.Namespace:      "#c678dd",
        Keyword.Pseudo:         "#c678dd",
        Keyword.Reserved:       "#c678dd",
        Keyword.Type:           "#e5c07b", # Yellow/gold for type keywords
        Generic:                "#e0e0e0", # Generic text
        Generic.Deleted:        "#e06c75 bg:#3a1b1d", # Soft red for deleted lines
        Generic.Emph:           "italic #e0e0e0", # Italic light grey for emphasis
        Generic.Error:          "#e06c75", # Soft red for generic errors
        Generic.Heading:        "bold #e0e0e0", # Bold light grey for headings
        Generic.Inserted:       "#98c379 bg:#203a1c", # Green for inserted lines
        Generic.Output:         "#5c6370", # Grey for program output (like One Dark comment)
        Generic.Prompt:         "#c678dd", # Purple for prompts
        Generic.Strong:         "bold #e0e0e0", # Bold light grey for strong emphasis
        Generic.Subheading:     "bold #61afef", # Bold blue for subheadings
        Generic.Traceback:      "#e06c75", # Soft red for tracebacks
        Literal:                "#e0e0e0", # Light grey for literals
        Literal.Date:           "#98c379", # Green for dates
        Comment:                "#5c6370", # Grey for comments (like One Dark)
        Comment.Multiline:      "#5c6370",
        Comment.Preproc:        "#c678dd", # Purple for preprocessor comments
        Comment.Single:         "#5c6370",
        Comment.Special:        "bold #5c6370", # Bold grey for special comments
        Operator:               "#56b6c2", # Teal for operators
        Operator.Word:          "#c678dd", # Purple for word operators
        Punctuation:            "#e0e0e0", # Light grey for punctuation
    }

# Neon theme with bright, vibrant colors
class NEON(Style):
    """
    NEON Style - Extremely bright, high-contrast colors on a black background. Use with caution!
    """
    background_color = "#000000"
    styles = {
        Text:                   "#ffffff",
        Whitespace:             "#333333", # Dark grey, slightly visible
        Error:                  "#ff0055",
        Other:                  "#ffffff",
        Name:                   "#00ffff",
        Name.Attribute:         "#00ffaa",
        Name.Builtin:           "#ff00ff",
        Name.Builtin.Pseudo:    "#ff00ff",
        Name.Class:             "#00ffff",
        Name.Constant:          "#ffff00",
        Name.Decorator:         "#ff00aa",
        Name.Entity:            "#ff00aa",
        Name.Exception:         "#ff0055",
        Name.Function:          "#00ffaa",
        Name.Property:          "#00ffaa",
        Name.Label:             "#ffffff",
        Name.Namespace:         "#ffff00",
        Name.Other:             "#ffffff",
        Name.Tag:               "#ff00ff",
        Name.Variable:          "#ff00aa",
        Name.Variable.Class:    "#00ffff",
        Name.Variable.Global:   "#ff00aa",
        Name.Variable.Instance: "#ff00aa",
        String:                 "#aaff00",
        String.Backtick:        "#aaff00",
        String.Char:            "#aaff00",
        String.Char:            "#aaff00",
        String.Doc:             "#aaff00", # Docstrings same as strings
        String.Double:          "#aaff00",
        String.Escape:          "#ff00aa", # Bright pink for escape sequences
        String.Heredoc:         "#aaff00",
        String.Interpol:        "#ff00aa", # Bright pink for interpolated parts
        String.Other:           "#aaff00",
        String.Regex:           "#aaff00", # Regexes same as strings
        String.Single:          "#aaff00",
        String.Symbol:          "#aaff00", # Symbols same as strings
        Number:                 "#00ffff",
        Number.Float:           "#00ffff",
        Number.Hex:             "#00ffff",
        Number.Integer:         "#00ffff",
        Number.Integer.Long:    "#00ffff",
        Number.Oct:             "#00ffff",
        Keyword:                "#ff00ff",
        Keyword.Constant:       "#ff00ff",
        Keyword.Declaration:    "#ff00ff",
        Keyword.Namespace:      "#ff00ff",
        Keyword.Pseudo:         "#ff00ff",
        Keyword.Reserved:       "#ff00ff",
        Keyword.Type:           "#00ffff", # Bright cyan for type keywords
        Generic:                "#ffffff", # Generic text
        Generic.Deleted:        "#ff0055 bg:#550011", # Bright pink/red for deleted lines
        Generic.Emph:           "italic #ffffff", # Italic white for emphasis
        Generic.Error:          "#ff0055", # Bright pink/red for generic errors
        Generic.Heading:        "bold #ffffff", # Bold white for headings
        Generic.Inserted:       "#aaff00 bg:#335500", # Bright lime green for inserted lines
        Generic.Output:         "#444444", # Dark grey for program output
        Generic.Prompt:         "#ff00ff", # Bright magenta for prompts
        Generic.Strong:         "bold #ffffff", # Bold white for strong emphasis
        Generic.Subheading:     "bold #00ffff", # Bold bright cyan for subheadings
        Generic.Traceback:      "#ff0055", # Bright pink/red for tracebacks
        Literal:                "#ffffff", # White for literals
        Literal.Date:           "#aaff00", # Bright lime green for dates
        Comment:                "#aaaaaa", # Light grey for comments
        Comment.Multiline:      "#aaaaaa",
        Comment.Preproc:        "#ff00ff", # Bright magenta for preprocessor comments
        Comment.Single:         "#aaaaaa",
        Comment.Special:        "bold #aaaaaa", # Bold light grey for special comments
        Operator:               "#ff00ff", # Bright magenta for operators
        Operator.Word:          "#ff00ff", # Bright magenta for word operators
        Punctuation:            "#ffffff", # White for punctuation
    }

# Cyberpunk theme with neon blue and pink
class CYBERPUNK(Style):
    """
    CYBERPUNK Style - Dark blue/purple background with neon pink, blue, and green highlights.
    """
    background_color = "#0a0a16" # Very dark desaturated blue
    styles = {
        Text:                   "#eeeeff", # Very light blue/lavender text
        Whitespace:             "#333344", # Dark desaturated blue/grey
        Error:                  "#ff2266",
        Other:                  "#eeeeff",
        Name:                   "#00ccff",
        Name.Attribute:         "#eeeeff",
        Name.Builtin:           "#ff2266",
        Name.Builtin.Pseudo:    "#ff2266",
        Name.Class:             "#00ccff",
        Name.Constant:          "#ffcc33",
        Name.Decorator:         "#ff2266",
        Name.Entity:            "#ff2266",
        Name.Exception:         "#ff2266",
        Name.Function:          "#00ccff",
        Name.Property:          "#00ccff",
        Name.Label:             "#eeeeff",
        Name.Namespace:         "#ffcc33",
        Name.Other:             "#eeeeff",
        Name.Tag:               "#ff2266",
        Name.Variable:          "#ff2266",
        Name.Variable.Class:    "#00ccff",
        Name.Variable.Global:   "#ff2266",
        Name.Variable.Instance: "#ff2266",
        String:                 "#33ff99",
        String.Backtick:        "#33ff99",
        String.Char:            "#33ff99",
        String.Char:            "#33ff99",
        String.Doc:             "#33ff99", # Docstrings same as strings
        String.Double:          "#33ff99",
        String.Escape:          "#ff2266", # Neon pink for escape sequences
        String.Heredoc:         "#33ff99",
        String.Interpol:        "#ff2266", # Neon pink for interpolated parts
        String.Other:           "#33ff99",
        String.Regex:           "#33ff99", # Regexes same as strings
        String.Single:          "#33ff99",
        String.Symbol:          "#33ff99", # Symbols same as strings
        Number:                 "#ffcc33",
        Number.Float:           "#ffcc33",
        Number.Hex:             "#ffcc33",
        Number.Integer:         "#ffcc33",
        Number.Integer.Long:    "#ffcc33",
        Number.Oct:             "#ffcc33",
        Keyword:                "#ff2266",
        Keyword.Constant:       "#ff2266",
        Keyword.Declaration:    "#ff2266",
        Keyword.Namespace:      "#ff2266",
        Keyword.Pseudo:         "#ff2266",
        Keyword.Reserved:       "#ff2266",
        Keyword.Type:           "#00ccff", # Neon blue for type keywords
        Generic:                "#eeeeff", # Generic text
        Generic.Deleted:        "#ff2266 bg:#441122", # Neon pink for deleted lines
        Generic.Emph:           "italic #eeeeff", # Italic light text for emphasis
        Generic.Error:          "#ff2266", # Neon pink for generic errors
        Generic.Heading:        "bold #eeeeff", # Bold light text for headings
        Generic.Inserted:       "#33ff99 bg:#114433", # Neon green for inserted lines
        Generic.Output:         "#444455", # Dark grey/blue for output
        Generic.Prompt:         "#ff2266", # Neon pink for prompts
        Generic.Strong:         "bold #eeeeff", # Bold light text for strong emphasis
        Generic.Subheading:     "bold #00ccff", # Bold neon blue for subheadings
        Generic.Traceback:      "#ff2266", # Neon pink for tracebacks
        Literal:                "#eeeeff", # Light text for literals
        Literal.Date:           "#33ff99", # Neon green for dates
        Comment:                "#7777aa", # Grey/purple for comments
        Comment.Multiline:      "#7777aa",
        Comment.Preproc:        "#ff2266", # Neon pink for preprocessor comments
        Comment.Single:         "#7777aa",
        Comment.Special:        "bold #7777aa", # Bold grey/purple for special comments
        Operator:               "#ff2266", # Neon pink for operators
        Operator.Word:          "#ff2266", # Neon pink for word operators
        Punctuation:            "#eeeeff", # Light text for punctuation
    }

class DRACULA(Style):
    """
    Dracula Theme - A popular dark theme with a distinct purple and cyan palette.
    """
    background_color = "#282a36" # Dark purple-grey background
    styles = {
        Text:                   "#f8f8f2", # Off-white text
        Whitespace:             "#44475a", # Grey background color for subtle whitespace
        Error:                  "#ff5555", # Soft red for errors
        Other:                  "#f8f8f2", # Default text
        Name:                   "#f8f8f2", # Off-white for general names
        Name.Attribute:         "#50fa7b", # Green for attributes
        Name.Builtin:           "#8be9fd", # Cyan for builtins
        Name.Builtin.Pseudo:    "#8be9fd", # Cyan for pseudo builtins
        Name.Class:             "#50fa7b", # Green for class names
        Name.Constant:          "#bd93f9", # Purple for constants
        Name.Decorator:         "#f1fa8c", # Yellow for decorators
        Name.Entity:            "#f1fa8c", # Yellow for HTML/XML entities
        Name.Exception:         "#ff5555", # Soft red for exceptions
        Name.Function:          "#50fa7b", # Green for functions
        Name.Property:          "#f8f8f2", # Off-white for properties
        Name.Label:             "#8be9fd", # Cyan for labels
        Name.Namespace:         "#f8f8f2", # Off-white for namespaces
        Name.Other:             "#f8f8f2", # Off-white for other names
        Name.Tag:               "#ff79c6", # Pink for HTML/XML tags
        Name.Variable:          "#f8f8f2", # Off-white for variables
        Name.Variable.Class:    "#8be9fd", # Cyan for class variables ('cls', 'self')
        Name.Variable.Global:   "#bd93f9", # Purple for global variables
        Name.Variable.Instance: "#f8f8f2", # Off-white for instance variables
        String:                 "#f1fa8c", # Yellow for strings
        String.Backtick:        "#f1fa8c",
        String.Char:            "#f1fa8c",
        String.Doc:             "#6272a4", # Use comment color for docstrings for contrast
        String.Double:          "#f1fa8c",
        String.Escape:          "#ff79c6", # Pink for escape sequences
        String.Heredoc:         "#f1fa8c",
        String.Interpol:        "#ff79c6", # Pink for interpolated parts (f-strings)
        String.Other:           "#f1fa8c",
        String.Regex:           "#f1fa8c", # Regexes same as strings
        String.Single:          "#f1fa8c",
        String.Symbol:          "#f1fa8c", # Symbols same as strings
        Number:                 "#bd93f9", # Purple for numbers
        Number.Float:           "#bd93f9",
        Number.Hex:             "#bd93f9",
        Number.Integer:         "#bd93f9",
        Number.Integer.Long:    "#bd93f9",
        Number.Oct:             "#bd93f9",
        Keyword:                "#ff79c6", # Pink for keywords
        Keyword.Constant:       "#bd93f9", # Purple for keyword constants (True, False, None)
        Keyword.Declaration:    "#8be9fd", # Cyan for declaration keywords (def, class)
        Keyword.Namespace:      "#ff79c6", # Pink for import/from
        Keyword.Pseudo:         "#bd93f9", # Purple for pseudo keywords
        Keyword.Reserved:       "#ff79c6", # Pink for reserved words
        Keyword.Type:           "#8be9fd", # Cyan for type keywords (int, str)
        Generic:                "#f8f8f2", # Generic text
        Generic.Deleted:        "#ff5555 bg:#44475a", # Soft red for deleted lines (diff)
        Generic.Emph:           "italic #f8f8f2", # Italic off-white for emphasis
        Generic.Error:          "#ff5555", # Soft red for generic errors
        Generic.Heading:        "bold #f8f8f2", # Bold off-white for headings
        Generic.Inserted:       "#50fa7b bg:#44475a", # Green for inserted lines (diff)
        Generic.Output:         "#44475a", # Grey for program output
        Generic.Prompt:         "#50fa7b", # Green for prompts
        Generic.Strong:         "bold #f8f8f2", # Bold off-white for strong emphasis
        Generic.Subheading:     "bold #bd93f9", # Bold purple for subheadings
        Generic.Traceback:      "#ff5555", # Soft red for tracebacks
        Literal:                "#f8f8f2", # Off-white for literals
        Literal.Date:           "#f1fa8c", # Yellow for dates
        Comment:                "#6272a4", # Grey-purple for comments
        Comment.Multiline:      "#6272a4",
        Comment.Preproc:        "#ff79c6", # Pink for preprocessor comments
        Comment.Single:         "#6272a4",
        Comment.Special:        "bold #6272a4", # Bold grey-purple for special comments (TODO, FIXME)
        Operator:               "#ff79c6", # Pink for operators
        Operator.Word:          "#ff79c6", # Pink for word operators (and, or, not)
        Punctuation:            "#f8f8f2", # Off-white for punctuation
    }

class MONOKAI(Style):
    """
    Monokai Theme - A classic dark theme known for its vibrant green, pink, and blue colors.
    """
    background_color = "#272822" # Dark grey background
    styles = {
        Text:                   "#f8f8f2", # Off-white text
        Whitespace:             "#3b3a32", # Slightly lighter grey for subtle whitespace
        Error:                  "#f92672", # Bright pink for errors
        Other:                  "#f8f8f2", # Default text
        Name:                   "#f8f8f2", # Off-white for general names
        Name.Attribute:         "#a6e22e", # Bright green for attributes
        Name.Builtin:           "#66d9ef", # Bright cyan for builtins
        Name.Builtin.Pseudo:    "#66d9ef", # Bright cyan for pseudo builtins
        Name.Class:             "#a6e22e", # Bright green for class names
        Name.Constant:          "#ae81ff", # Purple for constants
        Name.Decorator:         "#a6e22e", # Bright green for decorators
        Name.Entity:            "#ae81ff", # Purple for HTML/XML entities
        Name.Exception:         "#f92672", # Bright pink for exceptions
        Name.Function:          "#a6e22e", # Bright green for functions
        Name.Property:          "#f8f8f2", # Off-white for properties
        Name.Label:             "#e6db74", # Yellow for labels
        Name.Namespace:         "#f8f8f2", # Off-white for namespaces
        Name.Other:             "#f8f8f2", # Off-white for other names
        Name.Tag:               "#f92672", # Bright pink for HTML/XML tags
        Name.Variable:          "#f8f8f2", # Off-white for variables
        Name.Variable.Class:    "#a6e22e", # Bright green for class variables ('cls', 'self')
        Name.Variable.Global:   "#f8f8f2", # Off-white for global variables
        Name.Variable.Instance: "#fd971f", # Orange for instance variables
        String:                 "#e6db74", # Yellow for strings
        String.Backtick:        "#e6db74",
        String.Char:            "#e6db74",
        String.Doc:             "#75715e", # Use comment color for docstrings
        String.Double:          "#e6db74",
        String.Escape:          "#ae81ff", # Purple for escape sequences
        String.Heredoc:         "#e6db74",
        String.Interpol:        "#fd971f", # Orange for interpolated parts (f-strings)
        String.Other:           "#e6db74",
        String.Regex:           "#e6db74", # Regexes same as strings
        String.Single:          "#e6db74",
        String.Symbol:          "#e6db74", # Symbols same as strings
        Number:                 "#ae81ff", # Purple for numbers
        Number.Float:           "#ae81ff",
        Number.Hex:             "#ae81ff",
        Number.Integer:         "#ae81ff",
        Number.Integer.Long:    "#ae81ff",
        Number.Oct:             "#ae81ff",
        Keyword:                "#f92672", # Bright pink for keywords
        Keyword.Constant:       "#66d9ef", # Bright cyan for keyword constants (True, False, None)
        Keyword.Declaration:    "#66d9ef", # Bright cyan for declaration keywords (def, class)
        Keyword.Namespace:      "#f92672", # Bright pink for import/from
        Keyword.Pseudo:         "#ae81ff", # Purple for pseudo keywords
        Keyword.Reserved:       "#f92672", # Bright pink for reserved words
        Keyword.Type:           "#66d9ef", # Bright cyan for type keywords (int, str)
        Generic:                "#f8f8f2", # Generic text
        Generic.Deleted:        "#f92672 bg:#3b3a32", # Bright pink for deleted lines (diff)
        Generic.Emph:           "italic #f8f8f2", # Italic off-white for emphasis
        Generic.Error:          "#f92672", # Bright pink for generic errors
        Generic.Heading:        "bold #f8f8f2", # Bold off-white for headings
        Generic.Inserted:       "#a6e22e bg:#3b3a32", # Bright green for inserted lines (diff)
        Generic.Output:         "#49483e", # Darker grey for program output
        Generic.Prompt:         "#a6e22e", # Bright green for prompts
        Generic.Strong:         "bold #f8f8f2", # Bold off-white for strong emphasis
        Generic.Subheading:     "bold #a6e22e", # Bold bright green for subheadings
        Generic.Traceback:      "#f92672", # Bright pink for tracebacks
        Literal:                "#ae81ff", # Purple for literals (e.g., numbers within code)
        Literal.Date:           "#e6db74", # Yellow for dates
        Comment:                "#75715e", # Grey for comments
        Comment.Multiline:      "#75715e",
        Comment.Preproc:        "#f92672", # Bright pink for preprocessor comments
        Comment.Single:         "#75715e",
        Comment.Special:        "bold italic #75715e", # Bold italic grey for special comments
        Operator:               "#f92672", # Bright pink for operators
        Operator.Word:          "#f92672", # Bright pink for word operators (and, or, not)
        Punctuation:            "#f8f8f2", # Off-white for punctuation
    }


def create_custom_style(name, colors):
    """
    Create a custom color style for syntax highlighting.

    Args:
        name (str): The name of the custom style.
        colors (dict): A dictionary mapping token types to color strings.
                       Keys should be pygments.token types (e.g., Text, Keyword.Constant).
                       Values should be color strings (e.g., "#ff0000", "bold #00ff00", "italic").

    Returns:
        type: A new Style class (a type object) with the specified colors
              and default background.
    """
    # Ensure the base Text token has a color if not provided
    if Text not in colors:
        colors[Text] = '#ffffff' # Default to white text

    # Define the attributes for the new style class
    style_attrs = {
        'background_color': "#000000", # Default to black background
        'styles': colors
    }

    # Dynamically create the new Style subclass
    CustomStyle = type(name, (Style,), style_attrs)
    return CustomStyle
