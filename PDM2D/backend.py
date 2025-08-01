import os
from typing import List, Dict, Union, Optional
from config import ERROR_MESSAGES

class FileSearcher:
    
    def __init__(self, cartelle_da_cercare: Optional[List[str]] = None):
        self.cartelle_da_cercare: List[str] = cartelle_da_cercare or []
    

    def cerca_file(self, prefisso: str) -> Dict[str, Union[str, List[str]]]:
        if not prefisso or not prefisso.strip():
            return {"errore": ERROR_MESSAGES['empty_prefix']}
        
        risultati: List[str] = []
        prefisso_pulito = prefisso.strip()
        
        for cartella in self.cartelle_da_cercare:
            risultati.extend(self._cerca_in_cartella(cartella, prefisso_pulito))
        
        return {"risultati": risultati}
    
    def _cerca_in_cartella(self, cartella: str, prefisso: str) -> List[str]:
        if not os.path.exists(cartella):
            return [ERROR_MESSAGES['folder_not_exists'].format(folder=cartella)]
        
        try:
            risultati = []
            for root, _, files in os.walk(cartella):
                risultati.extend(os.path.join(root, file) for file in files if file.startswith(prefisso))
            return risultati
        except PermissionError:
            return [ERROR_MESSAGES['permission_denied'].format(folder=cartella)]
        except Exception as e:
            return [ERROR_MESSAGES['folder_access_error'].format(folder=cartella, error=str(e))]
    
    def apri_file(self, percorso: str) -> Dict[str, Union[bool, str]]:
        if not percorso:
            return {"errore": ERROR_MESSAGES['file_path_missing']}
        
        if not os.path.exists(percorso) or not os.path.isfile(percorso):
            return {"errore": ERROR_MESSAGES['invalid_file']}
        
        try:
            os.startfile(percorso)
            return {"successo": True}
        except FileNotFoundError:
            return {"errore": ERROR_MESSAGES['file_not_found']}
        except PermissionError:
            return {"errore": ERROR_MESSAGES['file_permission_denied']}
        except Exception as e:
            return {"errore": ERROR_MESSAGES['file_open_error'].format(error=str(e))}
    
    def get_cartelle(self) -> List[str]:
        return self.cartelle_da_cercare.copy()
    
    def set_cartelle(self, cartelle: Optional[List[str]]) -> None:
        self.cartelle_da_cercare = cartelle.copy() if cartelle else []