# Configurazione centralizzata dell'applicazione
# Tutte le costanti e configurazioni sono definite qui per evitare duplicazioni

# === CONFIGURAZIONE PERCORSI ===
CARTELLE_DA_CERCARE = [
    # Inserire qui i percorsi delle cartelle da cercare:
    # r"C:\Percorso\Alla\Cartella1",
    # r"C:\Percorso\Alla\Cartella2",
]

# === INFORMAZIONI APPLICAZIONE ===
APP_NAME = "Ricerca Disegni 3D"
APP_VERSION = "1.0"
APP_ORGANIZATION = "CAD Tools"
APP_ID = f"CADTools.RicercaDisegni3D.{APP_VERSION}"
APP_AUTHOR = "Davide Grilli"

# === CONFIGURAZIONE FINESTRA ===
WINDOW_TITLE = APP_NAME
WINDOW_SCREEN_RATIO = (0.5, 0.7)  # Percentuale schermo (larghezza, altezza)
WINDOW_POSITION_OFFSET_RATIO = (0, -0.05)  # Offset dinamico come percentuale dello schermo
ICON_FILE = "favicon.ico"

# === MESSAGGI INTERFACCIA ===
MESSAGES = {
    'search_placeholder': "es. 37202-60010",
    'search_button': "Cerca File",
    'searching': "Ricerca in corso...",
    'double_click_info': "Doppio click su un risultato per aprire il file",
    'no_results': "Nessun file trovato con il prefisso specificato",
    'error_prefix': "Errore durante la ricerca",
    'success_prefix': "Trovati",
    'file_opened': "File aperto:",
    'input_missing': "Input mancante",
    'insert_prefix': "Inserisci un prefisso per la ricerca.",
    'error_title': "Errore"
}

# === TESTI INTERFACCIA ===
UI_TEXTS = {
    'title': APP_NAME,
    'subtitle': "Trova rapidamente i tuoi file di progettazione",
    'prefix_label': "Inserisci il prefisso del file:",
    'results_label': "Risultati della ricerca:",
    'footer': f"Creato da {APP_AUTHOR} - Versione {APP_VERSION}"
}

# === MESSAGGI ERRORE BACKEND ===
ERROR_MESSAGES = {
    'empty_prefix': "Prefisso vuoto o non valido",
    'folder_not_exists': "Attenzione: La cartella {folder} non esiste.",
    'permission_denied': "Errore: Accesso negato alla cartella {folder}",
    'folder_access_error': "Errore nell'accesso alla cartella {folder}: {error}",
    'file_path_missing': "Percorso file non specificato",
    'invalid_file': "Il percorso non esiste o non è un file valido",
    'file_not_found': "File non trovato",
    'file_permission_denied': "Accesso negato al file",
    'file_open_error': "Impossibile aprire il file: {error}"
}

# === CONFIGURAZIONE LAYOUT ===
LAYOUT_CONFIG = {
    'main_spacing': 15,
    'main_margins': (20, 20, 20, 20),
    'results_min_height': 300,
    'footer_margins': (10, 5, 10, 5)
}

# Note per CARTELLE_DA_CERCARE:
# - Utilizzare percorsi assoluti (completi)
# - Per percorsi di rete usare la notazione UNC (\\server\cartella)
# - Assicurarsi di avere i permessi di lettura per tutte le cartelle
# - Ogni percorso deve terminare con una virgola (tranne l'ultimo)
