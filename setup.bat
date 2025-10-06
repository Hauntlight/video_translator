@echo off
:: Script di installazione per Video Translator su Windows
:: Eseguire questo file come amministratore se si riscontrano problemi con winget.

echo ==========================================================
echo  Script di Installazione per Video Translator (Windows)
echo ==========================================================
echo.
echo Questo script provera' a:
echo 1. Installare FFmpeg e RubberBand usando il gestore pacchetti winget.
echo 2. Creare un ambiente virtuale Python nella cartella 'venv'.
echo 3. Installare tutte le librerie Python necessarie.
echo.
pause

:: --- Fase 1: Verifica Prerequisiti ---
echo.
echo Verifico la presenza di Python 3.11...
python --version 2>NUL | find "3.11" >NUL
if %errorlevel% neq 0 (
    echo [ERRORE] Python 3.11 non trovato o non aggiunto al PATH.
    echo Per favore, installalo manualmente seguendo la guida e riesegui questo script.
    pause
    exit /b
)

echo Verifico la presenza di winget...
winget --version >NUL 2>NUL
if %errorlevel% neq 0 (
    echo [ERRORE] Gestore pacchetti 'winget' non trovato.
    echo E' necessario per installare FFmpeg e RubberBand.
    echo Aggiorna Windows o installa i pacchetti manualmente.
    pause
    exit /b
)
echo Prerequisiti di base trovati.
echo.

:: --- Fase 2: Installazione Dipendenze di Sistema ---
echo Installazione di FFmpeg (potrebbe richiedere conferma)...
winget install --id=Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
echo.
echo Installazione di RubberBand (potrebbe richiedere conferma)...
winget install --id=breakfast.rubberband -e --accept-source-agreements --accept-package-agreements
echo.
echo Dipendenze di sistema installate.
echo.

:: --- Fase 3: Configurazione Ambiente Python ---
echo Creazione dell'ambiente virtuale 'venv'...
if not exist venv (
    python -m venv venv
) else (
    echo Ambiente virtuale 'venv' gia' esistente.
)
echo.

echo Installazione delle librerie Python da requirements.txt...
echo Questa operazione potrebbe richiedere diversi minuti.
venv\Scripts\pip.exe install -r requirements.txt
echo.

:: --- Fase 4: Conclusione ---
echo ==========================================================
echo             INSTALLAZIONE COMPLETATA!
echo ==========================================================
echo.
echo Per avviare il programma:
echo 1. Attiva l'ambiente virtuale con il comando: venv\Scripts\activate
echo 2. Esegui il programma con il comando: python main.py
echo.
pause