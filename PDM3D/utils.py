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

def validate_file_path(file_path):
    if not file_path:
        return False, "Percorso file vuoto"
    
    if not os.path.exists(file_path):
        return False, "File non trovato"
    
    if not os.path.isfile(file_path):
        return False, "Il percorso non è un file valido"
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore'):
            pass
        return True, None
    except PermissionError:
        return False, "Permesso negato per accedere al file"
    except Exception as e:
        return False, f"Errore nell'accesso al file: {str(e)}"