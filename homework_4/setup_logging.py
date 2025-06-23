import logging


def init_logger(logger_name: str):
    """
    description:
    initialize a logger with INFO level that logs messages to both a file and the console

    :param logger_name: name of the logger to initialize

    :return: --> void
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel('INFO')

    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_file_handler = logging.FileHandler('log.txt')
    log_stream_handler = logging.StreamHandler()

    log_file_handler.setFormatter(log_formatter)
    log_stream_handler.setFormatter(log_formatter)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_stream_handler)
