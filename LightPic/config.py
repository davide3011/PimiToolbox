"""Modulo per la gestione delle configurazioni e impostazioni del programma.

Questo modulo definisce la classe Settings che contiene tutti i parametri
configurabili per l'elaborazione delle immagini.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Settings:
    """Classe che contiene tutte le impostazioni per l'elaborazione delle immagini.
    
    Attributes:
        overwrite: Se True, sovrascrive i file originali
        make_backup: Se True, crea un backup (.bak) prima di sovrascrivere
        output_dir: Cartella di destinazione (None = accanto all'originale)
        scale_percent: Percentuale di ridimensionamento (100 = dimensione originale)
        max_size: Dimensioni massime (larghezza, altezza) o None per disabilitare
        quality_base: Qualità JPEG di base (1-100)
        optimize_for_weight: Se True, ottimizza per raggiungere il rapporto target
        target_size_ratio: Rapporto di compressione target (es. 0.4 = 40%)
        progressive: Se True, crea JPEG progressivi
    """
    overwrite: bool = False
    make_backup: bool = False
    output_dir: Optional[str] = None
    scale_percent: int = 100
    max_size: Optional[Tuple[int, int]] = (1920, 1080)
    quality_base: int = 85
    optimize_for_weight: bool = True
    target_size_ratio: float = 0.40
    progressive: bool = True
    
    def __post_init__(self):
        """Validazione dei parametri dopo l'inizializzazione."""
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Valida i parametri delle impostazioni.
        
        Raises:
            ValueError: Se i parametri non sono validi
        """
        if not (1 <= self.scale_percent <= 100):
            raise ValueError("scale_percent deve essere tra 1 e 100")
        
        if not (1 <= self.quality_base <= 100):
            raise ValueError("quality_base deve essere tra 1 e 100")
        
        if not (0.01 <= self.target_size_ratio <= 1.0):
            raise ValueError("target_size_ratio deve essere tra 0.01 e 1.0")
        
        if self.max_size is not None:
            w, h = self.max_size
            if w <= 0 or h <= 0:
                raise ValueError("max_size deve avere valori positivi")
    
    @classmethod
    def create_default(cls) -> 'Settings':
        """Crea un'istanza con le impostazioni predefinite.
        
        Returns:
            Un'istanza di Settings con valori predefiniti
        """
        return cls()
    
    @classmethod
    def create_high_quality(cls) -> 'Settings':
        """Crea un'istanza ottimizzata per alta qualità.
        
        Returns:
            Un'istanza di Settings per alta qualità
        """
        return cls(
            quality_base=95,
            optimize_for_weight=False,
            target_size_ratio=0.8,
            max_size=(2560, 1440)
        )
    
    @classmethod
    def create_web_optimized(cls) -> 'Settings':
        """Crea un'istanza ottimizzata per il web.
        
        Returns:
            Un'istanza di Settings ottimizzata per il web
        """
        return cls(
            scale_percent=80,
            max_size=(1200, 800),
            quality_base=75,
            optimize_for_weight=True,
            target_size_ratio=0.3,
            progressive=True
        )
    
    def copy(self, **kwargs) -> 'Settings':
        """Crea una copia delle impostazioni con modifiche opzionali.
        
        Args:
            **kwargs: Parametri da modificare nella copia
            
        Returns:
            Una nuova istanza di Settings con le modifiche applicate
        """
        # Ottiene tutti i valori attuali
        current_values = {
            'overwrite': self.overwrite,
            'make_backup': self.make_backup,
            'output_dir': self.output_dir,
            'scale_percent': self.scale_percent,
            'max_size': self.max_size,
            'quality_base': self.quality_base,
            'optimize_for_weight': self.optimize_for_weight,
            'target_size_ratio': self.target_size_ratio,
            'progressive': self.progressive
        }
        
        # Applica le modifiche
        current_values.update(kwargs)
        
        return Settings(**current_values)
    
    def to_dict(self) -> dict:
        """Converte le impostazioni in un dizionario.
        
        Returns:
            Dizionario con tutte le impostazioni
        """
        return {
            'overwrite': self.overwrite,
            'make_backup': self.make_backup,
            'output_dir': self.output_dir,
            'scale_percent': self.scale_percent,
            'max_size': self.max_size,
            'quality_base': self.quality_base,
            'optimize_for_weight': self.optimize_for_weight,
            'target_size_ratio': self.target_size_ratio,
            'progressive': self.progressive
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Settings':
        """Crea un'istanza di Settings da un dizionario.
        
        Args:
            data: Dizionario con le impostazioni
            
        Returns:
            Un'istanza di Settings
        """
        return cls(**data)