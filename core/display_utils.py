"""
core/display_utils.py

Provides Quartz with essential display utilities such as getting the backing scale factor.

"""
from AppKit import NSScreen

def get_backing_scale_factor():
    """
    Returns the backing scale factor of the main screen.
    """
    screen = NSScreen.mainScreen()
    return screen.backingScaleFactor() if screen else 1.0