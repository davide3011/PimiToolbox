"""Modulo per i componenti dell'interfaccia utente riutilizzabili.

Questo modulo contiene widget personalizzati e componenti UI che possono
essere riutilizzati in diverse parti dell'applicazione.
"""

from typing import List, Optional, Tuple
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QSpinBox, QCheckBox, QGroupBox, QPushButton, QFileDialog
)

from config import Settings


class DropArea(QLabel):
    """Area di trascinamento per file e cartelle.
    
    Permette agli utenti di trascinare file e cartelle nell'applicazione.
    """
    
    filesDropped = Signal(list)  # Emesso quando vengono rilasciati dei file
    
    def __init__(self, text: str = "\n\n Trascina qui immagini o cartelle \n\n"):
        """Inizializza l'area di drop.
        
        Args:
            text: Testo da mostrare nell'area di drop
        """
        super().__init__()
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self._setup_style()
    
    def _setup_style(self) -> None:
        """Configura lo stile dell'area di drop."""
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #7a7a7a;
                border-radius: 12px;
                padding: 30px;
                font-size: 16px;
                color: #444;
                background-color: #f9f9f9;
            }
            QLabel:hover {
                border-color: #4a90e2;
                background-color: #f0f8ff;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Gestisce l'evento di ingresso del trascinamento."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(self.styleSheet() + """
                QLabel {
                    border-color: #4a90e2;
                    background-color: #e6f3ff;
                }
            """)
    
    def dragLeaveEvent(self, event) -> None:
        """Gestisce l'evento di uscita del trascinamento."""
        self._setup_style()
    
    def dropEvent(self, event: QDropEvent) -> None:
        """Gestisce l'evento di rilascio dei file."""
        paths = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path:
                paths.append(path)
        
        if paths:
            self.filesDropped.emit(paths)
        
        self._setup_style()


class SettingsPanel(QGroupBox):
    """Pannello per la configurazione delle impostazioni di elaborazione."""
    
    def __init__(self, title: str = "Parametri di elaborazione"):
        """Inizializza il pannello delle impostazioni.
        
        Args:
            title: Titolo del gruppo di impostazioni
        """
        super().__init__(title)
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _create_widgets(self) -> None:
        """Crea tutti i widget del pannello."""
        # Dimensioni massime
        self.edit_maxsize = QLineEdit("1920x1080")
        self.edit_maxsize.setPlaceholderText("LxH o vuoto per disattivare")
        
        # Scala percentuale
        self.spin_scale = QSpinBox()
        self.spin_scale.setRange(1, 100)
        self.spin_scale.setValue(100)
        self.spin_scale.setSuffix("%")
        
        # Qualità JPEG
        self.spin_quality = QSpinBox()
        self.spin_quality.setRange(40, 95)
        self.spin_quality.setValue(85)
        
        # Ottimizzazione per peso
        self.chk_opt_weight = QCheckBox("Ottimizza per peso target")
        self.chk_opt_weight.setChecked(True)
        
        # Rapporto target
        self.edit_ratio = QLineEdit("0.40")
        self.edit_ratio.setFixedWidth(80)
        
        # JPEG progressivo
        self.chk_progressive = QCheckBox("JPEG progressivo")
        self.chk_progressive.setChecked(True)
        
        # Opzioni di sovrascrittura
        self.chk_overwrite = QCheckBox("Sovrascrivi originali")
        self.chk_backup = QCheckBox("Crea .bak")
        self.chk_backup.setEnabled(False)
    
    def _setup_layout(self) -> None:
        """Configura il layout del pannello."""
        main_layout = QVBoxLayout()
        
        # Prima riga: dimensioni, scala, qualità
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Max size:"))
        row1.addWidget(self.edit_maxsize)
        row1.addSpacing(10)
        row1.addWidget(QLabel("Scala:"))
        row1.addWidget(self.spin_scale)
        row1.addSpacing(10)
        row1.addWidget(QLabel("Qualità:"))
        row1.addWidget(self.spin_quality)
        
        # Seconda riga: ottimizzazioni e opzioni
        row2 = QHBoxLayout()
        row2.addWidget(self.chk_opt_weight)
        row2.addWidget(QLabel("Target ratio:"))
        row2.addWidget(self.edit_ratio)
        row2.addSpacing(20)
        row2.addWidget(self.chk_progressive)
        row2.addSpacing(20)
        row2.addWidget(self.chk_overwrite)
        row2.addWidget(self.chk_backup)
        
        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        self.setLayout(main_layout)
    
    def _connect_signals(self) -> None:
        """Connette i segnali dei widget."""
        self.chk_overwrite.toggled.connect(
            lambda checked: self.chk_backup.setEnabled(checked)
        )
    
    def get_settings(self) -> Settings:
        """Ottiene le impostazioni correnti dal pannello.
        
        Returns:
            Un'istanza di Settings con i valori correnti
        """
        return Settings(
            overwrite=self.chk_overwrite.isChecked(),
            make_backup=self.chk_backup.isChecked(),
            output_dir=None,  # Gestito separatamente
            scale_percent=self.spin_scale.value(),
            max_size=self._parse_maxsize(),
            quality_base=self.spin_quality.value(),
            optimize_for_weight=self.chk_opt_weight.isChecked(),
            target_size_ratio=float(self.edit_ratio.text().strip() or "0.4"),
            progressive=self.chk_progressive.isChecked()
        )
    
    def set_settings(self, settings: Settings) -> None:
        """Imposta i valori del pannello da un'istanza di Settings.
        
        Args:
            settings: Le impostazioni da applicare
        """
        self.chk_overwrite.setChecked(settings.overwrite)
        self.chk_backup.setChecked(settings.make_backup)
        self.spin_scale.setValue(settings.scale_percent)
        self.spin_quality.setValue(settings.quality_base)
        self.chk_opt_weight.setChecked(settings.optimize_for_weight)
        self.edit_ratio.setText(str(settings.target_size_ratio))
        self.chk_progressive.setChecked(settings.progressive)
        
        if settings.max_size:
            w, h = settings.max_size
            self.edit_maxsize.setText(f"{w}x{h}")
        else:
            self.edit_maxsize.setText("")
    
    def _parse_maxsize(self) -> Optional[Tuple[int, int]]:
        """Analizza il testo delle dimensioni massime.
        
        Returns:
            Tupla (larghezza, altezza) o None se non valido
        """
        text = self.edit_maxsize.text().strip()
        if not text:
            return None
        
        text = text.lower().replace(" ", "")
        if "x" in text:
            try:
                w, h = text.split("x", 1)
                return (max(1, int(w)), max(1, int(h)))
            except ValueError:
                return None
        
        return None


class OutputDirectorySelector(QWidget):
    """Widget per la selezione della cartella di output."""
    
    def __init__(self):
        """Inizializza il selettore di cartella."""
        super().__init__()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _create_widgets(self) -> None:
        """Crea i widget del selettore."""
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(
            "Cartella di output (vuoto = accanto all'originale)"
        )
        
        self.browse_button = QPushButton("Scegli cartella output…")
    
    def _setup_layout(self) -> None:
        """Configura il layout del widget."""
        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.browse_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def _connect_signals(self) -> None:
        """Connette i segnali dei widget."""
        self.browse_button.clicked.connect(self._browse_directory)
    
    def _browse_directory(self) -> None:
        """Apre il dialogo per la selezione della cartella."""
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Scegli cartella di output"
        )
        if directory:
            self.line_edit.setText(directory)
    
    def get_directory(self) -> Optional[str]:
        """Ottiene la cartella selezionata.
        
        Returns:
            Percorso della cartella o None se vuoto
        """
        text = self.line_edit.text().strip()
        return text if text else None
    
    def set_directory(self, directory: Optional[str]) -> None:
        """Imposta la cartella selezionata.
        
        Args:
            directory: Percorso della cartella o None
        """
        self.line_edit.setText(directory or "")


