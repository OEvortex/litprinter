from .litprint import *
try:
    builtins = __import__('__builtin__')
except ImportError:
    builtins = __import__('builtins')

def install(name='litprint', ic='ic'):
    """
    Install litprint as a builtin function.
    
    Args:
        name (str): The name to install as a builtin. Default is 'litprint'.
        ic (str): The name to install as a builtin for icecream compatibility.
                 Default is 'ic'.
    """
    if name == 'litprint':
        setattr(builtins, name, litprint)
    
    # For icecream compatibility
    if ic:
        setattr(builtins, ic, litprint)

def uninstall(name='litprint', ic='ic'):
    """
    Uninstall litprint from builtins.
    
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
    # For icecream compatibility
    if ic and hasattr(builtins, ic):
        delattr(builtins, ic)
