import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
# Importiamo una funzione diversa da pydub
from pydub.silence import detect_silence
import yaml
from src.io.logs import get_logger

logger = get_logger(__name__)


def extract_audio(video_path, output_audio_path):
    """
    Estrae la traccia audio da un file video e la salva in formato WAV.
    (Questa funzione rimane invariata)
    """
    try:
        logger.info(f"Estrazione audio da {video_path}...")
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_audio_path, codec='pcm_s16le')
        video_clip.close()
        logger.info(f"Audio estratto e salvato in {output_audio_path}")
        return output_audio_path
    except Exception as e:
        logger.error(f"Errore durante l'estrazione dell'audio: {e}")
        return None


def segment_audio(audio_path):
    """
    Segmenta un file audio basandosi sulle pause, mantenendo i timestamp originali.
    (Questa funzione è stata completamente riscritta)
    """
    try:
        with open('config/settings.yaml', 'r') as f:
            config = yaml.safe_load(f)['silence_detection']

        logger.info(f"Segmentazione di {audio_path} con timestamp corretti...")
        audio = AudioSegment.from_wav(audio_path)

        # Step 1: Rileva i periodi di silenzio.
        # detect_silence ritorna una lista di [start_ms, end_ms] per ogni pausa.
        silent_ranges = detect_silence(
            audio,
            min_silence_len=config['min_silence_len'],
            silence_thresh=config['silence_thresh']
        )

        if not silent_ranges:
            logger.warning("Nessuna pausa rilevata. L'intero audio verrà trattato come un unico segmento.")
            return [(audio, 0, len(audio))]

        # Step 2: "Inverti" i range di silenzio per ottenere i range di parlato.
        segments = []
        previous_silence_end = 0

        for silence_start, silence_end in silent_ranges:
            # Il pezzo di parlato è lo spazio tra la fine della pausa precedente
            # e l'inizio di questa pausa.
            speech_start = previous_silence_end
            speech_end = silence_start

            if speech_end > speech_start:
                # Estrai il chunk di audio e aggiungilo alla lista con i timestamp corretti
                speech_chunk = audio[speech_start:speech_end]
                segments.append((speech_chunk, speech_start, speech_end))

            previous_silence_end = silence_end

        # Step 3: Controlla se c'è un ultimo pezzo di parlato dopo l'ultima pausa
        total_duration = len(audio)
        if total_duration > previous_silence_end:
            last_speech_start = previous_silence_end
            last_speech_end = total_duration
            last_chunk = audio[last_speech_start:last_speech_end]
            segments.append((last_chunk, last_speech_start, last_speech_end))

        logger.info(f"Audio segmentato in {len(segments)} parti con timestamp assoluti.")
        return segments

    except Exception as e:
        logger.error(f"Errore durante la segmentazione dell'audio: {e}")
        return []