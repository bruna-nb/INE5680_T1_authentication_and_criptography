import logging


class LoggerUtils:

    @staticmethod
    def get_logger(name):
        # Create a logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Create console handler and set level to INFO
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)

        # Create file handler and set level to DEBUG
        file_handler = logging.FileHandler('logging.log')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        return logger
