"""Applicazione di ricerca file 3D"""

import sys
from PySide6.QtWidgets import QApplication
from frontend import SearchGUI
from config import CARTELLE_DA_CERCARE, APP_NAME, APP_VERSION, APP_ORGANIZATION, APP_ID
from utils import create_app_icon, setup_windows_taskbar_icon

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_ORGANIZATION)
    app.setWindowIcon(create_app_icon())
    setup_windows_taskbar_icon(APP_ID)
    
    window = SearchGUI(cartelle_da_cercare=CARTELLE_DA_CERCARE)
    window.run()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()