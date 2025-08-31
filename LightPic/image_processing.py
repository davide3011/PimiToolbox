"""Modulo per l'elaborazione e compressione delle immagini JPEG.

Questo modulo fornisce funzionalità per:
- Ridimensionamento delle immagini mantenendo le proporzioni
- Compressione JPEG con controllo della qualità
- Ottimizzazione automatica per raggiungere un rapporto di compressione target
"""

import io
from typing import Optional, Tuple
from PIL import Image, ImageOps


def resize_keep_ratio(img: Image.Image, scale_percent: int, max_size_tuple: Optional[Tuple[int, int]]) -> Image.Image:
    """Ridimensiona un'immagine mantenendo le proporzioni.
    
    Args:
        img: L'immagine PIL da ridimensionare
        scale_percent: Percentuale di scala (100 = dimensione originale)
        max_size_tuple: Dimensioni massime (larghezza, altezza) o None per disabilitare
        
    Returns:
        L'immagine ridimensionata
    """
    # Corregge l'orientamento basato sui dati EXIF
    img = ImageOps.exif_transpose(img)
    
    # Applica la scala percentuale se diversa da 100%
    if scale_percent not in (None, 100):
        w, h = img.size
        new_w = max(1, int(w * scale_percent / 100))
        new_h = max(1, int(h * scale_percent / 100))
        img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Applica le dimensioni massime se specificate
    if max_size_tuple:
        img.thumbnail(max_size_tuple, Image.LANCZOS)
    
    return img


def jpeg_bytes(img: Image.Image, quality: int, progressive: bool) -> bytes:
    """Converte un'immagine PIL in bytes JPEG.
    
    Args:
        img: L'immagine PIL da convertire
        quality: Qualità JPEG (1-100)
        progressive: Se True, crea un JPEG progressivo
        
    Returns:
        I bytes dell'immagine JPEG
    """
    # Converte in RGB se necessario (per RGBA o P mode)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    buf = io.BytesIO()
    img.save(
        buf, 
        format="JPEG", 
        quality=int(quality), 
        optimize=True, 
        progressive=progressive
    )
    return buf.getvalue()


def compress_to_ratio(img: Image.Image, 
                     original_bytes_len: int, 
                     target_ratio: float,
                     progressive: bool, 
                     q_min: int = 40, 
                     q_max: int = 95, 
                     max_iter: int = 7) -> Optional[Tuple[bytes, int]]:
    """Comprime un'immagine per raggiungere un rapporto di dimensione target.
    
    Utilizza una ricerca binaria per trovare la qualità JPEG ottimale che
    produce una dimensione file il più vicina possibile al target.
    
    Args:
        img: L'immagine PIL da comprimere
        original_bytes_len: Dimensione originale del file in bytes
        target_ratio: Rapporto target (es. 0.4 per 40% della dimensione originale)
        progressive: Se True, crea un JPEG progressivo
        q_min: Qualità minima da testare
        q_max: Qualità massima da testare
        max_iter: Numero massimo di iterazioni per la ricerca binaria
        
    Returns:
        Tupla (bytes_compressi, qualità_usata) o None se fallisce
    """
    target = int(original_bytes_len * target_ratio)
    best = None
    lo, hi = q_min, q_max
    
    for _ in range(max_iter):
        q = (lo + hi) // 2
        data = jpeg_bytes(img, q, progressive)
        size = len(data)
        
        # Aggiorna il miglior risultato se questo è più vicino al target
        if (best is None or 
            abs(len(best[0]) - target) > abs(size - target) or 
            (size <= target < len(best[0]))):
            best = (data, q)
        
        # Aggiusta i limiti per la ricerca binaria
        if size > target:
            hi = q - 1
        else:
            lo = q + 1
            
        if lo > hi:
            break
    
    return best


# Costanti per le estensioni supportate
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".JPG", ".JPEG"}


def is_supported_image(file_path: str) -> bool:
    """Verifica se un file ha un'estensione supportata.
    
    Args:
        file_path: Percorso del file da verificare
        
    Returns:
        True se l'estensione è supportata, False altrimenti
    """
    import os
    return os.path.splitext(file_path)[1] in SUPPORTED_EXTENSIONS