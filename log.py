
import logging
from logging.handlers import RotatingFileHandler

__author__ = 'Thomas'


def setup_custom_logger(name):

    formatter = logging.Formatter("%(asctime)s -- %(levelname)s -- %(module)s -- %(message)s")

    logger = logging.getLogger(name)
    handler = logging.handlers.RotatingFileHandler("info.log", mode="a",
                                                   maxBytes=10000000, backupCount=1, encoding="utf-8")
    handler.setFormatter(formatter)
    high_handler = logging.handlers.RotatingFileHandler("important.log", mode="a",
                                                        maxBytes=10000000, backupCount=1, encoding="utf-8")
    high_handler.setLevel(logging.WARNING)
    high_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(high_handler)

    return logger
