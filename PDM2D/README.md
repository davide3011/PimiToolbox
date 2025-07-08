# Ricerca Disegni 2D

## Descrizione

Applicazione desktop per la ricerca rapida di file di progettazione 2D, sviluppata specificamente per essere utilizzata in affiancamento al software **ME10 Drafting**. Il programma permette di trovare velocemente i disegni tecnici attraverso la ricerca per prefisso del nome file e include una funzionalità di drag & drop che consente di trascinare direttamente i file sulla finestra di ME10 per aprirli e visualizzarli.

## Caratteristiche Principali

### Ricerca Intelligente
- **Ricerca per prefisso**: Trova rapidamente i file inserendo solo l'inizio del nome (es. "37202.60010")
- **Ricerca multi-cartella**: Scansiona automaticamente tutte le cartelle configurate
- **Ricerca ricorsiva**: Esplora anche le sottocartelle
- **Gestione errori**: Segnala cartelle inaccessibili o problemi di permessi

### Interazione Avanzata
- **Doppio click**: Apri direttamente i file con l'applicazione predefinita
- **Drag & Drop**: Trascina i file dalla lista dei risultati verso altre applicazioni
- **Interfaccia reattiva**: Ricerca in background senza bloccare l'interfaccia

### Interfaccia Moderna
- **Design pulito**: Interfaccia grafica moderna e intuitiva
- **Responsive**: Si adatta automaticamente alle dimensioni dello schermo
- **Feedback visivo**: Indicatori di stato durante la ricerca
- **Tooltips informativi**: Mostra il percorso completo dei file

### Configurazione Flessibile
- **Cartelle personalizzabili**: Configura facilmente i percorsi di ricerca
- **Supporto percorsi di rete**: Compatibile con cartelle condivise (UNC)
- **Gestione permessi**: Rileva e segnala problemi di accesso

## Integrazione con ME10 Drafting

Questo strumento è stato progettato per complementare il workflow di **ME10 Drafting**, permettendo di:
- Localizzare rapidamente i disegni tecnici durante la progettazione
- Trascinare i file direttamente nell'ambiente ME10
- Mantenere un flusso di lavoro fluido senza dover navigare manualmente nelle cartelle
- Accedere velocemente ai file di riferimento durante la modellazione

## Requisiti di Sistema

- **Sistema Operativo**: Windows 10/11
- **Python**: 3.8 o superiore
- **Dipendenze**: PySide6 >= 6.5.0

## Installazione

1. **Clona o scarica il progetto**

2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura i percorsi di ricerca**:
   Modifica il file `config.py` e aggiorna la lista `CARTELLE_DA_CERCARE` con i tuoi percorsi:
   ```python
   CARTELLE_DA_CERCARE = [
       r"C:\Progetti\Disegni",
       # Aggiungi altri percorsi...
   ]
   ```

4. **Avvia l'applicazione**:
   ```bash
   python main.py
   ```

## Utilizzo

1. **Avvia il programma** eseguendo `main.py`
2. **Inserisci il prefisso** del file che stai cercando (es. "37202.60010")
3. **Clicca "Cerca File"** o premi Invio
4. **Interagisci con i risultati**:
   - **Doppio click** per aprire il file
   - **Trascina** il file verso altre applicazioni (ME10, Esplora file, ecc.)

## Struttura del Progetto

```
PDM3D/
├── main.py            # Entry point dell'applicazione
├── frontend.py        # Interfaccia grafica (GUI)
├── backend.py         # Logica di ricerca file
├── config.py          # Configurazioni e costanti
├── styles.py          # Stili CSS per l'interfaccia
├── utils.py           # Funzioni di utilità
├── requirements.txt   # Dipendenze Python
├── favicon.ico        # Icona dell'applicazione
└── README.md          # Questo file
```

## Componenti Principali

### Frontend (`frontend.py`)
- **SearchGUI**: Finestra principale dell'applicazione
- **DragDropListWidget**: Lista personalizzata con supporto drag & drop
- **SearchThread**: Thread per ricerca asincrona

### Backend (`backend.py`)
- **FileSearcher**: Motore di ricerca file
- Gestione percorsi e validazione file
- Apertura file con applicazioni predefinite

### Configurazione (`config.py`)
- Percorsi di ricerca
- Messaggi dell'interfaccia
- Impostazioni finestra e layout

## Personalizzazione

### Aggiungere Nuove Cartelle
Modifica `CARTELLE_DA_CERCARE` in `config.py`:
```python
CARTELLE_DA_CERCARE = [
    r"C:\Percorso\Alla\Cartella1",
    r"C:\Percorso\Alla\Cartella2"
    # Aggiungi altre cartelle qui...
]
```

### Modificare l'Interfaccia
Personalizza i colori e lo stile modificando `styles.py`.

### Cambiare i Messaggi
Modifica i testi in `config.py` nella sezione `MESSAGES` e `UI_TEXTS`.

## Risoluzione Problemi

### Cartelle Non Accessibili
- Verifica i permessi di lettura
- Per cartelle di rete, assicurati di essere connesso
- Controlla che i percorsi siano corretti

### File Non Si Aprono
- Verifica che esista un'applicazione predefinita per il tipo di file
- Controlla i permessi del file
- Assicurati che il file non sia in uso da altre applicazioni

## Compilazione per Eseguibile

Per creare un eseguibile dell'applicazione:

### 1. Installa PyInstaller
```bash
pip install pyinstaller
```

### 2. Crea l'Eseguibile
```bash
pyinstaller --onefile --windowed --icon=favicon.ico --add-data "favicon.ico;." --name="search2D" main.py
```

### 3. Distribuzione
Troverai l'eseguibile in `dist/search2D.exe` pronto per la distribuzione.

## Sviluppo

### Architettura
- **Pattern MVC**: Separazione tra logica (backend), interfaccia (frontend) e configurazione
- **Threading**: Ricerca asincrona per mantenere l'interfaccia reattiva
- **Modularità**: Componenti separati e riutilizzabili

### Estensioni Future
- Ricerca per contenuto file
- Filtri avanzati (data, dimensione, tipo)
- Cronologia ricerche
- Integrazione con sistemi PLM

## Autore

**Davide Grilli**

---

*Questo strumento è stato sviluppato per ottimizzare il workflow di progettazione in ambiente ME10 Drafting, fornendo un accesso rapido e intuitivo ai file di progetto 2D.*