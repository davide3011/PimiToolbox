# Ricerca Disegni 3D

## Descrizione

Questa applicazione nasce con l'esigenza di **abbattere i tempi nella ricerca del file all'interno del server**. È uno strumento di ricerca rapida per file di progettazione CAD che permette di trovare velocemente i file utilizzando un prefisso del nome.

## Caratteristiche Principali

- **Ricerca rapida**: Trova file utilizzando un prefisso del nome
- **Interfaccia grafica moderna**: Sviluppata con PySide6 (Qt6)
- **Ricerca multi-cartella**: Supporta la ricerca in più directory contemporaneamente
- **Apertura diretta**: Doppio click sui risultati per aprire i file
- **Ricerca asincrona**: L'interfaccia rimane reattiva durante la ricerca
- **Gestione errori**: Messaggi informativi per problemi di accesso o permessi

## Configurazione

### Impostazione delle Cartelle di Ricerca

Per configurare l'applicazione, modifica il file `config.py` e inserisci la **cartella più grande** all'interno della quale il programma deve cercare i file:

```python
CARTELLE_DA_CERCARE = [
    # Inserire qui i percorsi delle cartelle da cercare:
    r"C:\Percorso\Alla\Cartella1",
    r"C:\Percorso\Alla\Cartella2"
]
```

### Note per la Configurazione

- Utilizzare **percorsi assoluti** (completi)
- Per percorsi di rete usare la notazione UNC (`\\server\cartella`)
- Assicurarsi di avere i **permessi di lettura** per tutte le cartelle
- Ogni percorso deve terminare con una virgola (tranne l'ultimo)

### Altre Configurazioni Disponibili

Nel file `config.py` è possibile personalizzare:
- Nome e versione dell'applicazione
- Dimensioni e posizione della finestra
- Messaggi dell'interfaccia utente
- Configurazioni di layout

## Informazioni Tecniche

### Architettura

L'applicazione è strutturata in moduli separati per una migliore manutenibilità:

- **`main.py`**: Punto di ingresso dell'applicazione
- **`frontend.py`**: Interfaccia grafica utente (GUI)
- **`backend.py`**: Logica di ricerca dei file
- **`config.py`**: Configurazioni centralizzate
- **`styles.py`**: Stili CSS per l'interfaccia
- **`utils.py`**: Funzioni di utilità

### Dipendenze

- **Python 3.11+**: Linguaggio di programmazione
- **PySide6**: Framework per l'interfaccia grafica (Qt6)
- **Threading**: Per ricerche asincrone non bloccanti
- **OS Module**: Per l'accesso al filesystem

### Funzionalità Tecniche

- **Ricerca ricorsiva**: Esplora tutte le sottocartelle
- **Gestione thread**: Ricerca in background per mantenere l'UI reattiva
- **Validazione percorsi**: Controllo dell'esistenza e accessibilità dei file
- **Gestione eccezioni**: Handling robusto degli errori di sistema
- **Icona personalizzata**: Supporto per favicon.ico

## Installazione e Utilizzo

### Prerequisiti

- Python 3.11 o superiore
- Sistema operativo Windows (per `os.startfile()`)

### Installazione Dipendenze

```bash
pip install -r requirements.txt
```

### Esecuzione

```bash
python main.py
```

## Compilazione per Eseguibile

Per creare un eseguibile dell'applicazione:

### 1. Installa PyInstaller

```bash
pip install pyinstaller
```

### 2. Crea l'Eseguibile

**Comando semplice (raccomandato):**

```bash
pyinstaller --onefile --windowed --icon=favicon.ico --name="search3D" main.py
```

### 3. Risultato

Troverai l'eseguibile in:
- **`dist/search3D.exe`** - Il file finale da distribuire

### 4. Distribuzione

Per distribuire l'applicazione:
1. Copia l'eseguibile `RicercaDisegni3D.exe`
2. Assicurati che il file `favicon.ico` sia nella stessa directory (se necessario)
3. L'eseguibile è standalone e non richiede Python installato

## Utilizzo dell'Applicazione

1. **Avvia** l'applicazione
2. **Inserisci** il prefisso del file da cercare (es. "37202-60010")
3. **Clicca** "Cerca File" o premi Invio
4. **Visualizza** i risultati nella lista
5. **Doppio click** su un risultato per aprire il file

## Autore

**Davide Grilli** 
Versione 1.0

---

*Questa applicazione è stata progettata per ottimizzare i flussi di lavoro CAD riducendo significativamente i tempi di ricerca dei file di progettazione.*