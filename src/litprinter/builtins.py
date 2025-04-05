from .litprint import litprint
from .lit import lit

try:
    builtins = __import__('__builtin__')
except ImportError:
    builtins = __import__('builtins')

def install(name='litprint', ic='ic'):
    """
    Install litprint or lit as a builtin function.
    
    Args:
        name (str): The name to install as a builtin. Default is 'litprint'.
                   Can also be 'lit' to install the shorter version.
        ic (str): The name to install as a builtin for icecream compatibility.
                 Default is 'ic'.
    """
    if name == 'litprint':
        setattr(builtins, name, litprint)
    elif name == 'lit':
        setattr(builtins, name, lit)
    
    # For icecream compatibility
    if ic:
        setattr(builtins, ic, lit)

def uninstall(name='litprint', ic='ic'):
    """
    Uninstall litprint or lit from builtins.
    
    Args:
        name (str): The name to uninstall from builtins. Default is 'litprint'.
        ic (str): The name to uninstall from builtins for icecream compatibility.
                 Default is 'ic'.
    """
    if hasattr(builtins, name):
        delattr(builtins, name)
    
    # For icecream compatibility
    if ic and hasattr(builtins, ic):
        delattr(builtins, ic)
