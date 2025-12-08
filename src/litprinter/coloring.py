#!/usr/bin/env python3
"""
LitPrinter Coloring Module

Defines color styles for syntax highlighting in ic/lit output.
Includes IceCream-compatible SolarizedDark and custom LitPrinter styles.

Author: OEvortex <helpingai5@gmail.com>
License: MIT
"""

from pygments.style import Style
from pygments.token import (
    Text, Name, Error, Other,
    String, Number, Keyword, Generic, Literal,
    Comment, Operator, Whitespace, Punctuation
)


__all__ = [
    "TokyoNight",         # Beautiful Tokyo Night theme (NEW DEFAULT)
    "LitStyle",           # Catppuccin-inspired style
    "SolarizedDark",      # IceCream-compatible
    "CyberpunkStyle",     # Neon cyberpunk theme  
    "MonokaiStyle",       # Classic Monokai
    "DEFAULT_STYLE",      # Default style to use
]


# =============================================================================
# Tokyo Night - Stunning Dark Theme (NEW DEFAULT)
# Inspired by the popular Tokyo Night VSCode theme
# =============================================================================

class TokyoNight(Style):
    """Tokyo Night theme - Beautiful blue-purple dark theme with vibrant colors."""
    
    # Background & Foreground
    BG         = '#1a1b26'   # Deep blue-black background
    FG         = '#c0caf5'   # Soft lavender foreground
    FG_DARK    = '#a9b1d6'   # Muted foreground
    
    # Core colors
    COMMENT    = '#565f89'   # Muted blue-gray
    RED        = '#f7768e'   # Soft coral red
    ORANGE     = '#ff9e64'   # Warm orange
    YELLOW     = '#e0af68'   # Golden yellow
    GREEN      = '#9ece6a'   # Fresh green
    TEAL       = '#73daca'   # Aqua teal
    CYAN       = '#7dcfff'   # Sky blue cyan
    BLUE       = '#7aa2f7'   # Bright blue
    PURPLE     = '#bb9af7'   # Soft purple
    MAGENTA    = '#ff007c'   # Hot magenta
    PINK       = '#f7768e'   # Soft pink
    
    background_color = BG
    
    styles = {
        Text:                   FG,
        Whitespace:             BG,
        Error:                  RED,
        Other:                  FG,

        Name:                   FG,
        Name.Attribute:         TEAL,
        Name.Builtin:           CYAN,
        Name.Builtin.Pseudo:    CYAN,
        Name.Class:             TEAL,
        Name.Constant:          ORANGE,
        Name.Decorator:         YELLOW,
        Name.Entity:            ORANGE,
        Name.Exception:         RED,
        Name.Function:          BLUE,
        Name.Property:          TEAL,
        Name.Label:             FG,
        Name.Namespace:         PURPLE,
        Name.Other:             FG,
        Name.Tag:               RED,
        Name.Variable:          FG,
        Name.Variable.Class:    TEAL,
        Name.Variable.Global:   TEAL,
        Name.Variable.Instance: TEAL,

        String:                 GREEN,
        String.Backtick:        GREEN,
        String.Char:            GREEN,
        String.Doc:             COMMENT,
        String.Double:          GREEN,
        String.Escape:          ORANGE,
        String.Heredoc:         GREEN,
        String.Interpol:        CYAN,
        String.Other:           GREEN,
        String.Regex:           TEAL,
        String.Single:          GREEN,
        String.Symbol:          GREEN,

        Number:                 ORANGE,
        Number.Float:           ORANGE,
        Number.Hex:             ORANGE,
        Number.Integer:         ORANGE,
        Number.Integer.Long:    ORANGE,
        Number.Oct:             ORANGE,

        Keyword:                PURPLE,
        Keyword.Constant:       ORANGE,
        Keyword.Declaration:    PURPLE,
        Keyword.Namespace:      PURPLE,
        Keyword.Pseudo:         PURPLE,
        Keyword.Reserved:       PURPLE,
        Keyword.Type:           CYAN,

        Generic:                FG,
        Generic.Deleted:        RED,
        Generic.Emph:           'italic ' + FG,
        Generic.Error:          RED,
        Generic.Heading:        'bold ' + BLUE,
        Generic.Inserted:       GREEN,
        Generic.Output:         COMMENT,
        Generic.Prompt:         CYAN,
        Generic.Strong:         'bold ' + FG,
        Generic.Subheading:     'bold ' + PURPLE,
        Generic.Traceback:      RED,

        Literal:                FG,
        Literal.Date:           TEAL,

        Comment:                COMMENT,
        Comment.Multiline:      COMMENT,
        Comment.Preproc:        CYAN,
        Comment.Single:         COMMENT,
        Comment.Special:        'bold ' + YELLOW,

        Operator:               CYAN,
        Operator.Word:          PURPLE,

        Punctuation:            FG_DARK,
    }


