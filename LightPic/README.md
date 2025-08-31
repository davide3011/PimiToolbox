# LightPic - Riduttore JPEG

## 📌 Perché nasce questo programma?

Quando inviamo immagini tramite **email**, oppure le carichiamo su portali aziendali o
servizi come **WeTransfer**, spesso ci imbattiamo in **limiti di dimensione**.
Le foto scattate da smartphone o fotocamere possono pesare diversi MB, rendendo difficile condividerle velocemente.

**LightPic** nasce per risolvere questo problema: riduce le dimensioni delle immagini
**senza perdere troppa qualità**, rendendo più semplice condividerle, archiviarle o inviarle.

---

## 💻 Compatibilità
- ✅ **Windows 11** (testato)
- ✅ **Debian 12** (testato)
- ⚠️ **macOS** (non testato)

Il programma è scritto in **Python 3** e utilizza:
- **PySide6** → per l'interfaccia grafica
- **Pillow (PIL)** → per l'elaborazione delle immagini

Tutti i pacchetti richiesti sono in `requirements.txt`.

---

## 🚀 Come installare e avviare

### 1. Installazione dipendenze
Apri il terminale nella cartella del progetto e digita:
```bash
pip install -r requirements.txt
```

### 2. Avvio in modalità sviluppo
Puoi eseguire direttamente il programma con:
```bash
python main.py
```

Si aprirà la finestra di **LightPic** pronta all’uso.

---

## 📦 Come creare l'eseguibile

Per distribuire il programma senza richiedere Python installato, si usa **PyInstaller**.

1. Installa PyInstaller:
```bash
pip install pyinstaller
```

2. Crea l'eseguibile:
```bash
pyinstaller --noconsole --onefile --windowed --icon=favicon.ico \
    --add-data "favicon.ico;." --name LightPic main.py
```

3. Troverai il file eseguibile in:
   - `dist/LightPic.exe` su Windows
   - `dist/LightPic` su Linux

### 🔎 Dettagli delle opzioni
- `--noconsole` → evita che compaia la console nera dietro l’app
- `--onefile` → crea un singolo file eseguibile
- `--windowed` → segnala che è un’app grafica
- `--icon=favicon.ico` → usa l’icona personalizzata
- `--add-data` → include i file extra (es. icona) nel pacchetto
- `--name` → rinomina l'eseguibile
---

## 🔧 Come modificare il programma (per sviluppatori)

Se vuoi personalizzare o migliorare LightPic:

- `config.py` → contiene i **parametri di configurazione** (es. qualità JPEG, ridimensionamento, compressione progressiva)
- `ui_components.py` → contiene i **widget grafici** riutilizzabili (pannelli, pulsanti, campi di testo)
- `main_window.py` → definisce la **finestra principale** e l’organizzazione dell’interfaccia
- `image_processing.py` → gestisce le **funzioni di ridimensionamento e compressione**
- `worker.py` → elabora le immagini in **background**, così l’interfaccia non si blocca

Per avviare il programma dopo una modifica:
```bash
python main.py
```

---

## 📖 Guida passo-passo all’uso

### 1. Avvia il programma
Apri l’eseguibile. Comparirà una finestra con titolo **LightPic**.

### 2. Carica le immagini
Hai due possibilità:
- **Trascinare** immagini o cartelle nell’area centrale
- Cliccare su **Scegli immagini da archivio…**

### 3. Imposta le preferenze
Nella sezione **Parametri di elaborazione** puoi:
- **Max size** → ridimensionare a una certa risoluzione massima (es. 1920x1080)
- **Scala %** → ridurre la dimensione in percentuale
- **Qualità JPEG** → regolare la qualità (da 40 a 95)
- **Ottimizza per peso target** → attiva un algoritmo che cerca di raggiungere la dimensione desiderata
- **JPEG progressivo** → genera immagini che si caricano gradualmente sul web
- **Sovrascrivi originali** → salva al posto del file originale (opzione avanzata)

Puoi anche usare i **preset**:
- 🔹 *Predefinito* → equilibrio qualità/dimensione
- 🔹 *Alta Qualità* → meno compressione, più qualità
- 🔹 *Ottimizzato Web* → dimensioni ridotte per caricamento online

### 4. Seleziona la cartella di output
- Puoi scegliere una cartella di destinazione
- Se lasci vuoto, i file ridotti vengono salvati accanto agli originali

### 5. Avvia l’elaborazione
- Premi **Elabora**
- Segui i messaggi nel **Log di elaborazione**
- Guarda la **barra di progresso** mentre le immagini vengono compresse

### 6. Interrompi se serve
- Con il tasto **Interrompi** puoi fermare il processo in corso

### 7. Controlla i file prodotti
- Le immagini ridotte hanno suffisso `_ridotta.jpg` se non hai scelto di sovrascrivere
- Puoi confrontare le dimensioni nel log (es. *5000 KB → 1200 KB (24%)*).

---

## 📜 Licenza
Questo progetto è rilasciato sotto licenza **MIT**. Puoi usarlo liberamente, modificarlo e ridistribuirlo.

---
