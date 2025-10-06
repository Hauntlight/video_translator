from moviepy.editor import VideoFileClip, AudioFileClip
from src.io.logs import get_logger

logger = get_logger(__name__)


def save_text_file(content, path):
    """Salva una stringa di testo in un file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"File di testo salvato in {path}")
        return True
    except Exception as e:
        logger.error(f"Impossibile salvare il file di testo {path}: {e}")
        return False


def save_audio_file(audio_segment, path):
    """Salva un oggetto AudioSegment di pydub in un file."""
    try:
        audio_segment.export(path, format="mp3")
        logger.info(f"File audio salvato in {path}")
        return True
    except Exception as e:
        logger.error(f"Impossibile salvare il file audio {path}: {e}")
        return False


def combine_video_and_audio(video_path, audio_path, output_path):
    """Combina un file video con una nuova traccia audio."""
    try:
        logger.info(f"Combinazione di {video_path} e {audio_path}...")
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        # Imposta l'audio del video clip
        final_clip = video_clip.set_audio(audio_clip)

        # Scrivi il file finale
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        video_clip.close()
        audio_clip.close()
        logger.info(f"Video finale salvato in {output_path}")
        return True
    except Exception as e:
        logger.error(f"Impossibile combinare video e audio: {e}")
        return False