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
It includes several predefined color schemes and the ability to create custom styles.

Available themes:
- JARVIS: A Tron-inspired theme with black background and vibrant cyan/green/magenta highlights
- RICH: Inspired by the Rich library's default theme
- MODERN: A high-contrast dark theme with blues, purples, and greens
- NEON: Extremely bright, high-contrast colors on a black background
- CYBERPUNK: Dark blue/purple background with neon pink, blue, and green highlights
- DRACULA: A popular dark theme with a distinct purple and cyan palette
- MONOKAI: A classic dark theme known for its vibrant green, pink, and blue colors
- SOLARIZED: Based on the popular Solarized color scheme with its distinctive palette
- NORD: Based on the Nord color scheme with its arctic, bluish colors
- GITHUB: Based on GitHub's light theme for a familiar look
- VSCODE: Based on VS Code's default dark theme
- MATERIAL: Based on Material Design colors for a modern look
- RETRO: A retro computing theme with amber/green on black
- OCEAN: A calming blue-based theme
- AUTUMN: A warm theme with autumn colors
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


class SOLARIZED(Style):
    """
    Solarized Theme - A popular color scheme known for its carefully chosen contrasts and readability.
    This is the dark variant of Solarized.
    """
    background_color = "#002b36" # Base03 (dark background)
    styles = {
        Text:                   "#839496", # Base0 (primary content)
        Whitespace:             "#073642", # Base02 (subtle highlights)
        Error:                  "#dc322f", # Red
        Other:                  "#839496", # Base0
        Name:                   "#839496", # Base0
        Name.Attribute:         "#268bd2", # Blue
        Name.Builtin:           "#859900", # Green
        Name.Builtin.Pseudo:    "#859900", # Green
        Name.Class:             "#268bd2", # Blue
        Name.Constant:          "#6c71c4", # Violet
        Name.Decorator:         "#cb4b16", # Orange
        Name.Entity:            "#cb4b16", # Orange
        Name.Exception:         "#dc322f", # Red
        Name.Function:          "#268bd2", # Blue
        Name.Property:          "#839496", # Base0
        Name.Label:             "#839496", # Base0
        Name.Namespace:         "#b58900", # Yellow
        Name.Other:             "#839496", # Base0
        Name.Tag:               "#268bd2", # Blue
        Name.Variable:          "#cb4b16", # Orange
        Name.Variable.Class:    "#268bd2", # Blue
        Name.Variable.Global:   "#cb4b16", # Orange
        Name.Variable.Instance: "#cb4b16", # Orange
        String:                 "#2aa198", # Cyan
        String.Backtick:        "#2aa198", # Cyan
        String.Char:            "#2aa198", # Cyan
        String.Doc:             "#586e75", # Base01 (comments)
        String.Double:          "#2aa198", # Cyan
        String.Escape:          "#cb4b16", # Orange
        String.Heredoc:         "#2aa198", # Cyan
        String.Interpol:        "#cb4b16", # Orange
        String.Other:           "#2aa198", # Cyan
        String.Regex:           "#2aa198", # Cyan
        String.Single:          "#2aa198", # Cyan
        String.Symbol:          "#2aa198", # Cyan
        Number:                 "#d33682", # Magenta
        Number.Float:           "#d33682", # Magenta
        Number.Hex:             "#d33682", # Magenta
        Number.Integer:         "#d33682", # Magenta
        Number.Integer.Long:    "#d33682", # Magenta
        Number.Oct:             "#d33682", # Magenta
        Keyword:                "#859900", # Green
        Keyword.Constant:       "#6c71c4", # Violet
        Keyword.Declaration:    "#268bd2", # Blue
        Keyword.Namespace:      "#859900", # Green
        Keyword.Pseudo:         "#859900", # Green
        Keyword.Reserved:       "#859900", # Green
        Keyword.Type:           "#b58900", # Yellow
        Generic:                "#839496", # Base0
        Generic.Deleted:        "#dc322f bg:#073642", # Red on Base02
        Generic.Emph:           "italic #839496", # Italic Base0
        Generic.Error:          "#dc322f", # Red
        Generic.Heading:        "bold #839496", # Bold Base0
        Generic.Inserted:       "#859900 bg:#073642", # Green on Base02
        Generic.Output:         "#586e75", # Base01
        Generic.Prompt:         "#268bd2", # Blue
        Generic.Strong:         "bold #839496", # Bold Base0
        Generic.Subheading:     "bold #268bd2", # Bold Blue
        Generic.Traceback:      "#dc322f", # Red
        Literal:                "#839496", # Base0
        Literal.Date:           "#2aa198", # Cyan
        Comment:                "#586e75", # Base01
        Comment.Multiline:      "#586e75", # Base01
        Comment.Preproc:        "#cb4b16", # Orange
        Comment.Single:         "#586e75", # Base01
        Comment.Special:        "bold #586e75", # Bold Base01
        Operator:               "#839496", # Base0
        Operator.Word:          "#859900", # Green
        Punctuation:            "#839496", # Base0
    }


class NORD(Style):
    """
    Nord Theme - A clean, elegant theme with arctic, bluish colors.
    """
    background_color = "#2e3440" # Nord0 (polar night)
    styles = {
        Text:                   "#d8dee9", # Nord4 (snow storm)
        Whitespace:             "#3b4252", # Nord1 (darker polar night)
        Error:                  "#bf616a", # Nord11 (aurora red)
        Other:                  "#d8dee9", # Nord4
        Name:                   "#d8dee9", # Nord4
        Name.Attribute:         "#8fbcbb", # Nord7 (frost)
        Name.Builtin:           "#81a1c1", # Nord9 (frost)
        Name.Builtin.Pseudo:    "#81a1c1", # Nord9
        Name.Class:             "#8fbcbb", # Nord7
        Name.Constant:          "#5e81ac", # Nord10 (frost)
        Name.Decorator:         "#d08770", # Nord12 (aurora orange)
        Name.Entity:            "#d08770", # Nord12
        Name.Exception:         "#bf616a", # Nord11
        Name.Function:          "#88c0d0", # Nord8 (frost)
        Name.Property:          "#d8dee9", # Nord4
        Name.Label:             "#d8dee9", # Nord4
        Name.Namespace:         "#8fbcbb", # Nord7
        Name.Other:             "#d8dee9", # Nord4
        Name.Tag:               "#81a1c1", # Nord9
        Name.Variable:          "#d8dee9", # Nord4
        Name.Variable.Class:    "#8fbcbb", # Nord7
        Name.Variable.Global:   "#81a1c1", # Nord9
        Name.Variable.Instance: "#d8dee9", # Nord4
        String:                 "#a3be8c", # Nord14 (aurora green)
        String.Backtick:        "#a3be8c", # Nord14
        String.Char:            "#a3be8c", # Nord14
        String.Doc:             "#616e88", # Blend of Nord2 and Nord3
        String.Double:          "#a3be8c", # Nord14
        String.Escape:          "#d08770", # Nord12
        String.Heredoc:         "#a3be8c", # Nord14
        String.Interpol:        "#d08770", # Nord12
        String.Other:           "#a3be8c", # Nord14
        String.Regex:           "#ebcb8b", # Nord13 (aurora yellow)
        String.Single:          "#a3be8c", # Nord14
        String.Symbol:          "#a3be8c", # Nord14
        Number:                 "#b48ead", # Nord15 (aurora purple)
        Number.Float:           "#b48ead", # Nord15
        Number.Hex:             "#b48ead", # Nord15
        Number.Integer:         "#b48ead", # Nord15
        Number.Integer.Long:    "#b48ead", # Nord15
        Number.Oct:             "#b48ead", # Nord15
        Keyword:                "#81a1c1", # Nord9
        Keyword.Constant:       "#5e81ac", # Nord10
        Keyword.Declaration:    "#81a1c1", # Nord9
        Keyword.Namespace:      "#81a1c1", # Nord9
        Keyword.Pseudo:         "#81a1c1", # Nord9
        Keyword.Reserved:       "#81a1c1", # Nord9
        Keyword.Type:           "#8fbcbb", # Nord7
        Generic:                "#d8dee9", # Nord4
        Generic.Deleted:        "#bf616a bg:#3b4252", # Nord11 on Nord1
        Generic.Emph:           "italic #d8dee9", # Italic Nord4
        Generic.Error:          "#bf616a", # Nord11
        Generic.Heading:        "bold #d8dee9", # Bold Nord4
        Generic.Inserted:       "#a3be8c bg:#3b4252", # Nord14 on Nord1
        Generic.Output:         "#4c566a", # Nord3 (polar night)
        Generic.Prompt:         "#88c0d0", # Nord8
        Generic.Strong:         "bold #d8dee9", # Bold Nord4
        Generic.Subheading:     "bold #88c0d0", # Bold Nord8
        Generic.Traceback:      "#bf616a", # Nord11
        Literal:                "#d8dee9", # Nord4
        Literal.Date:           "#a3be8c", # Nord14
        Comment:                "#616e88", # Blend of Nord2 and Nord3
        Comment.Multiline:      "#616e88", # Blend of Nord2 and Nord3
        Comment.Preproc:        "#5e81ac", # Nord10
        Comment.Single:         "#616e88", # Blend of Nord2 and Nord3
        Comment.Special:        "bold #616e88", # Bold blend of Nord2 and Nord3
        Operator:               "#81a1c1", # Nord9
        Operator.Word:          "#81a1c1", # Nord9
        Punctuation:            "#d8dee9", # Nord4
    }


