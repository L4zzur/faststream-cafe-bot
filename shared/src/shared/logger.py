import logging
import sys


def setup_logger(service_name: str, level: str = "INFO") -> logging.Logger:
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt=f"%(asctime)s | %(levelname)-8s | {service_name} | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger("aiormq").setLevel(logging.WARNING)
    logging.getLogger("aio_pika").setLevel(logging.WARNING)

    return logging.getLogger(service_name)
