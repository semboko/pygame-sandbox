import logging


def create_logger(name: str, file: str, level: int = logging.DEBUG, _format: str = '%(levelname)s - %(asctime)s - %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(file)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(_format)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