# =============================================================================
# Solarized Dark (IceCream-compatible)
# https://ethanschoonover.com/solarized/
# =============================================================================

class SolarizedDark(Style):
    """Solarized Dark theme - Same as IceCream for compatibility."""
    
    BASE03  = '#002b36'
    BASE02  = '#073642'
    BASE01  = '#586e75'
    BASE00  = '#657b83'
    BASE0   = '#839496'
    BASE1   = '#93a1a1'
    BASE2   = '#eee8d5'
    BASE3   = '#fdf6e3'
    YELLOW  = '#b58900'
    ORANGE  = '#cb4b16'
    RED     = '#dc322f'
    MAGENTA = '#d33682'
    VIOLET  = '#6c71c4'
    BLUE    = '#268bd2'
    CYAN    = '#2aa198'
    GREEN   = '#859900'

    background_color = BASE03
    
    styles = {
        Text:                   BASE0,
        Whitespace:             BASE03,
        Error:                  RED,
        Other:                  BASE0,

        Name:                   BASE1,
        Name.Attribute:         BASE0,
        Name.Builtin:           BLUE,
        Name.Builtin.Pseudo:    BLUE,
        Name.Class:             BLUE,
        Name.Constant:          YELLOW,
        Name.Decorator:         ORANGE,
        Name.Entity:            ORANGE,
        Name.Exception:         ORANGE,
        Name.Function:          BLUE,
        Name.Property:          BLUE,
        Name.Label:             BASE0,
        Name.Namespace:         YELLOW,
        Name.Other:             BASE0,
        Name.Tag:               GREEN,
        Name.Variable:          ORANGE,
        Name.Variable.Class:    BLUE,
        Name.Variable.Global:   BLUE,
        Name.Variable.Instance: BLUE,

        String:                 CYAN,
        String.Backtick:        CYAN,
        String.Char:            CYAN,
        String.Doc:             CYAN,
        String.Double:          CYAN,
        String.Escape:          ORANGE,
        String.Heredoc:         CYAN,
        String.Interpol:        ORANGE,
        String.Other:           CYAN,
        String.Regex:           CYAN,
        String.Single:          CYAN,
        String.Symbol:          CYAN,

        Number:                 CYAN,
        Number.Float:           CYAN,
        Number.Hex:             CYAN,
        Number.Integer:         CYAN,
        Number.Integer.Long:    CYAN,
        Number.Oct:             CYAN,

        Keyword:                GREEN,
        Keyword.Constant:       GREEN,
        Keyword.Declaration:    GREEN,
        Keyword.Namespace:      ORANGE,
        Keyword.Pseudo:         ORANGE,
        Keyword.Reserved:       GREEN,
        Keyword.Type:           GREEN,

        Generic:                BASE0,
        Generic.Deleted:        RED,
        Generic.Emph:           'italic ' + BASE0,
        Generic.Error:          RED,
        Generic.Heading:        'bold ' + BASE0,
        Generic.Inserted:       GREEN,
        Generic.Output:         BASE01,
        Generic.Prompt:         BLUE,
        Generic.Strong:         'bold ' + BASE0,
        Generic.Subheading:     'bold ' + BLUE,
        Generic.Traceback:      RED,

        Literal:                BASE0,
        Literal.Date:           CYAN,

        Comment:                BASE01,
        Comment.Multiline:      BASE01,
        Comment.Preproc:        MAGENTA,
        Comment.Single:         BASE01,
        Comment.Special:        'bold ' + BASE01,

        Operator:               BASE0,
        Operator.Word:          GREEN,

        Punctuation:            BASE0,
    }


# =============================================================================
# LitStyle - Enhanced IceCream (Default)
# Brighter and more vibrant than Solarized for better visibility
# =============================================================================

