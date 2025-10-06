from gtts import gTTS
from pydub import AudioSegment
import os
import yaml
from src.io.logs import get_logger
import numpy as np
import pyrubberband as pyrb
import soundfile as sf

logger = get_logger(__name__)


def text_to_speech(text, lang, output_path):
    """
    Converte una stringa di testo in un file audio WAV.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        temp_mp3_path = output_path.replace('.wav', '.mp3')
        tts.save(temp_mp3_path)
        # Assicura che il file WAV iniziale sia MONO
        AudioSegment.from_mp3(temp_mp3_path).set_channels(1).export(output_path, format="wav")
        os.remove(temp_mp3_path)
        logger.debug(f"Testo '{text[:20]}...' convertito in audio a {output_path}")
        return True
    except Exception as e:
        logger.error(f"Errore durante la generazione TTS per '{text[:20]}...': {e}")
        return False


def adjust_audio_speed(audio_path, target_duration_ms):
    """
    Regola la velocità di un file audio e restituisce un oggetto AudioSegment pydub
    della durata (approssimata) target_duration_ms. Se la funzione di time-stretch
    fallisce, ritorna un segmento di silenzio della durata target.
    """
    try:
        y, sr = sf.read(audio_path, dtype='float32')

        # Mono: media dei canali se necessario
        if y.ndim > 1:
            logger.debug(f"Rilevato audio stereo per {os.path.basename(audio_path)}, conversione in mono.")
            y = y.mean(axis=1)

        original_duration_ms = int((len(y) / sr) * 1000)

        # edge cases
        if original_duration_ms == 0 or target_duration_ms == 0:
            return AudioSegment.silent(duration=target_duration_ms)

        # tolleranza: se la differenza è trascurabile, restituisci l'originale
        tol_ms = max(10, int(0.005 * original_duration_ms))
        if abs(original_duration_ms - target_duration_ms) <= tol_ms:
            return AudioSegment.from_wav(audio_path)

        # candidate_rate = original / target  -> >1 = velocizza, <1 = rallenta
        candidate_rate = original_duration_ms / float(target_duration_ms)

        best_audio = None
        best_diff = None
        chosen_rate = None

        # Proviamo prima il candidato (original/target); poi l'alternativa (target/original)
        for rate in (candidate_rate, 1.0 / candidate_rate):
            try:
                stretched = pyrb.time_stretch(y, sr, rate)
            except Exception as e:
                logger.warning(f"Time-stretch con rate={rate:.4f} fallito: {e}")
                continue

            stretched_ms = int((len(stretched) / sr) * 1000)
            diff = abs(stretched_ms - target_duration_ms)
            logger.debug(f"Provato rate={rate:.4f} → durata {stretched_ms}ms (diff {diff}ms)")

            if best_diff is None or diff < best_diff:
                best_diff = diff
                best_audio = stretched
                chosen_rate = rate

            # se siamo molto vicini al target usiamo subito questo risultato
            if diff <= max(20, int(0.01 * target_duration_ms)):
                break

        if best_audio is None:
            logger.error(f"Time-stretch fallito per {audio_path}; restituisco silenzio ({target_duration_ms}ms).")
            return AudioSegment.silent(duration=target_duration_ms)

        # Clip per sicurezza e conversione ad int16
        best_audio = np.clip(best_audio, -1.0, 1.0)
        int_audio_data = (best_audio * 32767).astype(np.int16)

        segment = AudioSegment(
            data=int_audio_data.tobytes(),
            sample_width=2,
            frame_rate=sr,
            channels=1
        )

        # Forza la durata esatta (pad o trim)
        if len(segment) < target_duration_ms:
            segment += AudioSegment.silent(duration=(target_duration_ms - len(segment)))
        elif len(segment) > target_duration_ms:
            segment = segment[:target_duration_ms]

        logger.info(
            f"Adattamento velocità per {os.path.basename(audio_path)}: "
            f"da {original_duration_ms}ms a {target_duration_ms}ms (rate scelto {chosen_rate:.4f})"
        )
        return segment

    except Exception as e:
        logger.error(f"Errore durante l'adattamento della velocità per {audio_path}: {e}")
        return AudioSegment.silent(duration=target_duration_ms)


def create_final_audio_track(parsed_data, translated_texts, temp_dir, total_duration_ms, lang='en'):
    """
    Crea la traccia audio finale rispettando rigorosamente i timestamp e le durate.
    Ogni segmento viene inserito nella posizione esatta su una traccia silenziosa
    lunga quanto il video originale. Nessuna sovrapposizione o concatenazione errata.
    """
    logger.info("Inizio creazione traccia audio finale (metodo timeline precisa)...")

    #  Traccia vuota lunga quanto il video
    final_track = AudioSegment.silent(duration=total_duration_ms)

    for i, data in enumerate(parsed_data):
        text = translated_texts[i]
        target_duration_ms = int(data["duration"])

        #  Calcolo del timestamp in millisecondi
        timestamp_parts = [int(p) for p in data["timestamp"].split(":")]
        if len(timestamp_parts) == 3:
            start_time_ms = timestamp_parts[0] * 3600000 + timestamp_parts[1] * 60000 + timestamp_parts[2] * 1000
        elif len(timestamp_parts) == 2:
            start_time_ms = timestamp_parts[0] * 60000 + timestamp_parts[1] * 1000
        else:
            start_time_ms = timestamp_parts[0] * 1000

        segment_path = os.path.join(temp_dir, f"segment_{i}.wav")

        #  Genera l'audio TTS
        if text_to_speech(text, lang, segment_path):
            segment_audio = adjust_audio_speed(segment_path, target_duration_ms)
        else:
            logger.warning(f"Segmento {i} generato in silenzio per errore TTS.")
            segment_audio = AudioSegment.silent(duration=target_duration_ms)

        #  Inserisci il segmento nella traccia silenziosa esattamente al timestamp
        final_track = final_track.overlay(segment_audio, position=start_time_ms)

        logger.debug(
            f"Segmento {i}: start={start_time_ms}ms, durata={target_duration_ms}ms, "
            f"text='{text[:30]}...'"
        )

    # Verifica finale lunghezza
    final_length = len(final_track)
    if final_length > total_duration_ms:
        logger.warning(
            f"La traccia finale ({final_length}ms) eccede la durata del video ({total_duration_ms}ms). Taglio eseguito."
        )
        final_track = final_track[:total_duration_ms]

    logger.info(f"Traccia audio finale completata. Durata: {len(final_track)/1000:.2f}s.")
    return final_track
