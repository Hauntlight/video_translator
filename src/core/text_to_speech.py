from gtts import gTTS
from pydub import AudioSegment
import os
import yaml
from src.io.logs import get_logger
import pyrubberband as pyrb
import soundfile as sf



logger = get_logger(__name__)


def text_to_speech(text, lang, output_path):
    """
    Converts a string of text into a high-quality WAV audio file.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        # Save as temporary mp3 first
        temp_mp3_path = output_path.replace('.wav', '.mp3')
        tts.save(temp_mp3_path)

        # Convert to WAV for high-quality processing
        AudioSegment.from_mp3(temp_mp3_path).export(output_path, format="wav")
        os.remove(temp_mp3_path)

        logger.debug(f"Testo '{text[:20]}...' convertito in audio a {output_path}")
        return True
    except Exception as e:
        logger.error(f"Errore durante la generazione TTS per '{text[:20]}...': {e}")
        return False


def adjust_audio_speed(audio_path, target_duration_ms):
    """
    Regola la velocità di un file audio usando pyrubberband per alta qualità.
    """
    try:
        original_duration_ms = len(AudioSegment.from_wav(audio_path))

        if original_duration_ms == 0 or target_duration_ms == 0:
            logger.warning(f"Durata originale o target è zero per {audio_path}. Salto l'adattamento.")
            return

        # Il fattore per pyrubberband è l'inverso di quello per pydub.
        # speed > 1.0 -> Rallenta
        # speed < 1.0 -> Velocizza
        stretch_ratio = target_duration_ms / float(original_duration_ms)

        if abs(stretch_ratio - 1.0) > 0.01:
            logger.info(
                f"Adattamento velocità per {os.path.basename(audio_path)}: da {original_duration_ms}ms a {target_duration_ms}ms (fattore {stretch_ratio:.2f}x)")

            # 1. Carica il file audio con soundfile
            y, sr = sf.read(audio_path)

            # 2. Esegui il time-stretch con pyrubberband
            stretched_audio = pyrb.time_stretch(y, sr, stretch_ratio)

            # 3. Salva il file modificato
            sf.write(audio_path, stretched_audio, sr)
        else:
            logger.debug(
                f"La durata di {os.path.basename(audio_path)} è già sufficientemente vicina. Nessun adattamento.")

    except Exception as e:
        logger.error(f"Errore durante l'adattamento della velocità per {audio_path}: {e}")


def create_final_audio_track(parsed_data, translated_texts, temp_dir, lang='en'):
    """
    Crea la traccia audio finale combinando i segmenti TTS generati.
    """
    final_track = AudioSegment.silent(duration=0)
    last_end_time = 0

    logger.info("Creazione traccia audio finale...")
    for i, data in enumerate(parsed_data):
        text = translated_texts[i]
        target_duration_ms = data['duration']

        start_time_ms = sum(int(t) * w for t, w in zip(data['timestamp'].split(':'), (3600000, 60000, 1000)))
        silence_duration = start_time_ms - last_end_time
        if silence_duration > 0:
            final_track += AudioSegment.silent(duration=silence_duration)

        # Usiamo .wav come formato intermedio
        segment_path = os.path.join(temp_dir, f"segment_{i}.wav")
        if text_to_speech(text, lang, segment_path):
            adjust_audio_speed(segment_path, target_duration_ms)
            # Carichiamo il file .wav finale
            segment_audio = AudioSegment.from_wav(segment_path)
            final_track += segment_audio
            last_end_time = start_time_ms + len(segment_audio)
        else:
            final_track += AudioSegment.silent(duration=target_duration_ms)
            last_end_time = start_time_ms + target_duration_ms

    logger.info("Traccia audio finale creata.")
    return final_track