from utils.logger import Logger
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path is None:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_data_dir():
    """
    Get the directory for saving persistent data (config, logs).
    When running as a PyInstaller executable, use AppData/Local/DidacticSpoon.
    Otherwise, use the local directory.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
        return os.path.join(appdata, 'DidacticSpoon')
    else:
        # Running as script
        return os.path.abspath(".")
