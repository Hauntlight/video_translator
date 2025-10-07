# Video Translator 🎥 ➡️ 🌍 🔊

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Kivy-purple.svg)](https://kivy.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](base_doc.html)

Hai mai desiderato tradurre un video dall'italiano all'inglese, sincronizzando perfettamente l'audio, senza dover usare complessi software di video editing? **Video Translator** è la soluzione che fa per te.

Questo tool diventa il tuo assistente personale per la localizzazione di contenuti video. Sfruttando la potenza dell'intelligenza artificiale per la trascrizione e la traduzione, ti offre un'interfaccia semplice per revisionare il testo e genera un nuovo video con una traccia audio tradotta e perfettamente sincronizzata.


---

## ✨ Caratteristiche Principali

*   🗣️ **Trascrizione Automatica di Alta Qualità**: Utilizza i potenti modelli di **OpenAI Whisper** per convertire l'audio italiano in testo con grande accuratezza.
*   ✍️ **Editor Integrato per Revisione**: Nessuna trascrizione è perfetta. Correggi e perfeziona facilmente sia il testo originale che quello tradotto direttamente nell'app.
*   🌐 **Traduzione Istantanea**: Traduce il testo dall'italiano all'inglese (o altre lingue, vedi configurazione) frase per frase.
*   🎤 **Sintesi Vocale Sincronizzata**: Genera una nuova traccia audio nella lingua di destinazione. Grazie a un time-stretching di alta qualità, **l'audio tradotto dura esattamente quanto l'originale**, garantendo una sincronizzazione labiale perfetta.
*   🖥️ **Interfaccia Grafica Semplice**: Un'unica finestra ti guida attraverso i 3 passaggi chiave: Trascrivi, Traduci e Genera.
*   💾 **Ripresa Automatica del Lavoro**: Hai chiuso l'app a metà? Nessun problema. Ricaricando lo stesso video, il programma ripartirà dall'ultimo passaggio completato.
*   🔧 **Altamente Configurabile**: Modifica il modello AI, la sensibilità delle pause e le lingue tramite un semplice file di configurazione.

---

## 🚀 Installazione Rapida (Consigliata)

Abbiamo reso l'installazione un gioco da ragazzi. L'unico prerequisito è avere **Python 3.11** installato sul tuo sistema.

#### Per Windows:
1.  Fai **click con il tasto destro** sul file `setup.bat`.
2.  Seleziona **"Esegui come amministratore"**.
3.  Segui le istruzioni a schermo. Fatto!

#### Per macOS / Linux:
1.  Apri il Terminale nella cartella del progetto.
2.  Rendi lo script eseguibile: `chmod +x setup.sh`
3.  Eseguilo: `./setup.sh`

> Per un'installazione manuale, per risolvere problemi o per maggiori dettagli, consulta la nostra **[Guida Completa all'Installazione](advanced_doc.html)**.

---

## 🎯 Utilizzo

Una volta completata l'installazione, avviare il tool è semplicissimo.

1.  **Attiva l'ambiente virtuale**:
    *   Su Windows: `venv\Scripts\activate`
    *   Su macOS/Linux: `source venv/bin/activate`

2.  **Lancia l'applicazione**:
    ```bash
    python main.py
    ```
3.  **Segui il flusso di lavoro a 3 passaggi nell'app**:
    *   Seleziona il tuo video `.mp4`.
    *   Clicca su **"1. Trascrivi"** e attendi.
    *   Correggi il testo (opzionale) e clicca su **"2. Traduci"**.
    *   Correggi la traduzione (opzionale) e clicca su **"3. Genera Video"**.

Il tuo nuovo video tradotto ti aspetterà nella cartella `output`!

---

## ⚙️ Configurazione

Vuoi più accuratezza o tradurre in un'altra lingua? Apri il file `config/settings.yaml` e personalizza il tool a tuo piacimento!

```yaml
stt:
  # Cambia il modello per un'accuratezza maggiore (es. 'large') o maggiore velocità (es. 'base')
  whisper_model: 'medium'

languages:
  # Cambia le lingue di origine e destinazione
  source: 'it'
  target: 'en'

silence_detection:
  # Regola come il tool rileva le pause tra le frasi
  min_silence_len: 700
  silence_thresh: -40
```

---

## 🗺️ Roadmap e Sviluppi Futuri (Things to do)

Il progetto è in continua evoluzione. Ecco alcune delle aree su cui ci concentreremo in futuro:

*   **📦 Creazione di un Eseguibile Standalone**
    *   Creare un installer (`.exe` per Windows, `.app` per macOS) utilizzando strumenti come PyInstaller per permettere un'installazione "one-click" che non richieda la configurazione manuale di Python o delle altre dipendenze.

*   **🎨 Miglioramento della GUI (UI/UX)**
    *   Rinnovare il design per renderlo più moderno e intuitivo.
    *   Aggiungere un feedback visivo migliore durante le operazioni lunghe (es. una console di log in tempo reale nell'interfaccia).

*   **🧹 Refactoring e Qualità del Codice**
    *   Aumentare la robustezza del codice aggiungendo test unitari con `pytest`.
    *   Introdurre il type hinting per migliorare la manutenibilità.
    *   Ottimizzare le sezioni critiche per migliorare le performance con video di lunga durata.

---

## 🤝 Contribuire

Sei uno sviluppatore e vuoi dare una mano? I contributi sono i benvenuti! Sentiti libero di aprire una issue per discutere di nuove idee o di inviare una pull request per contribuire direttamente al codice.

---

## 📜 Licenza

Questo progetto è rilasciato sotto la Licenza MIT. Vedi il file `LICENSE` (se presente) per maggiori dettagli.