class GITHUB(Style):
    """
    GitHub Theme - Based on GitHub's light theme for a familiar look.
    """
    background_color = "#ffffff" # White background
    styles = {
        Text:                   "#24292e", # GitHub's default text color
        Whitespace:             "#e1e4e8", # Light grey for whitespace
        Error:                  "#d73a49", # GitHub's red
        Other:                  "#24292e", # Default text
        Name:                   "#24292e", # Default text
        Name.Attribute:         "#005cc5", # GitHub's blue
        Name.Builtin:           "#6f42c1", # GitHub's purple
        Name.Builtin.Pseudo:    "#6f42c1", # GitHub's purple
        Name.Class:             "#6f42c1", # GitHub's purple
        Name.Constant:          "#005cc5", # GitHub's blue
        Name.Decorator:         "#6f42c1", # GitHub's purple
        Name.Entity:            "#6f42c1", # GitHub's purple
        Name.Exception:         "#d73a49", # GitHub's red
        Name.Function:          "#6f42c1", # GitHub's purple
        Name.Property:          "#005cc5", # GitHub's blue
        Name.Label:             "#24292e", # Default text
        Name.Namespace:         "#24292e", # Default text
        Name.Other:             "#24292e", # Default text
        Name.Tag:               "#22863a", # GitHub's green
        Name.Variable:          "#e36209", # GitHub's orange
        Name.Variable.Class:    "#e36209", # GitHub's orange
        Name.Variable.Global:   "#e36209", # GitHub's orange
        Name.Variable.Instance: "#e36209", # GitHub's orange
        String:                 "#032f62", # GitHub's blue for strings
        String.Backtick:        "#032f62", # GitHub's blue for strings
        String.Char:            "#032f62", # GitHub's blue for strings
        String.Doc:             "#6a737d", # GitHub's grey for comments
        String.Double:          "#032f62", # GitHub's blue for strings
        String.Escape:          "#005cc5", # GitHub's blue
        String.Heredoc:         "#032f62", # GitHub's blue for strings
        String.Interpol:        "#005cc5", # GitHub's blue
        String.Other:           "#032f62", # GitHub's blue for strings
        String.Regex:           "#032f62", # GitHub's blue for strings
        String.Single:          "#032f62", # GitHub's blue for strings
        String.Symbol:          "#032f62", # GitHub's blue for strings
        Number:                 "#005cc5", # GitHub's blue
        Number.Float:           "#005cc5", # GitHub's blue
        Number.Hex:             "#005cc5", # GitHub's blue
        Number.Integer:         "#005cc5", # GitHub's blue
        Number.Integer.Long:    "#005cc5", # GitHub's blue
        Number.Oct:             "#005cc5", # GitHub's blue
        Keyword:                "#d73a49", # GitHub's red
        Keyword.Constant:       "#005cc5", # GitHub's blue
        Keyword.Declaration:    "#d73a49", # GitHub's red
        Keyword.Namespace:      "#d73a49", # GitHub's red
        Keyword.Pseudo:         "#d73a49", # GitHub's red
        Keyword.Reserved:       "#d73a49", # GitHub's red
        Keyword.Type:           "#d73a49", # GitHub's red
        Generic:                "#24292e", # Default text
        Generic.Deleted:        "#b31d28 bg:#ffeef0", # GitHub's red on light red
        Generic.Emph:           "italic #24292e", # Italic default text
        Generic.Error:          "#b31d28", # GitHub's dark red
        Generic.Heading:        "bold #24292e", # Bold default text
        Generic.Inserted:       "#22863a bg:#f0fff4", # GitHub's green on light green
        Generic.Output:         "#6a737d", # GitHub's grey
        Generic.Prompt:         "#005cc5", # GitHub's blue
        Generic.Strong:         "bold #24292e", # Bold default text
        Generic.Subheading:     "bold #005cc5", # Bold blue
        Generic.Traceback:      "#b31d28", # GitHub's dark red
        Literal:                "#24292e", # Default text
        Literal.Date:           "#032f62", # GitHub's blue for strings
        Comment:                "#6a737d", # GitHub's grey for comments
        Comment.Multiline:      "#6a737d", # GitHub's grey for comments
        Comment.Preproc:        "#d73a49", # GitHub's red
        Comment.Single:         "#6a737d", # GitHub's grey for comments
        Comment.Special:        "bold #6a737d", # Bold grey for special comments
        Operator:               "#d73a49", # GitHub's red
        Operator.Word:          "#d73a49", # GitHub's red
        Punctuation:            "#24292e", # Default text
    }


