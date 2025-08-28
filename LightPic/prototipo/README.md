# LightPic (Prototipo)

## Introduzione

Spesso capita di dover inviare foto via email o caricarle su piattaforme online,
ma i file risultano troppo pesanti anche dopo una semplice compressione.
Questo prototipo nasce per risolvere il problema: ridurre drasticamente
la dimensione delle immagini senza compromettere eccessivamente la qualità visiva.
L'idea alla base è semplice: applicare una riduzione controllata della
risoluzione e una compressione intelligente (con ricerca automatica del
livello di qualità ottimale) così da ottenere file molto più leggeri,
ma comunque adatti alla visualizzazione.

## Stato del progetto

Questo programma è un MVP (Minimum Viable Product): un prototipo funzionante
che dimostra l'efficacia dell'approccio e offre già le funzioni principali:

- Ridimensionamento delle immagini mantenendo le proporzioni.

- Compressione in formato JPEG con ricerca automatica della qualità per raggiungere un obiettivo di peso.

- Possibilità di sovrascrivere i file originali o salvarne una copia ridotta.

- Supporto per JPEG progressivi (più efficienti in molti casi).

## Come funziona
Il programma elabora tutte le immagini (per default i file **.jpg** nella
cartella corrente) applicando due passaggi:

1. **Riduzione geometrica opzionale**: si può ridurre la dimensione in
percentuale oppure limitare la risoluzione massima (es. 1920x1080).

2. **Compressione ottimizzata**: se attiva, il programma cerca la qualità
JPEG migliore che porti la foto a un peso vicino a una percentuale 
dell'originale (es. 40%).

Grazie a questi due step, le immagini risultano molto più leggere,
pur mantenendo una qualità visiva accettabile.

## Utilizzo

### 1. Requisiti
- Python 3.x
- Libreria **Pillow** (`pip install pillow`)

### 2. Parametri da configurare
All'inizio del file `prototipo.py` sono presenti alcune variabili modificabili:
- `cartella`: cartella contenente le immagini.
- `pattern`: estensioni dei file da elaborare (es. `['*.jpg', '*.JPG']`).
- `overwrite`: `True` per sovrascrivere i file, `False` per creare una
nuova copia con suffisso `_ridotta`.
- `make_backup`: se `True`, salva una copia `.bak` prima di sovrascrivere.
- `scala_percent`: riduzione in percentuale (100 = nessuna riduzione).
- `max_size`: risoluzione massima (Larghezza x Altezza).
- `ottimizza_per_peso`: se `True`, cerca la qualità ottimale per ridurre la dimensione.
- `target_size_ratio`: obiettivo peso finale (es. `0.40` = 40% dell'originale).
- `progressive` >`True` salva JPEG progressivi.

### 3. Esecuzione
Posizionarsi nella cartella del programma ed eseguire:
```bash
python prototipo.py
```
Il programma cercherà le immagini corrispondenti al pattern e le elaborerà
secondo i parametri scelti.

### 4. Output
- Se `overwrite=True`, i file originali vengono sostituiti (con backup opzionale).
- Se `overwrite=False`, vengono generati nuovi file con suffisso `_ridotta`.
- A fine elaborazione, per ogni immagine viene mostrato un riepilogo con:
  - qualità utilizzata,
  - dimensione originale e finale,
  - percentuale di riduzione ottenuta.
  
## Esempio di risultato
```
[OK] foto1.jpg > foto1.jpg (q=78) | 3500.0KB > 1200.0KB (34.2%)
[OK] viaggio.jpg > foto2.jpg (q=82) | 4800.0KB > 1800.0KB (37.5%)
```

---








