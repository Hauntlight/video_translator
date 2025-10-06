import re
from src.io.logs import get_logger

logger = get_logger(__name__)


def parse_transcription_file(file_content):
    """
    Estrae frasi, timestamp e durate da un file di testo formattato.

    Args:
        file_content (str): Il contenuto del file di testo.

    Returns:
        list: Una lista di dizionari, ognuno con 'timestamp', 'duration', 'text'.
    """
    parsed_data = []
    # Regex per catturare [hh:mm:ss][durata]"testo"
    pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2})\]\[(\d+)\]\s*"(.*?)"')

    lines = file_content.strip().split('\n')
    for line in lines:
        match = pattern.match(line)
        if match:
            timestamp, duration, text = match.groups()
            parsed_data.append({
                'timestamp': timestamp,
                'duration': int(duration),
                'text': text
            })
        else:
            logger.warning(f"La riga non corrisponde al formato atteso: '{line}'")

    return parsed_data