class VSCODE(Style):
    """
    VS Code Theme - Based on VS Code's default dark theme.
    """
    background_color = "#1e1e1e" # VS Code dark theme background
    styles = {
        Text:                   "#d4d4d4", # VS Code default text
        Whitespace:             "#3e3e42", # Slightly lighter than background
        Error:                  "#f44747", # VS Code error red
        Other:                  "#d4d4d4", # Default text
        Name:                   "#d4d4d4", # Default text
        Name.Attribute:         "#9cdcfe", # VS Code light blue
        Name.Builtin:           "#569cd6", # VS Code blue
        Name.Builtin.Pseudo:    "#569cd6", # VS Code blue
        Name.Class:             "#4ec9b0", # VS Code teal
        Name.Constant:          "#4fc1ff", # VS Code bright blue
        Name.Decorator:         "#dcdcaa", # VS Code yellow/gold
        Name.Entity:            "#dcdcaa", # VS Code yellow/gold
        Name.Exception:         "#f44747", # VS Code error red
        Name.Function:          "#dcdcaa", # VS Code yellow/gold
        Name.Property:          "#9cdcfe", # VS Code light blue
        Name.Label:             "#d4d4d4", # Default text
        Name.Namespace:         "#4ec9b0", # VS Code teal
        Name.Other:             "#d4d4d4", # Default text
        Name.Tag:               "#569cd6", # VS Code blue
        Name.Variable:          "#9cdcfe", # VS Code light blue
        Name.Variable.Class:    "#9cdcfe", # VS Code light blue
        Name.Variable.Global:   "#9cdcfe", # VS Code light blue
        Name.Variable.Instance: "#9cdcfe", # VS Code light blue
        String:                 "#ce9178", # VS Code orange/brown
        String.Backtick:        "#ce9178", # VS Code orange/brown
        String.Char:            "#ce9178", # VS Code orange/brown
        String.Doc:             "#608b4e", # VS Code green (comments)
        String.Double:          "#ce9178", # VS Code orange/brown
        String.Escape:          "#d7ba7d", # VS Code light yellow
        String.Heredoc:         "#ce9178", # VS Code orange/brown
        String.Interpol:        "#d7ba7d", # VS Code light yellow
        String.Other:           "#ce9178", # VS Code orange/brown
        String.Regex:           "#d16969", # VS Code red/orange
        String.Single:          "#ce9178", # VS Code orange/brown
        String.Symbol:          "#ce9178", # VS Code orange/brown
        Number:                 "#b5cea8", # VS Code light green
        Number.Float:           "#b5cea8", # VS Code light green
        Number.Hex:             "#b5cea8", # VS Code light green
        Number.Integer:         "#b5cea8", # VS Code light green
        Number.Integer.Long:    "#b5cea8", # VS Code light green
        Number.Oct:             "#b5cea8", # VS Code light green
        Keyword:                "#c586c0", # VS Code purple
        Keyword.Constant:       "#569cd6", # VS Code blue
        Keyword.Declaration:    "#569cd6", # VS Code blue
        Keyword.Namespace:      "#c586c0", # VS Code purple
        Keyword.Pseudo:         "#c586c0", # VS Code purple
        Keyword.Reserved:       "#c586c0", # VS Code purple
        Keyword.Type:           "#569cd6", # VS Code blue
        Generic:                "#d4d4d4", # Default text
        Generic.Deleted:        "#f44747 bg:#3e3e42", # VS Code error red on darker background
        Generic.Emph:           "italic #d4d4d4", # Italic default text
        Generic.Error:          "#f44747", # VS Code error red
        Generic.Heading:        "bold #d4d4d4", # Bold default text
        Generic.Inserted:       "#b5cea8 bg:#3e3e42", # VS Code light green on darker background
        Generic.Output:         "#808080", # VS Code grey
        Generic.Prompt:         "#569cd6", # VS Code blue
        Generic.Strong:         "bold #d4d4d4", # Bold default text
        Generic.Subheading:     "bold #569cd6", # Bold blue
        Generic.Traceback:      "#f44747", # VS Code error red
        Literal:                "#d4d4d4", # Default text
        Literal.Date:           "#ce9178", # VS Code orange/brown
        Comment:                "#608b4e", # VS Code green
        Comment.Multiline:      "#608b4e", # VS Code green
        Comment.Preproc:        "#c586c0", # VS Code purple
        Comment.Single:         "#608b4e", # VS Code green
        Comment.Special:        "bold #608b4e", # Bold green
        Operator:               "#d4d4d4", # Default text
        Operator.Word:          "#c586c0", # VS Code purple
        Punctuation:            "#d4d4d4", # Default text
    }


