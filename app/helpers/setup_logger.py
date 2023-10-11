import logging


def setup_logger(log_file=None, log_level=logging.INFO):
    """
    Configura um logger para ser usado em todo o projeto, exibindo logs no console e salvando-os em um arquivo.
    :param log_file:
    :param log_level:
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    formatter = logging.Formatter(log_format)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger('crawler.log')
