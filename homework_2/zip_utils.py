import shutil
import logging
from consts import LOGGER_NAME


def archive_folder(path: str, zip_name: str):
    logger = logging.getLogger(LOGGER_NAME)
    archive_name = shutil.make_archive(zip_name, 'zip', path)
    logger.info(f'Folder archived: {archive_name}')
