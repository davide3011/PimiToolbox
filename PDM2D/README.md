# PDM2D

## Indice

1. **Descrizione**
2. **Funzionalità principali**
3. **Requisiti di sistema**
4. **Installazione**
5. **Configurazione variabili d'ambiente (`.env`)**
6. **Struttura del progetto**
7. **Come si usa**
8. **Compatibilità e sistema operativo supportato**
9. **Compilazione per sviluppatori**
10. **Licenza**
11. **Contatti e autore**

---

## Descrizione

**PDM2D** è un'applicazione desktop progettata per facilitare l'individuazione rapida di file di disegno tecnico 2D, con particolare attenzione all'integrazione con il software **ME10 Drafting**. L'utente può eseguire ricerche per prefisso del nome file all'interno di più cartelle configurabili e aprire i file trovati tramite un semplice gesto di drag & drop direttamente sull'interfaccia di ME10.

L'interfaccia grafica, sviluppata con PySide6 (Qt for Python), è ottimizzata per garantire reattività e chiarezza. Tutte le impostazioni sono centralizzate in un file `.env`, che rende l'app facilmente configurabile senza necessità di modificare il codice sorgente.

Questa soluzione è pensata per contesti industriali e uffici tecnici che gestiscono quotidianamente grandi quantità di disegni 2D archiviati in rete o su percorsi locali, riducendo i tempi di ricerca e migliorando la produttività operativa.

---

## Funzionalità principali

- **Ricerca per prefisso del nome file**: consente all'utente di individuare rapidamente i disegni tecnici inserendo solo le iniziali del nome.
- **Supporto per percorsi multipli**: permette la scansione simultanea di più directory, configurabili tramite file `.env`.
- **Apertura immediata dei file**: i file trovati possono essere aperti con un doppio clic o trascinati direttamente in ME10 Drafting. Sono supportati anche i documenti in formato PDF.
- **Interfaccia grafica reattiva e moderna**: costruita con PySide6, fornisce un'esperienza utente fluida e professionale.
- **Personalizzazione dell'aspetto**: layout, dimensioni e margini dell'interfaccia sono completamente configurabili senza modificare il codice.
- **Messaggistica integrata**: l'app fornisce messaggi informativi e di errore chiari, per guidare l'utente durante l'uso.
- **Adatta a contesti aziendali**: ottimizzata per ambienti multiutente e reti condivise, ideale per uffici tecnici e reparti progettazione.

---

