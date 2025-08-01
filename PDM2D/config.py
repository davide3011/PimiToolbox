# Configurazione centralizzata dell'applicazione
# Tutte le costanti e configurazioni sono caricate dalle variabili di ambiente

import os
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()

def get_env_list(key):
    """Converte una stringa separata da virgole in una lista"""
    value = os.getenv(key, "")
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]

def get_env_float(key):
    """Converte una variabile di ambiente in float"""
    try:
        return float(os.getenv(key, "0"))
    except (ValueError, TypeError):
        return 0.0

def get_env_int(key):
    """Converte una variabile di ambiente in int"""
    try:
        return int(os.getenv(key, "0"))
    except (ValueError, TypeError):
        return 0

# === CONFIGURAZIONE PERCORSI ===
CARTELLE_DA_CERCARE = get_env_list('CARTELLE_DA_CERCARE')

# === INFORMAZIONI APPLICAZIONE ===
APP_NAME = "Ricerca Disegni 2D"
APP_VERSION = "2.0"
APP_ORGANIZATION = "CAD Tools"
APP_ID = f"CADTools.RicercaDisegni2D.{APP_VERSION}"
APP_AUTHOR = "Davide Grilli"

# === CONFIGURAZIONE FINESTRA ===
WINDOW_TITLE = APP_NAME
WINDOW_SCREEN_RATIO = (
    get_env_float('WINDOW_SCREEN_RATIO_WIDTH'),
    get_env_float('WINDOW_SCREEN_RATIO_HEIGHT')
)
WINDOW_POSITION_OFFSET_RATIO = (
    get_env_float('WINDOW_POSITION_OFFSET_X'),
    get_env_float('WINDOW_POSITION_OFFSET_Y')
)
ICON_FILE = os.getenv('ICON_FILE')

# === MESSAGGI INTERFACCIA ===
MESSAGES = {
    'search_placeholder': os.getenv('SEARCH_PLACEHOLDER'),
    'search_button': os.getenv('SEARCH_BUTTON'),
    'searching': os.getenv('SEARCHING'),
    'double_click_info': os.getenv('DOUBLE_CLICK_INFO'),
    'no_results': os.getenv('NO_RESULTS'),
    'error_prefix': os.getenv('ERROR_PREFIX'),
    'success_prefix': os.getenv('SUCCESS_PREFIX'),
    'file_opened': os.getenv('FILE_OPENED'),
    'input_missing': os.getenv('INPUT_MISSING'),
    'insert_prefix': os.getenv('INSERT_PREFIX'),
    'error_title': os.getenv('ERROR_TITLE')
}

# === TESTI INTERFACCIA ===
UI_TEXTS = {
    'title': os.getenv('UI_TITLE'),
    'subtitle': os.getenv('UI_SUBTITLE'),
    'prefix_label': os.getenv('PREFIX_LABEL'),
    'results_label': os.getenv('RESULTS_LABEL'),
    'footer': f"Creato da {APP_AUTHOR} - Versione {APP_VERSION}"
}

# === MESSAGGI ERRORE BACKEND ===
ERROR_MESSAGES = {
    'empty_prefix': os.getenv('ERROR_EMPTY_PREFIX'),
    'folder_not_exists': os.getenv('ERROR_FOLDER_NOT_EXISTS'),
    'permission_denied': os.getenv('ERROR_PERMISSION_DENIED'),
    'folder_access_error': os.getenv('ERROR_FOLDER_ACCESS'),
    'file_path_missing': os.getenv('ERROR_FILE_PATH_MISSING'),
    'invalid_file': os.getenv('ERROR_INVALID_FILE'),
    'file_not_found': os.getenv('ERROR_FILE_NOT_FOUND'),
    'file_permission_denied': os.getenv('ERROR_FILE_PERMISSION_DENIED'),
    'file_open_error': os.getenv('ERROR_FILE_OPEN')
}

# === CONFIGURAZIONE LAYOUT ===
LAYOUT_CONFIG = {
    'main_spacing': get_env_int('MAIN_SPACING'),
    'main_margins': (
        get_env_int('MAIN_MARGINS_TOP'),
        get_env_int('MAIN_MARGINS_RIGHT'),
        get_env_int('MAIN_MARGINS_BOTTOM'),
        get_env_int('MAIN_MARGINS_LEFT')
    ),
    'results_min_height': get_env_int('RESULTS_MIN_HEIGHT'),
    'footer_margins': (
        get_env_int('FOOTER_MARGINS_TOP'),
        get_env_int('FOOTER_MARGINS_RIGHT'),
        get_env_int('FOOTER_MARGINS_BOTTOM'),
        get_env_int('FOOTER_MARGINS_LEFT')
    ),
    'search_section_min_height': get_env_int('SEARCH_SECTION_MIN_HEIGHT'),
    'results_section_min_height': get_env_int('RESULTS_SECTION_MIN_HEIGHT')
}