class MATERIAL(Style):
    """
    Material Theme - Based on Material Design colors for a modern look.
    """
    background_color = "#263238" # Material dark background
    styles = {
        Text:                   "#eeffff", # Material light text
        Whitespace:             "#37474f", # Material darker blue-grey
        Error:                  "#ff5370", # Material red
        Other:                  "#eeffff", # Default text
        Name:                   "#eeffff", # Default text
        Name.Attribute:         "#82aaff", # Material blue
        Name.Builtin:           "#89ddff", # Material cyan
        Name.Builtin.Pseudo:    "#89ddff", # Material cyan
        Name.Class:             "#ffcb6b", # Material yellow
        Name.Constant:          "#f78c6c", # Material orange
        Name.Decorator:         "#82aaff", # Material blue
        Name.Entity:            "#82aaff", # Material blue
        Name.Exception:         "#f07178", # Material red-pink
        Name.Function:          "#82aaff", # Material blue
        Name.Property:          "#c792ea", # Material purple
        Name.Label:             "#eeffff", # Default text
        Name.Namespace:         "#ffcb6b", # Material yellow
        Name.Other:             "#eeffff", # Default text
        Name.Tag:               "#f07178", # Material red-pink
        Name.Variable:          "#eeffff", # Default text
        Name.Variable.Class:    "#eeffff", # Default text
        Name.Variable.Global:   "#eeffff", # Default text
        Name.Variable.Instance: "#eeffff", # Default text
        String:                 "#c3e88d", # Material green
        String.Backtick:        "#c3e88d", # Material green
        String.Char:            "#c3e88d", # Material green
        String.Doc:             "#546e7a", # Material blue-grey
        String.Double:          "#c3e88d", # Material green
        String.Escape:          "#89ddff", # Material cyan
        String.Heredoc:         "#c3e88d", # Material green
        String.Interpol:        "#89ddff", # Material cyan
        String.Other:           "#c3e88d", # Material green
        String.Regex:           "#89ddff", # Material cyan
        String.Single:          "#c3e88d", # Material green
        String.Symbol:          "#c3e88d", # Material green
        Number:                 "#f78c6c", # Material orange
        Number.Float:           "#f78c6c", # Material orange
        Number.Hex:             "#f78c6c", # Material orange
        Number.Integer:         "#f78c6c", # Material orange
        Number.Integer.Long:    "#f78c6c", # Material orange
        Number.Oct:             "#f78c6c", # Material orange
        Keyword:                "#c792ea", # Material purple
        Keyword.Constant:       "#89ddff", # Material cyan
        Keyword.Declaration:    "#c792ea", # Material purple
        Keyword.Namespace:      "#c792ea", # Material purple
        Keyword.Pseudo:         "#c792ea", # Material purple
        Keyword.Reserved:       "#c792ea", # Material purple
        Keyword.Type:           "#ffcb6b", # Material yellow
        Generic:                "#eeffff", # Default text
        Generic.Deleted:        "#ff5370 bg:#37474f", # Material red on darker background
        Generic.Emph:           "italic #eeffff", # Italic default text
        Generic.Error:          "#ff5370", # Material red
        Generic.Heading:        "bold #eeffff", # Bold default text
        Generic.Inserted:       "#c3e88d bg:#37474f", # Material green on darker background
        Generic.Output:         "#546e7a", # Material blue-grey
        Generic.Prompt:         "#82aaff", # Material blue
        Generic.Strong:         "bold #eeffff", # Bold default text
        Generic.Subheading:     "bold #82aaff", # Bold blue
        Generic.Traceback:      "#ff5370", # Material red
        Literal:                "#eeffff", # Default text
        Literal.Date:           "#c3e88d", # Material green
        Comment:                "#546e7a", # Material blue-grey
        Comment.Multiline:      "#546e7a", # Material blue-grey
        Comment.Preproc:        "#89ddff", # Material cyan
        Comment.Single:         "#546e7a", # Material blue-grey
        Comment.Special:        "bold #546e7a", # Bold blue-grey
        Operator:               "#89ddff", # Material cyan
        Operator.Word:          "#c792ea", # Material purple
        Punctuation:            "#89ddff", # Material cyan
    }


