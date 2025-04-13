"""
Module for creating custom color styles.
"""
from pygments.style import Style
from pygments.token import Text


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
        colors[Text] = '#ffffff'  # Default to white text

    # Define the attributes for the new style class
    style_attrs = {
        'background_color': "#000000",  # Default to black background
        'styles': colors
    }

    # Dynamically create the new Style subclass
    CustomStyle = type(name, (Style,), style_attrs)
    return CustomStyle
