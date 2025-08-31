"""Modulo per la finestra principale dell'applicazione.

Questo modulo contiene la classe MainWindow che coordina tutti i componenti
dell'interfaccia utente e gestisce l'elaborazione delle immagini.
"""

import os
import sys
import threading
from typing import List, Optional
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTextEdit, QProgressBar
)

def get_resource_path(relative_path):
    """Ottiene il percorso corretto per le risorse sia in sviluppo che nell'eseguibile."""
    try:
        # PyInstaller crea una cartella temporanea e memorizza il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from config import Settings
from worker import Worker
from ui_components import (
    DropArea, SettingsPanel, OutputDirectorySelector, PresetButtons, FileSelector
)


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione Riduttore JPEG.
    
    Coordina tutti i componenti dell'interfaccia utente e gestisce
    l'elaborazione delle immagini attraverso il sistema di worker.
    """
    
    def __init__(self):
        """Inizializza la finestra principale."""
        super().__init__()
        
        # Stato dell'applicazione
        self.collected_paths: List[str] = []
        self.worker_thread: Optional[threading.Thread] = None
        self.worker_obj: Optional[Worker] = None
        
        # Configurazione della finestra
        self._setup_window()
        
        # Creazione dei componenti UI
        self._create_components()
        
        # Setup del layout
        self._setup_layout()
        
        # Connessione dei segnali
        self._connect_signals()
    
    def _setup_window(self) -> None:
        """Configura le proprietà base della finestra."""
        self.setWindowTitle("LightPic")
        self.setMinimumSize(QSize(900, 700))
        
        # Imposta l'icona della finestra
        try:
            # Percorso del file favicon.ico utilizzando get_resource_path
            icon_path = get_resource_path("favicon.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                # Fallback all'icona di sistema
                self.setWindowIcon(QIcon.fromTheme("image"))
        except Exception:
            pass  # Ignora se l'icona non è disponibile
    
    def _create_components(self) -> None:
        """Crea tutti i componenti dell'interfaccia utente."""
        # Area di trascinamento
        self.drop_area = DropArea()
        
        # Selettore di file da archivio
        self.file_selector = FileSelector()
        
        # Etichetta informativa sui file selezionati
        self.file_info_label = QLabel("Nessun elemento.")
        self.file_info_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        
        # Pulsanti per i preset
        self.preset_buttons = PresetButtons()
        
        # Pannello delle impostazioni
        self.settings_panel = SettingsPanel()
        
        # Selettore della cartella di output
        self.output_selector = OutputDirectorySelector()
        
        # Pulsanti di controllo
        self.btn_start = QPushButton("Elabora")
        self.btn_clear = QPushButton("Svuota lista")
        self.btn_stop = QPushButton("Interrompi")
        self.btn_stop.setEnabled(False)
        
        # Stile per i pulsanti
        button_style = """
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:enabled {
                background-color: #4a90e2;
                color: white;
                border: none;
            }
            QPushButton:hover:enabled {
                background-color: #357abd;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
                border: 1px solid #999999;
            }
        """
        
        for btn in [self.btn_start, self.btn_clear, self.btn_stop]:
            btn.setStyleSheet(button_style)
        
        # Barra di progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Area di log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(200)
        self.log_area.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                background-color: #f8f8f8;
                border: 1px solid #ddd;
            }
        """)
    
    def _setup_layout(self) -> None:
        """Configura il layout della finestra."""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        
        # Area di trascinamento
        main_layout.addWidget(self.drop_area)
        
        # Selettore di file da archivio
        main_layout.addWidget(self.file_selector)
        
        # Informazioni sui file
        main_layout.addWidget(self.file_info_label)
        
        # Pulsanti preset
        main_layout.addWidget(self.preset_buttons)
        
        # Pannello impostazioni
        main_layout.addWidget(self.settings_panel)
        
        # Selettore output
        main_layout.addWidget(self.output_selector)
        
        # Pulsanti di controllo
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_clear)
        button_layout.addWidget(self.btn_stop)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Barra di progresso
        main_layout.addWidget(self.progress_bar)
        
        # Area di log
        main_layout.addWidget(QLabel("Log di elaborazione:"))
        main_layout.addWidget(self.log_area)
        
        self.setCentralWidget(central_widget)
    
    def _connect_signals(self) -> None:
        """Connette tutti i segnali dei componenti."""
        # Area di trascinamento
        self.drop_area.filesDropped.connect(self._on_files_dropped)
        
        # Selettore di file da archivio
        self.file_selector.filesSelected.connect(self._on_files_dropped)
        
        # Pulsanti preset
        self.preset_buttons.presetSelected.connect(self._on_preset_selected)
        
        # Pulsanti di controllo
        self.btn_start.clicked.connect(self._start_processing)
        self.btn_clear.clicked.connect(self._clear_files)
        self.btn_stop.clicked.connect(self._stop_processing)
    
    def _on_files_dropped(self, paths: List[str]) -> None:
        """Gestisce il rilascio di file nell'area di trascinamento.
        
        Args:
            paths: Lista dei percorsi rilasciati
        """
        self.collected_paths.extend(paths)
        # Rimuove i duplicati mantenendo l'ordine
        self.collected_paths = list(dict.fromkeys(self.collected_paths))
        
        self._update_file_info()
        self._log_message(f"Aggiunti {len(paths)} elementi alla lista.")
    
    def _on_preset_selected(self, settings: Settings) -> None:
        """Gestisce la selezione di un preset.
        
        Args:
            settings: Impostazioni del preset selezionato
        """
        self.settings_panel.set_settings(settings)
        self._log_message("Preset applicato alle impostazioni.")
    
    def _update_file_info(self) -> None:
        """Aggiorna l'etichetta con le informazioni sui file."""
        count = len(self.collected_paths)
        if count == 0:
            text = "Nessun elemento."
        elif count == 1:
            text = "1 elemento selezionato (file/cartella)."
        else:
            text = f"{count} elementi selezionati (file/cartelle)."
        
        self.file_info_label.setText(text)
    
    def _clear_files(self) -> None:
        """Svuota la lista dei file selezionati."""
        self.collected_paths.clear()
        self._update_file_info()
        self.log_area.clear()
        self._log_message("Lista svuotata.")
    
    def _start_processing(self) -> None:
        """Avvia l'elaborazione delle immagini."""
        if not self.collected_paths:
            self._log_message("➡️ Trascina qui immagini o cartelle prima di avviare.")
            return
        
        # Ottiene le impostazioni correnti
        settings = self._gather_settings()
        
        # Configura l'interfaccia per l'elaborazione
        self._set_processing_state(True)
        
        self._log_message("🚀 Avvio elaborazione…")
        
        # Crea e avvia il worker
        self.worker_obj = Worker(self.collected_paths, settings)
        self.worker_thread = threading.Thread(
            target=self.worker_obj.run, 
            daemon=True
        )
        
        # Connette i segnali del worker
        self.worker_obj.log.connect(self._log_message)
        self.worker_obj.progress.connect(self._update_progress)
        self.worker_obj.done.connect(self._on_processing_done)
        
        # Avvia il thread
        self.worker_thread.start()
    
    def _stop_processing(self) -> None:
        """Interrompe l'elaborazione in corso."""
        if self.worker_obj:
            self.worker_obj.stop()
            self._log_message("⏹️ Richiesta di interruzione inviata...")
    
    def _gather_settings(self) -> Settings:
        """Raccoglie le impostazioni correnti dall'interfaccia.
        
        Returns:
            Un'istanza di Settings con i valori correnti
        """
        settings = self.settings_panel.get_settings()
        settings.output_dir = self.output_selector.get_directory()
        return settings
    
    def _set_processing_state(self, processing: bool) -> None:
        """Configura l'interfaccia per lo stato di elaborazione.
        
        Args:
            processing: True se l'elaborazione è in corso
        """
        self.btn_start.setEnabled(not processing)
        self.btn_stop.setEnabled(processing)
        self.drop_area.setEnabled(not processing)
        self.settings_panel.setEnabled(not processing)
        self.output_selector.setEnabled(not processing)
        self.preset_buttons.setEnabled(not processing)
        
        if processing:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
        else:
            self.progress_bar.setVisible(False)
    
    def _update_progress(self, current: int, total: int) -> None:
        """Aggiorna la barra di progresso.
        
        Args:
            current: Numero di file elaborati
            total: Numero totale di file
        """
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.progress_bar.setFormat(f"{current}/{total} ({percentage}%)")
    
    def _on_processing_done(self) -> None:
        """Gestisce il completamento dell'elaborazione."""
        self._set_processing_state(False)
        self._log_message("\n✅ Elaborazione completata.")
        
        # Pulisce i riferimenti al worker
        self.worker_obj = None
        self.worker_thread = None
    
    def _log_message(self, message: str) -> None:
        """Aggiunge un messaggio al log.
        
        Args:
            message: Messaggio da aggiungere
        """
        self.log_area.append(message)
        # Scorre automaticamente verso il basso
        scrollbar = self.log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def closeEvent(self, event) -> None:
        """Gestisce la chiusura della finestra.
        
        Args:
            event: Evento di chiusura
        """
        # Interrompe l'elaborazione se in corso
        if self.worker_obj:
            self.worker_obj.stop()
        
        # Attende la terminazione del thread (con timeout)
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)
        
        event.accept()