class RETRO(Style):
    """
    Retro Theme - A retro computing theme with amber/green on black.
    """
    background_color = "#000000" # Black background
    styles = {
        Text:                   "#ffb000", # Amber text
        Whitespace:             "#3a3000", # Dark amber
        Error:                  "#ff0000", # Red for errors
        Other:                  "#ffb000", # Amber text
        Name:                   "#ffb000", # Amber text
        Name.Attribute:         "#ffc000", # Brighter amber
        Name.Builtin:           "#00ff00", # Green for built-ins
        Name.Builtin.Pseudo:    "#00ff00", # Green for pseudo built-ins
        Name.Class:             "#ffd700", # Gold for classes
        Name.Constant:          "#ffd700", # Gold for constants
        Name.Decorator:         "#ffc000", # Brighter amber
        Name.Entity:            "#ffc000", # Brighter amber
        Name.Exception:         "#ff0000", # Red for exceptions
        Name.Function:          "#ffc000", # Brighter amber
        Name.Property:          "#ffb000", # Amber text
        Name.Label:             "#ffb000", # Amber text
        Name.Namespace:         "#ffd700", # Gold for namespaces
        Name.Other:             "#ffb000", # Amber text
        Name.Tag:               "#ffc000", # Brighter amber
        Name.Variable:          "#ffb000", # Amber text
        Name.Variable.Class:    "#ffb000", # Amber text
        Name.Variable.Global:   "#ffb000", # Amber text
        Name.Variable.Instance: "#ffb000", # Amber text
        String:                 "#00ff00", # Green for strings
        String.Backtick:        "#00ff00", # Green for strings
        String.Char:            "#00ff00", # Green for strings
        String.Doc:             "#007700", # Darker green for docstrings
        String.Double:          "#00ff00", # Green for strings
        String.Escape:          "#00aa00", # Darker green for escapes
        String.Heredoc:         "#00ff00", # Green for strings
        String.Interpol:        "#00aa00", # Darker green for interpolation
        String.Other:           "#00ff00", # Green for strings
        String.Regex:           "#00ff00", # Green for strings
        String.Single:          "#00ff00", # Green for strings
        String.Symbol:          "#00ff00", # Green for strings
        Number:                 "#ffd700", # Gold for numbers
        Number.Float:           "#ffd700", # Gold for numbers
        Number.Hex:             "#ffd700", # Gold for numbers
        Number.Integer:         "#ffd700", # Gold for numbers
        Number.Integer.Long:    "#ffd700", # Gold for numbers
        Number.Oct:             "#ffd700", # Gold for numbers
        Keyword:                "#ffc000", # Brighter amber
        Keyword.Constant:       "#ffd700", # Gold for constants
        Keyword.Declaration:    "#ffc000", # Brighter amber
        Keyword.Namespace:      "#ffc000", # Brighter amber
        Keyword.Pseudo:         "#ffc000", # Brighter amber
        Keyword.Reserved:       "#ffc000", # Brighter amber
        Keyword.Type:           "#ffd700", # Gold for types
        Generic:                "#ffb000", # Amber text
        Generic.Deleted:        "#ff0000 bg:#3a0000", # Red on dark red
        Generic.Emph:           "italic #ffb000", # Italic amber
        Generic.Error:          "#ff0000", # Red for errors
        Generic.Heading:        "bold #ffb000", # Bold amber
        Generic.Inserted:       "#00ff00 bg:#003a00", # Green on dark green
        Generic.Output:         "#777700", # Dark amber for output
        Generic.Prompt:         "#ffc000", # Brighter amber
        Generic.Strong:         "bold #ffb000", # Bold amber
        Generic.Subheading:     "bold #ffc000", # Bold brighter amber
        Generic.Traceback:      "#ff0000", # Red for tracebacks
        Literal:                "#ffb000", # Amber text
        Literal.Date:           "#00ff00", # Green for dates
        Comment:                "#777700", # Dark amber for comments
        Comment.Multiline:      "#777700", # Dark amber for comments
        Comment.Preproc:        "#ffc000", # Brighter amber
        Comment.Single:         "#777700", # Dark amber for comments
        Comment.Special:        "bold #777700", # Bold dark amber
        Operator:               "#ffc000", # Brighter amber
        Operator.Word:          "#ffc000", # Brighter amber
        Punctuation:            "#ffb000", # Amber text
    }


