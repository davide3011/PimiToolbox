import os
from PySide6.QtGui import QIcon
from config import ICON_FILE

def get_icon_path():
    return os.path.join(os.path.dirname(__file__), ICON_FILE)

def create_app_icon():
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    return QIcon()

def setup_windows_taskbar_icon(app_id):
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        return True
    except (ImportError, AttributeError):
        return False