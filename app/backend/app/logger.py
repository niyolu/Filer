import logging


logger = logging.getLogger("my_custom_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(asctime)s - %(levelname)s - %(funcName)s] %(message)s",
    datefmt="%d %b %Y - %H:%M:%S"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)