class LitStyle(Style):
    """LitPrinter default style - Enhanced with brighter colors."""
    
    # Colors
    BG         = '#1e1e2e'   # Dark background
    FG         = '#cdd6f4'   # Light foreground
    COMMENT    = '#6c7086'   # Muted gray
    RED        = '#f38ba8'   # Soft red
    ORANGE     = '#fab387'   # Soft orange
    YELLOW     = '#f9e2af'   # Soft yellow  
    GREEN      = '#a6e3a1'   # Soft green
    TEAL       = '#94e2d5'   # Soft teal
    BLUE       = '#89b4fa'   # Soft blue
    PURPLE     = '#cba6f7'   # Soft purple
    PINK       = '#f5c2e7'   # Soft pink
    
    background_color = BG
    
    styles = {
        Text:                   FG,
        Whitespace:             BG,
        Error:                  RED,
        Other:                  FG,

        Name:                   FG,
        Name.Attribute:         TEAL,
        Name.Builtin:           PURPLE,
        Name.Builtin.Pseudo:    PURPLE,
        Name.Class:             YELLOW,
        Name.Constant:          ORANGE,
        Name.Decorator:         PINK,
        Name.Entity:            ORANGE,
        Name.Exception:         RED,
        Name.Function:          BLUE,
        Name.Property:          TEAL,
        Name.Label:             FG,
        Name.Namespace:         YELLOW,
        Name.Other:             FG,
        Name.Tag:               PINK,
        Name.Variable:          FG,
        Name.Variable.Class:    TEAL,
        Name.Variable.Global:   TEAL,
        Name.Variable.Instance: TEAL,

        String:                 GREEN,
        String.Backtick:        GREEN,
        String.Char:            GREEN,
        String.Doc:             COMMENT,
        String.Double:          GREEN,
        String.Escape:          ORANGE,
        String.Heredoc:         GREEN,
        String.Interpol:        ORANGE,
        String.Other:           GREEN,
        String.Regex:           PINK,
        String.Single:          GREEN,
        String.Symbol:          GREEN,

        Number:                 ORANGE,
        Number.Float:           ORANGE,
        Number.Hex:             ORANGE,
        Number.Integer:         ORANGE,
        Number.Integer.Long:    ORANGE,
        Number.Oct:             ORANGE,

        Keyword:                PURPLE,
        Keyword.Constant:       ORANGE,
        Keyword.Declaration:    PURPLE,
        Keyword.Namespace:      PINK,
        Keyword.Pseudo:         PURPLE,
        Keyword.Reserved:       PURPLE,
        Keyword.Type:           YELLOW,

        Generic:                FG,
        Generic.Deleted:        RED,
        Generic.Emph:           'italic ' + FG,
        Generic.Error:          RED,
        Generic.Heading:        'bold ' + BLUE,
        Generic.Inserted:       GREEN,
        Generic.Output:         COMMENT,
        Generic.Prompt:         BLUE,
        Generic.Strong:         'bold ' + FG,
        Generic.Subheading:     'bold ' + PURPLE,
        Generic.Traceback:      RED,

        Literal:                FG,
        Literal.Date:           TEAL,

        Comment:                COMMENT,
        Comment.Multiline:      COMMENT,
        Comment.Preproc:        PINK,
        Comment.Single:         COMMENT,
        Comment.Special:        'bold ' + COMMENT,

        Operator:               TEAL,
        Operator.Word:          PURPLE,

        Punctuation:            FG,
    }


# =============================================================================
# Cyberpunk Style - Neon colors
# =============================================================================

class CyberpunkStyle(Style):
    """Cyberpunk Style - Neon pink, blue, and green on dark background."""
    
    BG        = '#0c0c16'   # Dark blue-purple
    FG        = '#f0f0ff'   # Light blue-white
    COMMENT   = '#3d5a70'   # Muted blue
    PINK      = '#ff2e97'   # Neon pink
    TEAL      = '#00ffd9'   # Neon teal
    GREEN     = '#00ff6e'   # Neon green  
    YELLOW    = '#fffc58'   # Neon yellow
    
    background_color = BG
    
    styles = {
        Text:                   FG,
        Whitespace:             '#1a1a2a',
        Error:                  PINK,
        Other:                  FG,

        Name:                   FG,
        Name.Attribute:         TEAL,
        Name.Builtin:           PINK,
        Name.Builtin.Pseudo:    PINK,
        Name.Class:             TEAL,
        Name.Constant:          PINK,
        Name.Decorator:         YELLOW,
        Name.Entity:            YELLOW,
        Name.Exception:         PINK,
        Name.Function:          TEAL,
        Name.Property:          FG,
        Name.Label:             FG,
        Name.Namespace:         PINK,
        Name.Other:             FG,
        Name.Tag:               PINK,
        Name.Variable:          FG,
        Name.Variable.Class:    FG,
        Name.Variable.Global:   FG,
        Name.Variable.Instance: FG,

        String:                 GREEN,
        String.Backtick:        GREEN,
        String.Char:            GREEN,
        String.Doc:             COMMENT,
        String.Double:          GREEN,
        String.Escape:          YELLOW,
        String.Heredoc:         GREEN,
        String.Interpol:        YELLOW,
        String.Other:           GREEN,
        String.Regex:           GREEN,
        String.Single:          GREEN,
        String.Symbol:          GREEN,

        Number:                 YELLOW,
        Number.Float:           YELLOW,
        Number.Hex:             YELLOW,
        Number.Integer:         YELLOW,
        Number.Integer.Long:    YELLOW,
        Number.Oct:             YELLOW,

        Keyword:                PINK,
        Keyword.Constant:       PINK,
        Keyword.Declaration:    PINK,
        Keyword.Namespace:      PINK,
        Keyword.Pseudo:         PINK,
        Keyword.Reserved:       PINK,
        Keyword.Type:           TEAL,

        Generic:                FG,
        Generic.Deleted:        PINK + ' bg:#1a1a2a',
        Generic.Emph:           'italic ' + FG,
        Generic.Error:          PINK,
        Generic.Heading:        'bold ' + FG,
        Generic.Inserted:       GREEN + ' bg:#1a1a2a',
        Generic.Output:         COMMENT,
        Generic.Prompt:         TEAL,
        Generic.Strong:         'bold ' + FG,
        Generic.Subheading:     'bold ' + TEAL,
        Generic.Traceback:      PINK,

        Literal:                FG,
        Literal.Date:           GREEN,

        Comment:                COMMENT,
        Comment.Multiline:      COMMENT,
        Comment.Preproc:        PINK,
        Comment.Single:         COMMENT,
        Comment.Special:        'bold ' + COMMENT,

        Operator:               TEAL,
        Operator.Word:          PINK,

        Punctuation:            FG,
    }


