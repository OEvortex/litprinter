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
- SYNTHWAVE: A retro 80s-inspired theme with neon purples and blues
- FOREST: A nature-inspired theme with various shades of green
- MONOCHROME: A minimalist black and white theme with high contrast
- SUNSET: A warm theme with sunset colors (oranges, reds, and purples)
"""

# Import all styles and the custom style creator from the styles package
from litprinter.styles import (
    JARVIS, RICH, MODERN, NEON, CYBERPUNK, DRACULA, MONOKAI, SOLARIZED, NORD,
    GITHUB, VSCODE, MATERIAL, RETRO, OCEAN, AUTUMN, SYNTHWAVE, FOREST, MONOCHROME,
    SUNSET, create_custom_style
)

# Re-export everything for backward compatibility
__all__ = [
    'JARVIS', 'RICH', 'MODERN', 'NEON', 'CYBERPUNK', 'DRACULA', 'MONOKAI',
    'SOLARIZED', 'NORD', 'GITHUB', 'VSCODE', 'MATERIAL', 'RETRO', 'OCEAN',
    'AUTUMN', 'SYNTHWAVE', 'FOREST', 'MONOCHROME', 'SUNSET', 'create_custom_style'
]
