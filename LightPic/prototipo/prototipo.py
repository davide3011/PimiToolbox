from PIL import Image, ImageOps
import glob, os, io

# ====== PARAMETRI DA MODIFICARE PRIMA DI ESEGUIRE ======
cartella = "."                # cartella da processare
pattern = ["*.jpg", "*.JPG"]  # pattern file
overwrite = True              # True = sovrascrivi; False = crea _ridotta
make_backup = False           # True = salva .bak prima di sovrascrivere

# Riduzione geometrica (usa uno o entrambi)
scala_percent = 100           # es. 50 = riduci lati al 50%. 100 = nessun rescale
max_size = (1920, 1080)       # limite massimo (LxH). Metti None per disattivare, es. max_size = None

# Qualità/compressione
quality_base = 85             # qualità di partenza se non ottimizzi per peso
ottimizza_per_peso = True     # se True usa target_size_ratio con ricerca binaria qualità
target_size_ratio = 0.40      # obiettivo peso finale: 0.40 = ~40% del peso originale

progressive = True            # salva JPEG progressivo (di solito più efficiente)
# =======================================================

def resize_keep_ratio(img: Image.Image, scale_percent: int, max_size_tuple):
    # Corregge orientamento EXIF
    img = ImageOps.exif_transpose(img)

    # Scala percentuale
    if scale_percent not in (None, 100):
        w, h = img.size
        new_w = max(1, int(w * scale_percent / 100))
        new_h = max(1, int(h * scale_percent / 100))
        img = img.resize((new_w, new_h), Image.LANCZOS)

    # Limite LxH mantenendo proporzioni
    if max_size_tuple:
        img.thumbnail(max_size_tuple, Image.LANCZOS)

    return img

def jpeg_bytes(img: Image.Image, quality: int):
    # Garantisce RGB per JPEG
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True, progressive=progressive)
    return buf.getvalue()

def compress_to_ratio(img: Image.Image, original_bytes_len: int, target_ratio: float, q_min=40, q_max=95, max_iter=7):
    """
    Cerca una qualità JPEG che porti il peso vicino al rapporto desiderato.
    Restituisce (bytes_finali, qualità_usata)
    """
    target = int(original_bytes_len * target_ratio)
    best = None
    lo, hi = q_min, q_max

    for _ in range(max_iter):
        q = (lo + hi) // 2
        data = jpeg_bytes(img, q)
        size = len(data)

        # salva il migliore finora (il più vicino sotto target, o il più vicino in assoluto)
        if best is None or abs(len(best[0]) - target) > abs(size - target) or (size <= target < len(best[0])):
            best = (data, q)

        if size > target:
            # troppo pesante → abbassa qualità
            lo, hi = lo, q - 1
        else:
            # troppo leggero o giusto → prova qualità più alta per migliorare
            lo, hi = q + 1, hi

        if lo > hi:
            break

    return best

def process_file(path):
    try:
        # dimensione originale su disco
        original_size = os.path.getsize(path)

        img = Image.open(path)
        img = resize_keep_ratio(img, scala_percent, max_size)

        if ottimizza_per_peso:
            data, used_q = compress_to_ratio(img, original_size, target_size_ratio)
            out_bytes = data
            q_info = f"(q≈{used_q})"
        else:
            out_bytes = jpeg_bytes(img, quality_base)
            q_info = f"(q={quality_base})"

        new_size = len(out_bytes)
        ratio = new_size / original_size if original_size > 0 else 0

        # destinazione
        if overwrite:
            if make_backup:
                bak = path + ".bak"
                if not os.path.exists(bak):
                    with open(bak, "wb") as f:
                        f.write(open(path, "rb").read())
            out_path = path
        else:
            name, _ = os.path.splitext(path)
            out_path = f"{name}_ridotta.jpg"

        with open(out_path, "wb") as f:
            f.write(out_bytes)

        print(f"[OK] {os.path.basename(path)} → {os.path.basename(out_path)} "
              f"{q_info} | {original_size/1024:.1f}KB → {new_size/1024:.1f}KB ({ratio*100:.1f}%)")

    except Exception as e:
        print(f"[ERRORE] {path} -> {e}")

def main():
    files = []
    for pat in pattern:
        files.extend(glob.glob(os.path.join(cartella, pat)))
    if not files:
        print("Nessun file trovato.")
        return
    for f in files:
        process_file(f)

if __name__ == "__main__":
    main()
