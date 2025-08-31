"""Riduttore JPEG - Applicazione per la compressione e ottimizzazione di immagini JPEG."""

import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from main_window import MainWindow

def get_resource_path(relative_path):
    """Ottiene il percorso corretto per le risorse sia in sviluppo che nell'eseguibile."""
    try:
        # PyInstaller crea una cartella temporanea e memorizza il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('lightpic.imageprocessor.1.0')
    except:
        pass
    
    app = QApplication(sys.argv)
    
    try:
        icon_path = get_resource_path("favicon.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
    except:
        pass
    
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
