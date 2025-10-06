from googletrans import Translator
from src.io.logs import get_logger
import time

logger = get_logger(__name__)


def translate_sentences(sentences, target_lang='en'):
    """
    Traduci una lista di frasi.

    Args:
        sentences (list): Lista di frasi da tradurre.
        target_lang (str): Lingua di destinazione.

    Returns:
        list: Lista di frasi tradotte.
    """
    if not sentences:
        return []

    translator = Translator()
    translated_sentences = []
    logger.info(f"Inizio traduzione di {len(sentences)} frasi in '{target_lang}'...")

    for sentence in sentences:
        try:
            # Aggiungiamo un piccolo ritardo per non sovraccaricare l'API gratuita
            time.sleep(0.1)
            translation = translator.translate(sentence, dest=target_lang)
            translated_sentences.append(translation.text)
            logger.debug(f"'{sentence}' -> '{translation.text}'")
        except Exception as e:
            logger.error(f"Errore durante la traduzione di '{sentence}': {e}")
            translated_sentences.append(f"<{sentence} [TRADUZIONE FALLITA]>")

    logger.info("Traduzione completata.")
    return translated_sentences