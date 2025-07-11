"""
This package contains color styles for syntax highlighting in litprinter.

Each style is defined in its own module and can be imported directly:

from litprinter.styles.jarvis import JARVIS
from litprinter.styles.rich import RICH
from litprinter.styles.modern import MODERN
from litprinter.styles.neon import NEON
from litprinter.styles.cyberpunk import CYBERPUNK
from litprinter.styles.dracula import DRACULA
from litprinter.styles.monokai import MONOKAI
from litprinter.styles.solarized import SOLARIZED
from litprinter.styles.nord import NORD
from litprinter.styles.github import GITHUB
from litprinter.styles.vscode import VSCODE
from litprinter.styles.material import MATERIAL
from litprinter.styles.retro import RETRO
from litprinter.styles.ocean import OCEAN
from litprinter.styles.autumn import AUTUMN
from litprinter.styles.synthwave import SYNTHWAVE
from litprinter.styles.forest import FOREST
from litprinter.styles.monochrome import MONOCHROME
from litprinter.styles.sunset import SUNSET

# For creating custom styles
from litprinter.styles.custom import create_custom_style
"""

# Import all styles for easy access
from .jarvis import JARVIS
from .rich import RICH
from .modern import MODERN
from .neon import NEON
from .cyberpunk import CYBERPUNK
from .dracula import DRACULA
from .monokai import MONOKAI
from .solarized import SOLARIZED
from .nord import NORD
from .github import GITHUB
from .vscode import VSCODE
from .material import MATERIAL
from .retro import RETRO
from .ocean import OCEAN
from .autumn import AUTUMN
from .synthwave import SYNTHWAVE
from .forest import FOREST
from .monochrome import MONOCHROME
from .sunset import SUNSET
from .custom import create_custom_style

# Define what gets imported with 'from litprinter.styles import *'
__all__ = [
    'JARVIS', 'RICH', 'MODERN', 'NEON', 'CYBERPUNK', 'DRACULA', 'MONOKAI',
    'SOLARIZED', 'NORD', 'GITHUB', 'VSCODE', 'MATERIAL', 'RETRO', 'OCEAN',
    'AUTUMN', 'SYNTHWAVE', 'FOREST', 'MONOCHROME', 'SUNSET', 'create_custom_style'
]
