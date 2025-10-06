import whisper
from src.io.logs import get_logger
import os
import yaml

logger = get_logger(__name__)

# Funzione per caricare il modello dinamicamente
def load_whisper_model():
    """Carica il modello Whisper specificato nel file di configurazione."""
    try:
        with open('config/settings.yaml', 'r') as f:
            model_name = yaml.safe_load(f)['stt']['whisper_model']
        logger.info(f"Caricamento del modello Whisper '{model_name}' in corso...")
        model = whisper.load_model(model_name)
        logger.info(f"Modello Whisper '{model_name}' caricato con successo.")
        return model
    except Exception as e:
        logger.error(f"Impossibile caricare il modello Whisper: {e}")
        return None

# Carica il modello una sola volta all'avvio
model = load_whisper_model()


def transcribe_audio_segments(audio_segments, temp_dir):
    """
    Trascrive una lista di segmenti audio.
    La durata nel timestamp viene salvata in millisecondi per maggiore precisione.
    """
    if not model:
        logger.error("Modello Whisper non disponibile. Trascrizione annullata.")
        return []

    transcribed_lines = []
    logger.info(f"Inizio trascrizione di {len(audio_segments)} segmenti...")

    for i, (chunk, start_ms, end_ms) in enumerate(audio_segments):
        chunk_path = os.path.join(temp_dir, f"chunk_{i}.wav")
        chunk.export(chunk_path, format="wav")

        try:
            result = model.transcribe(chunk_path, language="it")
            text = result["text"].strip()

            if text:

                # Calcola la durata direttamente in millisecondi
                duration_ms = end_ms - start_ms

                # Formattazione timestamp (rimane in hh:mm:ss per leggibilità)
                start_sec = start_ms / 1000
                hours, rem = divmod(start_sec, 3600)
                minutes, seconds = divmod(rem, 60)
                timestamp = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

                # Usa la durata in millisecondi nel formato finale
                formatted_line = f"[{timestamp}][{int(duration_ms)}] \"{text}\""
                transcribed_lines.append(formatted_line)
                logger.debug(f"Segmento {i} trascritto: {formatted_line}")
        except Exception as e:
            logger.error(f"Errore durante la trascrizione del chunk {i}: {e}")
        finally:
            if os.path.exists(chunk_path):
                os.remove(chunk_path)

    logger.info("Trascrizione completata.")
    return transcribed_lines