class OCEAN(Style):
    """
    Ocean Theme - A calming blue-based theme.
    """
    background_color = "#0f111a" # Deep blue background
    styles = {
        Text:                   "#8f93a2", # Light blue-grey text
        Whitespace:             "#1f2233", # Slightly lighter background
        Error:                  "#ff5370", # Coral red for errors
        Other:                  "#8f93a2", # Light blue-grey text
        Name:                   "#8f93a2", # Light blue-grey text
        Name.Attribute:         "#82aaff", # Bright blue
        Name.Builtin:           "#c792ea", # Purple
        Name.Builtin.Pseudo:    "#c792ea", # Purple
        Name.Class:             "#ffcb6b", # Yellow
        Name.Constant:          "#89ddff", # Cyan
        Name.Decorator:         "#82aaff", # Bright blue
        Name.Entity:            "#82aaff", # Bright blue
        Name.Exception:         "#f07178", # Coral
        Name.Function:          "#82aaff", # Bright blue
        Name.Property:          "#8f93a2", # Light blue-grey text
        Name.Label:             "#8f93a2", # Light blue-grey text
        Name.Namespace:         "#ffcb6b", # Yellow
        Name.Other:             "#8f93a2", # Light blue-grey text
        Name.Tag:               "#f07178", # Coral
        Name.Variable:          "#8f93a2", # Light blue-grey text
        Name.Variable.Class:    "#8f93a2", # Light blue-grey text
        Name.Variable.Global:   "#8f93a2", # Light blue-grey text
        Name.Variable.Instance: "#8f93a2", # Light blue-grey text
        String:                 "#c3e88d", # Green
        String.Backtick:        "#c3e88d", # Green
        String.Char:            "#c3e88d", # Green
        String.Doc:             "#464b5d", # Darker blue-grey
        String.Double:          "#c3e88d", # Green
        String.Escape:          "#89ddff", # Cyan
        String.Heredoc:         "#c3e88d", # Green
        String.Interpol:        "#89ddff", # Cyan
        String.Other:           "#c3e88d", # Green
        String.Regex:           "#89ddff", # Cyan
        String.Single:          "#c3e88d", # Green
        String.Symbol:          "#c3e88d", # Green
        Number:                 "#f78c6c", # Orange
        Number.Float:           "#f78c6c", # Orange
        Number.Hex:             "#f78c6c", # Orange
        Number.Integer:         "#f78c6c", # Orange
        Number.Integer.Long:    "#f78c6c", # Orange
        Number.Oct:             "#f78c6c", # Orange
        Keyword:                "#c792ea", # Purple
        Keyword.Constant:       "#89ddff", # Cyan
        Keyword.Declaration:    "#c792ea", # Purple
        Keyword.Namespace:      "#c792ea", # Purple
        Keyword.Pseudo:         "#c792ea", # Purple
        Keyword.Reserved:       "#c792ea", # Purple
        Keyword.Type:           "#ffcb6b", # Yellow
        Generic:                "#8f93a2", # Light blue-grey text
        Generic.Deleted:        "#ff5370 bg:#1f2233", # Coral on slightly lighter background
        Generic.Emph:           "italic #8f93a2", # Italic light blue-grey
        Generic.Error:          "#ff5370", # Coral
        Generic.Heading:        "bold #8f93a2", # Bold light blue-grey
        Generic.Inserted:       "#c3e88d bg:#1f2233", # Green on slightly lighter background
        Generic.Output:         "#464b5d", # Darker blue-grey
        Generic.Prompt:         "#82aaff", # Bright blue
        Generic.Strong:         "bold #8f93a2", # Bold light blue-grey
        Generic.Subheading:     "bold #82aaff", # Bold bright blue
        Generic.Traceback:      "#ff5370", # Coral
        Literal:                "#8f93a2", # Light blue-grey text
        Literal.Date:           "#c3e88d", # Green
        Comment:                "#464b5d", # Darker blue-grey
        Comment.Multiline:      "#464b5d", # Darker blue-grey
        Comment.Preproc:        "#89ddff", # Cyan
        Comment.Single:         "#464b5d", # Darker blue-grey
        Comment.Special:        "bold #464b5d", # Bold darker blue-grey
        Operator:               "#89ddff", # Cyan
        Operator.Word:          "#c792ea", # Purple
        Punctuation:            "#89ddff", # Cyan
    }