class FileSelector(QWidget):
    """Widget per la selezione di file immagine da archivio."""
    
    filesSelected = Signal(list)  # Emesso quando vengono selezionati dei file
    
    def __init__(self):
        """Inizializza il selettore di file."""
        super().__init__()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _create_widgets(self) -> None:
        """Crea i widget del selettore."""
        self.browse_button = QPushButton("Scegli immagini da archivio…")
        self.browse_button.setMinimumHeight(40)
    
    def _setup_layout(self) -> None:
        """Configura il layout del widget."""
        layout = QHBoxLayout()
        layout.addWidget(self.browse_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def _connect_signals(self) -> None:
        """Connette i segnali dei widget."""
        self.browse_button.clicked.connect(self._browse_files)
    
    def _browse_files(self) -> None:
        """Apre il dialogo per la selezione dei file immagine."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleziona immagini JPEG",
            "",
            "Immagini JPEG (*.jpg *.jpeg *.JPG *.JPEG);;Tutti i file (*.*)"
        )
        if files:
            self.filesSelected.emit(files)


class PresetButtons(QWidget):
    """Widget con pulsanti per preset di impostazioni predefinite."""
    
    presetSelected = Signal(Settings)  # Emesso quando viene selezionato un preset
    
    def __init__(self):
        """Inizializza i pulsanti dei preset."""
        super().__init__()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
    
    def _create_widgets(self) -> None:
        """Crea i pulsanti dei preset."""
        self.btn_default = QPushButton("Predefinito")
        self.btn_high_quality = QPushButton("Alta Qualità")
        self.btn_web_optimized = QPushButton("Ottimizzato Web")
        
        # Imposta le dimensioni dei pulsanti
        for btn in [self.btn_default, self.btn_high_quality, self.btn_web_optimized]:
            btn.setMaximumWidth(120)
    
    def _setup_layout(self) -> None:
        """Configura il layout dei pulsanti."""
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Preset:"))
        layout.addWidget(self.btn_default)
        layout.addWidget(self.btn_high_quality)
        layout.addWidget(self.btn_web_optimized)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def _connect_signals(self) -> None:
        """Connette i segnali dei pulsanti."""
        self.btn_default.clicked.connect(
            lambda: self.presetSelected.emit(Settings.create_default())
        )
        self.btn_high_quality.clicked.connect(
            lambda: self.presetSelected.emit(Settings.create_high_quality())
        )
        self.btn_web_optimized.clicked.connect(
            lambda: self.presetSelected.emit(Settings.create_web_optimized())
        )