# =============================================================================
# Monokai Style - Classic editor theme
# =============================================================================

class MonokaiStyle(Style):
    """Monokai Style - Classic code editor theme."""
    
    BG        = '#272822'
    FG        = '#f8f8f2'
    COMMENT   = '#75715e'
    RED       = '#f92672'
    ORANGE    = '#fd971f'
    YELLOW    = '#e6db74'
    GREEN     = '#a6e22e'
    BLUE      = '#66d9ef'
    PURPLE    = '#ae81ff'
    
    background_color = BG
    
    styles = {
        Text:                   FG,
        Whitespace:             BG,
        Error:                  RED,
        Other:                  FG,

        Name:                   FG,
        Name.Attribute:         GREEN,
        Name.Builtin:           BLUE,
        Name.Builtin.Pseudo:    BLUE,
        Name.Class:             GREEN,
        Name.Constant:          PURPLE,
        Name.Decorator:         GREEN,
        Name.Entity:            FG,
        Name.Exception:         GREEN,
        Name.Function:          GREEN,
        Name.Property:          FG,
        Name.Label:             FG,
        Name.Namespace:         FG,
        Name.Other:             FG,
        Name.Tag:               RED,
        Name.Variable:          FG,
        Name.Variable.Class:    FG,
        Name.Variable.Global:   FG,
        Name.Variable.Instance: FG,

        String:                 YELLOW,
        String.Backtick:        YELLOW,
        String.Char:            YELLOW,
        String.Doc:             COMMENT,
        String.Double:          YELLOW,
        String.Escape:          PURPLE,
        String.Heredoc:         YELLOW,
        String.Interpol:        PURPLE,
        String.Other:           YELLOW,
        String.Regex:           YELLOW,
        String.Single:          YELLOW,
        String.Symbol:          YELLOW,

        Number:                 PURPLE,
        Number.Float:           PURPLE,
        Number.Hex:             PURPLE,
        Number.Integer:         PURPLE,
        Number.Integer.Long:    PURPLE,
        Number.Oct:             PURPLE,

        Keyword:                RED,
        Keyword.Constant:       BLUE,
        Keyword.Declaration:    BLUE,
        Keyword.Namespace:      RED,
        Keyword.Pseudo:         BLUE,
        Keyword.Reserved:       RED,
        Keyword.Type:           BLUE,

        Generic:                FG,
        Generic.Deleted:        RED,
        Generic.Emph:           'italic ' + FG,
        Generic.Error:          RED,
        Generic.Heading:        'bold ' + FG,
        Generic.Inserted:       GREEN,
        Generic.Output:         COMMENT,
        Generic.Prompt:         BLUE,
        Generic.Strong:         'bold ' + FG,
        Generic.Subheading:     COMMENT,
        Generic.Traceback:      RED,

        Literal:                FG,
        Literal.Date:           YELLOW,

        Comment:                COMMENT,
        Comment.Multiline:      COMMENT,
        Comment.Preproc:        COMMENT,
        Comment.Single:         COMMENT,
        Comment.Special:        COMMENT,

        Operator:               RED,
        Operator.Word:          RED,

        Punctuation:            FG,
    }
# Default style - Tokyo Night for stunning blue-purple aesthetics
DEFAULT_STYLE = TokyoNight
