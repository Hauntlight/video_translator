from src.io.logs import get_logger

logger = get_logger(__name__)

def read_text_file(path):
    """Legge il contenuto di un file di testo."""
    try:
        with open(path, 'r', encoding='utf--8') as f:
            content = f.read()
        logger.info(f"File di testo caricato con successo da {path}")
        return content
    except FileNotFoundError:
        logger.warning(f"File non trovato: {path}")
        return None
    except Exception as e:
        logger.error(f"Impossibile leggere il file di testo {path}: {e}")
        return None