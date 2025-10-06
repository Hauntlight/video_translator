#!/bin/bash
# Script di installazione per Video Translator su macOS e Linux
# Rende lo script "stoppabile" al primo errore
set -e

echo "=========================================================="
echo " Script di Installazione per Video Translator (macOS/Linux)"
echo "=========================================================="
echo
echo "Questo script provera' a:"
echo "1. Installare FFmpeg e RubberBand usando il gestore pacchetti di sistema."
echo "2. Creare un ambiente virtuale Python nella cartella 'venv'."
echo "3. Installare tutte le librerie Python necessarie."
echo
read -p "Vuoi continuare? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]
then
    exit 1
fi

# --- Fase 1: Rilevamento OS e Installazione Dipendenze ---
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Rilevato macOS. Utilizzo di Homebrew."
    if ! command -v brew &> /dev/null; then
        echo "[ERRORE] Homebrew non trovato. Per favore, installalo da https://brew.sh e riesegui."
        exit 1
    fi
    echo "Installazione/aggiornamento di FFmpeg e RubberBand..."
    brew install ffmpeg rubberband

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux (Debian/Ubuntu)
    echo "Rilevato Linux. Utilizzo di APT."
    echo "Potrebbe essere richiesta la password di amministratore per installare i pacchetti."
    sudo apt update
    sudo apt install -y ffmpeg rubberband-cli python3.11-venv
else
    echo "[ERRORE] Sistema operativo non supportato da questo script."
    exit 1
fi

echo "Dipendenze di sistema installate."
echo

# --- Fase 2: Configurazione Ambiente Python ---
echo "Verifico la presenza di Python 3.11..."
if ! command -v python3.11 &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "[ERRORE] Python 3 non trovato. Per favore, installalo manualmente."
    exit 1
fi

echo "Creazione dell'ambiente virtuale 'venv'..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
else
    echo "Ambiente virtuale 'venv' gia' esistente."
fi
echo

echo "Installazione delle librerie Python da requirements.txt..."
echo "Questa operazione potrebbe richiedere diversi minuti."
# Chiama pip direttamente dall'ambiente virtuale per robustezza
venv/bin/pip install -r requirements.txt
echo

# --- Fase 3: Conclusione ---
echo "=========================================================="
echo "            INSTALLAZIONE COMPLETATA!"
echo "=========================================================="
echo
echo "Per avviare il programma:"
echo "1. Attiva l'ambiente virtuale con il comando: source venv/bin/activate"
echo "2. Esegui il programma con il comando: python main.py"
echo