class AUTUMN(Style):
    """
    Autumn Theme - A warm theme with autumn colors.
    """
    background_color = "#282218" # Dark brown background
    styles = {
        Text:                   "#e8dcc5", # Light tan text
        Whitespace:             "#3a3225", # Slightly lighter background
        Error:                  "#db4631", # Rust red for errors
        Other:                  "#e8dcc5", # Light tan text
        Name:                   "#e8dcc5", # Light tan text
        Name.Attribute:         "#e5a458", # Orange
        Name.Builtin:           "#b46950", # Rust
        Name.Builtin.Pseudo:    "#b46950", # Rust
        Name.Class:             "#e5a458", # Orange
        Name.Constant:          "#d9a762", # Gold
        Name.Decorator:         "#b46950", # Rust
        Name.Entity:            "#b46950", # Rust
        Name.Exception:         "#db4631", # Rust red
        Name.Function:          "#b46950", # Rust
        Name.Property:          "#e8dcc5", # Light tan text
        Name.Label:             "#e8dcc5", # Light tan text
        Name.Namespace:         "#e5a458", # Orange
        Name.Other:             "#e8dcc5", # Light tan text
        Name.Tag:               "#b46950", # Rust
        Name.Variable:          "#e8dcc5", # Light tan text
        Name.Variable.Class:    "#e8dcc5", # Light tan text
        Name.Variable.Global:   "#e8dcc5", # Light tan text
        Name.Variable.Instance: "#e8dcc5", # Light tan text
        String:                 "#7a9e67", # Olive green
        String.Backtick:        "#7a9e67", # Olive green
        String.Char:            "#7a9e67", # Olive green
        String.Doc:             "#6e6b5e", # Darker tan
        String.Double:          "#7a9e67", # Olive green
        String.Escape:          "#d9a762", # Gold
        String.Heredoc:         "#7a9e67", # Olive green
        String.Interpol:        "#d9a762", # Gold
        String.Other:           "#7a9e67", # Olive green
        String.Regex:           "#7a9e67", # Olive green
        String.Single:          "#7a9e67", # Olive green
        String.Symbol:          "#7a9e67", # Olive green
        Number:                 "#d9a762", # Gold
        Number.Float:           "#d9a762", # Gold
        Number.Hex:             "#d9a762", # Gold
        Number.Integer:         "#d9a762", # Gold
        Number.Integer.Long:    "#d9a762", # Gold
        Number.Oct:             "#d9a762", # Gold
        Keyword:                "#b46950", # Rust
        Keyword.Constant:       "#d9a762", # Gold
        Keyword.Declaration:    "#b46950", # Rust
        Keyword.Namespace:      "#b46950", # Rust
        Keyword.Pseudo:         "#b46950", # Rust
        Keyword.Reserved:       "#b46950", # Rust
        Keyword.Type:           "#e5a458", # Orange
        Generic:                "#e8dcc5", # Light tan text
        Generic.Deleted:        "#db4631 bg:#3a3225", # Rust red on slightly lighter background
        Generic.Emph:           "italic #e8dcc5", # Italic light tan
        Generic.Error:          "#db4631", # Rust red
        Generic.Heading:        "bold #e8dcc5", # Bold light tan
        Generic.Inserted:       "#7a9e67 bg:#3a3225", # Olive green on slightly lighter background
        Generic.Output:         "#6e6b5e", # Darker tan
        Generic.Prompt:         "#b46950", # Rust
        Generic.Strong:         "bold #e8dcc5", # Bold light tan
        Generic.Subheading:     "bold #e5a458", # Bold orange
        Generic.Traceback:      "#db4631", # Rust red
        Literal:                "#e8dcc5", # Light tan text
        Literal.Date:           "#7a9e67", # Olive green
        Comment:                "#6e6b5e", # Darker tan
        Comment.Multiline:      "#6e6b5e", # Darker tan
        Comment.Preproc:        "#b46950", # Rust
        Comment.Single:         "#6e6b5e", # Darker tan
        Comment.Special:        "bold #6e6b5e", # Bold darker tan
        Operator:               "#d9a762", # Gold
        Operator.Word:          "#b46950", # Rust
        Punctuation:            "#e8dcc5", # Light tan text
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