## Requisiti di sistema
- **Sistema operativo**: Windows 10 o superiore, Debian 12
- **Python**: Versione 3.9 o superiore (solo per compilazione)
- **Dipendenze Python**:
  - [PySide6](https://pypi.org/project/PySide6/)
  - [python-dotenv](https://pypi.org/project/python-dotenv/)
- **ME10 Drafting installato**: necessario per aprire i file `.mi`
- **Permessi di rete**: accesso in lettura ai percorsi condivisi specificati in `.env`

---

## Installazione

### 1. Clona il repository
```bash
git clone https://github.com/davide3011/PimiToolbox.git
cd PDM2D
```

Consulta la sezione **Compilazione per sviluppatori** per creare l'eseguibile. Successivamente configura il file `.env`.

---

## Configurazione variabili d'ambiente (`.env`)

Il file `.env` consente di personalizzare il comportamento dell'applicazione senza modificare il codice sorgente. Va posizionato nella stessa cartella dell'eseguibile (search2D.exe) o del file main.py se si esegue da sorgente.

### 1. Percorsi di ricerca

```ini
CARTELLE_DA_CERCARE=C:\Progetti\ME10,Z:\ArchivioDisegni\Produzione,Y:\CAD\Disegni2024
```
Questa è la variabile principale, che specifica le directory in cui l'app deve cercare i file di disegno.

- I percorsi devono essere separati da virgole, **senza spazi**.
- Sono ammessi sia percorsi locali (`C:\...`) che di rete (`\\server\condivisione`).
- Tutti i percorsi indicati devono esistere ed essere accessibili dall'utente che esegue il programma.
---

### 2. Dimensioni e posizione della finestra
```ini
WINDOW_SCREEN_RATIO_WIDTH=0.25
WINDOW_SCREEN_RATIO_HEIGHT=0.7
WINDOW_POSITION_OFFSET_X=0
WINDOW_POSITION_OFFSET_Y=-0.05
``` 

Queste variabili determinano la larghezza e l'altezza della finestra rispetto allo schermo, oltre alla posizione (offset X e Y).

- I valori sono frazioni (es. `0.25` = 25% della larghezza dello schermo).
- Gli offset possono essere negativi o positivi per regolare la posizione sul desktop.

```ini
ICON_FILE=favicon.ico
```
Indica il file icona da usare come logo della finestra. Deve trovarsi nella stessa cartella del programma. Il file deve avere estensione `.ico`.

---

### 3. Layout

```ini
MAIN_SPACING=5
MAIN_MARGINS_TOP=18
MAIN_MARGINS_RIGHT=18
MAIN_MARGINS_BOTTOM=18
MAIN_MARGINS_LEFT=18
```

Personalizzano il layout interno della finestra: margini, spaziature e distanza tra i componenti dell'interfaccia. I valori sono in pixel.

```ini
FOOTER_MARGINS_TOP=10
FOOTER_MARGINS_RIGHT=10
FOOTER_MARGINS_BOTTOM=1
FOOTER_MARGINS_LEFT=10
```
Controllano la spaziatura attorno al footer in fondo alla finestra principale.

```ini
RESULTS_MIN_HEIGHT=450
SEARCH_SECTION_MIN_HEIGHT=150
RESULTS_SECTION_MIN_HEIGHT=300
```
Definiscono le altezze minime di alcune aree della GUI, utili per assicurare una buona visualizzazione anche su schermi piccoli.

### 4. Testi dell'interfaccia utente
```ini
SEARCH_PLACEHOLDER=es. 37202.60010
SEARCH_BUTTON=Cerca File
NO_RESULTS=Nessun file trovato con il prefisso specificato
FILE_OPENED=File aperto:
```
Queste voci ti permettono di personalizzare i messaggi e i testi visualizzati all'interno dell'applicazione, come etichette dei pulsanti e notifiche.

### 5. Messaggi di errore personalizzati
```ini
ERROR_EMPTY_PREFIX=Prefisso vuoto o non valido
ERROR_FOLDER_NOT_EXISTS=Attenzione: La cartella {folder} non esiste.
```
Puoi personalizzare anche i messaggi di errore visualizzati agli utenti. Le variabili tra parentesi graffe verranno sostituite dinamicamente.

---

Una volta completato e salvato correttamente, il file `.env` verrà caricato automaticamente all'avvio del programma.

Assicurati che:
- Ogni variabile sia su una riga separata.
- Non ci siano spazi tra nome, `=` e valore.
- Il file abbia nome `.env` (senza estensione aggiuntiva).

---

## Struttura del progetto

```
PDM2D/
├── backend.py         # Logica di ricerca e apertura file
├── config.py          # Variabili d'ambiente centralizzate
├── frontend.py        # Interfaccia grafica (GUI)
├── main.py            # Entry point dell'app
├── styles.py          # Stili grafici Qt
├── utils.py           # Utilità generali (icone, compatibilità)
├── favicon.ico        # Icona applicazione
├── .env               # File configurazione utente
└── requirements.txt   # Dipendenze Python
```

---

## Come si usa

1. **Avvia l'eseguibile** (es. `search2D.exe`)
2. **Inserisci un prefisso** (es. `37202.60010`)
3. **Visualizza e seleziona** tra i file elencati
4. **Apri il file** con doppio clic o trascinalo in ME10

Esempio:
```
Input: 37202.60010
Risultati:
- 37202.60010.mi
- 37202.60010.pdf
- 37202.60010_v1.mi
```

---

## Compatibilità e sistema operativo supportato

- ✅ Testato su Windows 10 e Windows 11 (architettura x64)
- ✅ Testato e funzionante su Debian 12 (Linux)
- ❌ Non testato su macOS/iOS

---

## Compilazione per sviluppatori

### 1. Installa PyInstaller
```bash
pip install pyinstaller
```

### 2. Crea l'eseguibile
```bash
pyinstaller --onefile --windowed --icon=favicon.ico --add-data "favicon.ico;." --name="search2D" main.py
```

Il file compilato sarà generato in `dist/search2D.exe`

---

## Licenza

Questo progetto è distribuito con licenza **MIT**. Per maggiori informazioni, consulta il file `LICENSE` incluso nel repository.

---

## Contatti e autore

**Autore**: Davide Grilli 
**Email**: [davide.grilli@outlook.com](mailto:davide.grilli@outlook.com)
