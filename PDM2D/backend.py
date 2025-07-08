import os
from typing import List, Dict, Union, Optional
from config import ERROR_MESSAGES
from utils import validate_file_path

class FileSearcher:
    
    def __init__(self, cartelle_da_cercare: Optional[List[str]] = None):
        self.cartelle_da_cercare: List[str] = cartelle_da_cercare or []
    
    def aggiungi_cartella(self, cartella: str) -> None:
        if cartella and cartella not in self.cartelle_da_cercare:
            self.cartelle_da_cercare.append(cartella)
    
    def rimuovi_cartella(self, cartella: str) -> None:
        if cartella in self.cartelle_da_cercare:
            self.cartelle_da_cercare.remove(cartella)
    
    def cerca_file(self, prefisso: str) -> Dict[str, Union[str, List[str]]]:
        if not prefisso or not prefisso.strip():
            return {"errore": ERROR_MESSAGES['empty_prefix']}
        
        risultati: List[str] = []
        prefisso_pulito = prefisso.strip()
        
        for cartella in self.cartelle_da_cercare:
            risultati.extend(self._cerca_in_cartella(cartella, prefisso_pulito))
        
        return {"risultati": risultati}
    
    def _cerca_in_cartella(self, cartella: str, prefisso: str) -> List[str]:
        risultati: List[str] = []
        
        if not os.path.exists(cartella):
            return [ERROR_MESSAGES['folder_not_exists'].format(folder=cartella)]
        
        try:
            for root, dirs, files in os.walk(cartella):
                risultati.extend([os.path.join(root, file) for file in files if file.startswith(prefisso)])
        except PermissionError:
            risultati.append(ERROR_MESSAGES['permission_denied'].format(folder=cartella))
        except Exception as e:
            risultati.append(ERROR_MESSAGES['folder_access_error'].format(folder=cartella, error=str(e)))
        
        return risultati
    
    def valida_file(self, percorso: str) -> bool:
        is_valid, _ = validate_file_path(percorso)
        return is_valid
    
    def apri_file(self, percorso: str) -> Dict[str, Union[bool, str]]:
        try:
            if not percorso:
                return {"errore": ERROR_MESSAGES['file_path_missing']}
            
            is_valid, error_msg = validate_file_path(percorso)
            if not is_valid:
                return {"errore": error_msg or ERROR_MESSAGES['invalid_file']}
            
            os.startfile(percorso)
            return {"successo": True}
        except (FileNotFoundError, PermissionError, Exception) as e:
            error_messages = {
                FileNotFoundError: ERROR_MESSAGES['file_not_found'],
                PermissionError: ERROR_MESSAGES['file_permission_denied']
            }
            return {"errore": error_messages.get(type(e), ERROR_MESSAGES['file_open_error'].format(error=str(e)))}
    
    def get_cartelle(self) -> List[str]:
        return self.cartelle_da_cercare.copy()
    
    def set_cartelle(self, cartelle: Optional[List[str]]) -> None:
        self.cartelle_da_cercare = cartelle.copy() if cartelle else []