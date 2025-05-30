import logging
from consts import LOGGER_NAME
from pathlib import Path


def setup_logger(name: str, log_level: str):
    logger = logging.getLogger(name=name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(fmt='{asctime} - {levelname} - {message}', style='{', datefmt='%Y-%m-%d %H:%M')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename="./homework_2/lab_3.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log_folder_structure(path: Path, level=0):
    logger = logging.getLogger(LOGGER_NAME)
    for item in sorted(path.iterdir()):
        prefix = '    ' * level + ('[FOLDER] ' if item.is_dir() else '[FILE] ')
        logger.info(f'{prefix}{item.name}')
        if item.is_dir():
            log_folder_structure(item, level + 1)
