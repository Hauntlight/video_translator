import logging
import sys


def get_logger(name):
    """
    Configura e restituisce un logger con un handler per la console e per un file.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Evita di aggiungere handler multipli
        logger.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console Handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File Handler
        file_handler = logging.FileHandler('logs/app.log', mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger