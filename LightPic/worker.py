"""Modulo per l'elaborazione delle immagini in background.

Questo modulo contiene la classe Worker che gestisce l'elaborazione
delle immagini in un thread separato per non bloccare l'interfaccia utente.
"""

import os
from typing import List, Iterator
from PIL import Image
from PySide6.QtCore import QObject, Signal

from config import Settings
from image_processing import (
    resize_keep_ratio, 
    jpeg_bytes, 
    compress_to_ratio, 
    is_supported_image
)


class ImageProcessor:
    """Classe per l'elaborazione di singole immagini.
    
    Separa la logica di elaborazione dalla gestione dei thread.
    """
    
    def __init__(self, settings: Settings):
        """Inizializza il processore con le impostazioni specificate.
        
        Args:
            settings: Configurazioni per l'elaborazione
        """
        self.settings = settings
    
    def process_image(self, file_path: str) -> dict:
        """Elabora una singola immagine.
        
        Args:
            file_path: Percorso del file immagine da elaborare
            
        Returns:
            Dizionario con i risultati dell'elaborazione:
            {
                'success': bool,
                'input_path': str,
                'output_path': str,
                'original_size': int,
                'new_size': int,
                'quality_info': str,
                'error': str (solo se success=False)
            }
        """
        try:
            original_size = os.path.getsize(file_path)
            
            # Carica e elabora l'immagine
            img = Image.open(file_path)
            img = resize_keep_ratio(
                img, 
                self.settings.scale_percent, 
                self.settings.max_size
            )
            
            # Determina la compressione da utilizzare
            if self.settings.optimize_for_weight:
                compression_result = compress_to_ratio(
                    img, 
                    original_size, 
                    self.settings.target_size_ratio, 
                    self.settings.progressive
                )
                
                if compression_result is None:
                    # Fallback alla qualità base
                    out_bytes = jpeg_bytes(
                        img, 
                        self.settings.quality_base, 
                        self.settings.progressive
                    )
                    quality_info = f"(q={self.settings.quality_base}, fallback)"
                else:
                    out_bytes, used_quality = compression_result
                    quality_info = f"(q≈{used_quality})"
            else:
                out_bytes = jpeg_bytes(
                    img, 
                    self.settings.quality_base, 
                    self.settings.progressive
                )
                quality_info = f"(q={self.settings.quality_base})"
            
            new_size = len(out_bytes)
            
            # Determina il percorso di output
            output_path = self._get_output_path(file_path)
            
            # Gestisce il backup se necessario
            if self.settings.overwrite and self.settings.make_backup:
                self._create_backup(file_path)
            
            # Crea la directory di output se non esiste
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Salva il file elaborato
            with open(output_path, "wb") as f:
                f.write(out_bytes)
            
            return {
                'success': True,
                'input_path': file_path,
                'output_path': output_path,
                'original_size': original_size,
                'new_size': new_size,
                'quality_info': quality_info
            }
            
        except Exception as e:
            return {
                'success': False,
                'input_path': file_path,
                'output_path': '',
                'original_size': 0,
                'new_size': 0,
                'quality_info': '',
                'error': str(e)
            }
    
    def _get_output_path(self, input_path: str) -> str:
        """Determina il percorso di output per un file.
        
        Args:
            input_path: Percorso del file di input
            
        Returns:
            Percorso del file di output
        """
        if self.settings.overwrite:
            return input_path
        else:
            base = os.path.basename(input_path)
            name, _ = os.path.splitext(base)
            
            if self.settings.output_dir:
                # Se è specificata una cartella di output diversa,
                # preserva la struttura delle directory relative
                output_dir = self._get_relative_output_dir(input_path)
            else:
                # Se non è specificata, usa la stessa cartella dell'input
                output_dir = os.path.dirname(input_path)
            
            return os.path.join(output_dir, f"{name}_ridotta.jpg")
    
    def _get_relative_output_dir(self, input_path: str) -> str:
        """Calcola la cartella di output preservando la struttura relativa.
        
        Quando si elaborano cartelle con sottocartelle, questa funzione
        preserva la struttura delle directory nella cartella di output.
        
        Args:
            input_path: Percorso del file di input
            
        Returns:
            Percorso della cartella di output per questo file
        """
        input_dir = os.path.dirname(input_path)
        
        # Trova la cartella radice comune tra tutti i percorsi di input
        common_root = self._find_common_root()
        
        if common_root and input_dir.startswith(common_root):
            # Calcola il percorso relativo dalla radice comune
            relative_path = os.path.relpath(input_dir, common_root)
            
            # Se il percorso relativo è ".", significa che siamo nella radice
            if relative_path == ".":
                return self.settings.output_dir
            else:
                return os.path.join(self.settings.output_dir, relative_path)
        else:
            # Fallback: usa direttamente la cartella di output
            return self.settings.output_dir
    
    def _find_common_root(self) -> str:
        """Trova la cartella radice comune tra tutti i percorsi di input.
        
        Returns:
            Percorso della cartella radice comune, o stringa vuota se non trovata
        """
        if not hasattr(self, '_common_root_cache'):
            # Ottiene tutti i percorsi delle cartelle dai file di input
            all_dirs = set()
            
            # Se abbiamo accesso ai percorsi originali, li usiamo
            # Altrimenti, usiamo solo la cartella del file corrente
            if hasattr(self, 'original_paths'):
                for path in self.original_paths:
                    if os.path.isdir(path):
                        all_dirs.add(os.path.abspath(path))
                    else:
                        all_dirs.add(os.path.dirname(os.path.abspath(path)))
            
            if len(all_dirs) > 1:
                # Trova il prefisso comune
                common_path = os.path.commonpath(list(all_dirs))
                self._common_root_cache = common_path
            elif len(all_dirs) == 1:
                self._common_root_cache = list(all_dirs)[0]
            else:
                self._common_root_cache = ""
        
        return self._common_root_cache
    
    def _create_backup(self, file_path: str) -> None:
        """Crea un backup del file originale.
        
        Args:
            file_path: Percorso del file da cui creare il backup
        """
        backup_path = file_path + ".bak"
        if not os.path.exists(backup_path):
            with open(backup_path, "wb") as backup_file:
                with open(file_path, "rb") as original_file:
                    backup_file.write(original_file.read())


