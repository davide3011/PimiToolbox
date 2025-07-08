import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QFrame, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QThread, Signal
from backend import FileSearcher
from config import (
    WINDOW_TITLE, WINDOW_SCREEN_RATIO, WINDOW_POSITION_OFFSET_RATIO,
    MESSAGES, UI_TEXTS, LAYOUT_CONFIG
)
from styles import get_application_styles
from utils import create_app_icon

class SearchThread(QThread):
    search_completed = Signal(dict)
    
    def __init__(self, file_searcher, search_prefix):
        super().__init__()
        self.file_searcher = file_searcher
        self.search_prefix = search_prefix
    
    def run(self):
        try:
            risultato = self.file_searcher.cerca_file(self.search_prefix)
            self.search_completed.emit(risultato)
        except Exception as e:
            self.search_completed.emit({"errore": f"Errore durante la ricerca: {str(e)}"})

class SearchGUI(QMainWindow):
    
    def __init__(self, cartelle_da_cercare=None):
        super().__init__()
        self.file_searcher = FileSearcher()
        self.file_searcher.set_cartelle(cartelle_da_cercare or [])
        self.search_thread = None
        self._setup_window()
        self._setup_ui()
        self.setStyleSheet(get_application_styles())
    
    def _setup_window(self):
        """Configura la finestra principale adattandola allo schermo"""
        self.setWindowTitle(WINDOW_TITLE)

        # Ottieni le dimensioni dello schermo primario
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        window_width = int(screen_width * WINDOW_SCREEN_RATIO[0])
        window_height = int(screen_height * WINDOW_SCREEN_RATIO[1])

        offset_x = int(screen_width * WINDOW_POSITION_OFFSET_RATIO[0])
        offset_y = int(screen_height * WINDOW_POSITION_OFFSET_RATIO[1])
        pos_x = (screen_width - window_width) // 2 + offset_x
        pos_y = (screen_height - window_height) // 2 + offset_y

        self.setGeometry(pos_x, pos_y, window_width, window_height)
        self.setMinimumSize(int(window_width * 0.7), int(window_height * 0.6))
        self.setMaximumSize(int(window_width * 1.5), int(window_height * 1.8))

        self._set_window_icon()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(LAYOUT_CONFIG['main_spacing'])
        self.main_layout.setContentsMargins(*LAYOUT_CONFIG['main_margins'])
    
    def _set_window_icon(self):
        self.setWindowIcon(create_app_icon())
    
    def _setup_ui(self):
        self._create_header()
        self._create_search_section()
        self._create_results_section()
        self.entry_prefisso.setFocus()
    
    def _create_header(self):
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        title_label = QLabel(UI_TEXTS['title'])
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel(UI_TEXTS['subtitle'])
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setObjectName("subtitle")
        header_layout.addWidget(subtitle_label)
        
        self.main_layout.addWidget(header_frame)
    
    def _create_search_section(self):
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QVBoxLayout(search_frame)
        
        prefix_label = QLabel(UI_TEXTS['prefix_label'])
        prefix_label.setObjectName("prefixLabel")
        search_layout.addWidget(prefix_label)
        
        input_layout = QHBoxLayout()
        
        self.entry_prefisso = QLineEdit()
        self.entry_prefisso.setObjectName("searchInput")
        self.entry_prefisso.setPlaceholderText(MESSAGES['search_placeholder'])
        self.entry_prefisso.returnPressed.connect(self.avvia_ricerca)
        input_layout.addWidget(self.entry_prefisso)
        
        self.btn_cerca = QPushButton(MESSAGES['search_button'])
        self.btn_cerca.setObjectName("searchButton")
        self.btn_cerca.clicked.connect(self.avvia_ricerca)
        input_layout.addWidget(self.btn_cerca)
        
        search_layout.addLayout(input_layout)
        self.main_layout.addWidget(search_frame)
    
    def _create_results_section(self):
        results_frame = QFrame()
        results_frame.setObjectName("resultsFrame")
        results_layout = QVBoxLayout(results_frame)
        
        results_label = QLabel(UI_TEXTS['results_label'])
        results_label.setObjectName("resultsLabel")
        results_layout.addWidget(results_label)
        
        self.list_risultati = QListWidget()
        self.list_risultati.setObjectName("resultsList")
        self.list_risultati.itemDoubleClicked.connect(self._handle_item_double_click)
        results_layout.addWidget(self.list_risultati, 1)
        
        self.info_label = QLabel(MESSAGES['double_click_info'])
        self.info_label.setObjectName("infoLabel")
        results_layout.addWidget(self.info_label)
        
        self.main_layout.addWidget(results_frame, 1)
        self._create_footer()
    
    def _create_footer(self):
        footer_frame = QFrame()
        footer_frame.setObjectName("footerFrame")
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(*LAYOUT_CONFIG['footer_margins'])
        
        footer_label = QLabel(UI_TEXTS['footer'])
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setObjectName("footerLabel")
        footer_layout.addWidget(footer_label)
        
        self.main_layout.addWidget(footer_frame)
    
    def avvia_ricerca(self):
        search_prefix = self.entry_prefisso.text().strip()
        
        if not search_prefix:
            QMessageBox.warning(self, MESSAGES['input_missing'], MESSAGES['insert_prefix'])
            return
        
        self._set_search_state(True)
        
        self.search_thread = SearchThread(self.file_searcher, search_prefix)
        self.search_thread.search_completed.connect(self._on_search_completed)
        self.search_thread.start()
    
    def _set_search_state(self, is_searching):
        if is_searching:
            self.btn_cerca.setEnabled(False)
            self.btn_cerca.setText(MESSAGES['searching'])
            self.list_risultati.clear()
            self.info_label.setText(MESSAGES['searching'])
        else:
            self.btn_cerca.setEnabled(True)
            self.btn_cerca.setText(MESSAGES['search_button'])
            self.info_label.setText(MESSAGES['double_click_info'])
    
    def _on_search_completed(self, risultato):
        self._set_search_state(False)
        
        if "errore" in risultato:
            QMessageBox.critical(self, MESSAGES['error_title'], risultato["errore"])
            self.info_label.setText(MESSAGES['error_prefix'])
            return
        
        self._display_results(risultato["risultati"])
    
    def _display_results(self, risultati):
        self.list_risultati.clear()
        
        if not risultati:
            item = QListWidgetItem(MESSAGES['no_results'])
            item.setData(Qt.UserRole, None)
            self.list_risultati.addItem(item)
            self.info_label.setText(MESSAGES['no_results'])
            return
        
        valid_files = 0
        for file_path in risultati:
            if file_path.startswith(("Attenzione:", "Errore:")):
                item = QListWidgetItem(file_path)
                item.setData(Qt.UserRole, None)
            else:
                item = QListWidgetItem(os.path.basename(file_path))
                item.setToolTip(f"Percorso completo: {file_path}")
                item.setData(Qt.UserRole, file_path)
                valid_files += 1
            self.list_risultati.addItem(item)
        
        self.info_label.setText(f"{MESSAGES['success_prefix']} {valid_files} file")
    
    def _handle_item_double_click(self, item):
        try:
            file_path = item.data(Qt.UserRole)
            if not file_path:
                return
            
            result = self.file_searcher.apri_file(file_path)
            if "errore" in result:
                QMessageBox.critical(self, MESSAGES['error_title'], f"{result['errore']}\n\nPercorso: {file_path}")
            else:
                self.info_label.setText(f"{MESSAGES['file_opened']} {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, MESSAGES['error_title'], f"Si è verificato un errore:\n{str(e)}")
    
    def aggiungi_cartella(self, cartella):
        self.file_searcher.aggiungi_cartella(cartella)
    
    def rimuovi_cartella(self, cartella):
        self.file_searcher.rimuovi_cartella(cartella)
    
    def get_cartelle(self):
        return self.file_searcher.get_cartelle()
    
    def run(self):
        self.show()