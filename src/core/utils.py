import os
import shutil
from src.io.logs import get_logger

logger = get_logger(__name__)


def setup_directories(config):
    """
    Crea le directory temporanee e di output se non esistono.
    """
    temp_dir = config['output']['temp_dir']
    final_dir = config['output']['final_dir']

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        logger.info(f"Directory temporanea '{temp_dir}' pulita.")
    os.makedirs(temp_dir)

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
        logger.info(f"Directory di output '{final_dir}' creata.")


def get_output_paths(video_path, config):
    """
    Genera i percorsi per i file di output.
    """
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    temp_dir = config['output']['temp_dir']
    final_dir = config['output']['final_dir']

    return {
        "audio": os.path.join(temp_dir, f"{base_name}_audio.wav"),
        "transcription": os.path.join(final_dir, f"{base_name}_transcription_it.txt"),
        "translated_transcription": os.path.join(final_dir, f"{base_name}_transcription_en.txt"), # NUOVO
        "translated_audio": os.path.join(temp_dir, f"{base_name}_translated_audio.mp3"),
        "final_video": os.path.join(final_dir, f"{base_name}_translated.mp4")
    }