class FileScanner:
    """Classe per la scansione e raccolta dei file immagine."""
    
    @staticmethod
    def scan_paths(paths: List[str]) -> List[str]:
        """Scansiona i percorsi forniti e raccoglie tutti i file immagine.
        
        Args:
            paths: Lista di percorsi (file o cartelle) da scansionare
            
        Returns:
            Lista di percorsi di file immagine trovati
        """
        files = []
        for path in paths:
            files.extend(FileScanner._scan_single_path(path))
        
        # Rimuove i duplicati mantenendo l'ordine
        return list(dict.fromkeys(files))
    
    @staticmethod
    def _scan_single_path(path: str) -> Iterator[str]:
        """Scansiona un singolo percorso per file immagine.
        
        Args:
            path: Percorso da scansionare (file o cartella)
            
        Yields:
            Percorsi dei file immagine trovati
        """
        if os.path.isdir(path):
            # Scansiona ricorsivamente la cartella
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if is_supported_image(file_path):
                        yield file_path
        elif os.path.isfile(path) and is_supported_image(path):
            # È un singolo file immagine
            yield path


class Worker(QObject):
    """Worker per l'elaborazione delle immagini in background.
    
    Questa classe gestisce l'elaborazione di più immagini in un thread separato,
    emettendo segnali per aggiornare l'interfaccia utente.
    """
    
    # Segnali per comunicare con l'interfaccia utente
    log = Signal(str)  # Messaggio di log
    progress = Signal(int, int)  # (corrente, totale)
    done = Signal()  # Elaborazione completata
    
    def __init__(self, paths: List[str], settings: Settings):
        """Inizializza il worker.
        
        Args:
            paths: Lista di percorsi da elaborare
            settings: Configurazioni per l'elaborazione
        """
        super().__init__()
        self.paths = paths
        self.settings = settings
        self._stop_requested = False
        self.processor = ImageProcessor(settings)
        # Passa i percorsi originali al processor per calcolare la struttura
        self.processor.original_paths = paths
    
    def stop(self) -> None:
        """Richiede l'interruzione dell'elaborazione."""
        self._stop_requested = True
    
    def run(self) -> None:
        """Esegue l'elaborazione delle immagini.
        
        Questo metodo dovrebbe essere chiamato in un thread separato.
        """
        try:
            # Scansiona i percorsi per trovare tutti i file immagine
            files = FileScanner.scan_paths(self.paths)
            
            if not files:
                self.log.emit("Nessuna immagine JPG/JPEG trovata.")
                self.done.emit()
                return
            
            total_files = len(files)
            self.log.emit(f"Trovati {total_files} file da elaborare.\n")
            
            # Elabora ogni file
            for i, file_path in enumerate(files, 1):
                if self._stop_requested:
                    self.log.emit("Elaborazione interrotta dall'utente.")
                    break
                
                # Aggiorna il progresso
                self.progress.emit(i, total_files)
                
                # Elabora il file
                result = self.processor.process_image(file_path)
                
                # Emette il risultato
                if result['success']:
                    ratio = (result['new_size'] / result['original_size'] 
                            if result['original_size'] > 0 else 0)
                    
                    message = (
                        f"[OK] {os.path.basename(result['input_path'])} → "
                        f"{os.path.basename(result['output_path'])} "
                        f"{result['quality_info']} | "
                        f"{result['original_size']/1024:.1f}KB → "
                        f"{result['new_size']/1024:.1f}KB ({ratio*100:.1f}%)"
                    )
                else:
                    message = f"[ERRORE] {result['input_path']} -> {result['error']}"
                
                self.log.emit(message)
        
        except Exception as e:
            self.log.emit(f"Errore generale durante l'elaborazione: {e}")
        
        finally:
            self.done.emit()