import logging

from rich.logging import RichHandler


class MyClass:

    # ==================================================================================================================
    # Public methods
    # ==================================================================================================================
    def __init__(self):
        self.name = self.__class__.__name__
        self.logger = self.create_new_logger(self.name)

    def create_new_logger(self, logger_name: str,
                          logger_format: str = "%(asctime)s - %(name)s %(message)s",
                          to_file='mylog.log',
                          level=logging.DEBUG) -> logging.Logger:

        # Set the formatter
        _std_handler_formatter = logging.Formatter(logger_format)
        _file_handler_formatter = logging.Formatter(f"%(levelname)s {logger_format})")

        _std_handler: logging.Handler = RichHandler(rich_tracebacks=True)
        _std_handler.setLevel(level)
        _std_handler.setFormatter(_std_handler_formatter)

        # Add a file handler as well
        _file_handler = logging.FileHandler(to_file)
        _file_handler.setLevel(logging.DEBUG)  # Always set the file handler to debug
        _file_handler.setFormatter(_file_handler_formatter)

        # Assign the handler to the logger
        _logger = logging.getLogger(logger_name)
        _logger.handlers = [_std_handler, _file_handler]
        _logger.setLevel(logging.DEBUG)  # Set the logger to debug, so every message is printed using the file handler

        return _logger

    def test_logging(self, msg):
        self.logger.warning(msg)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)
    myclass = MyClass()
    myclass.test_logging("MSG 1 Hello from MyClass") # The message is printed twice

    logger = logging.getLogger("mylogger")   # create a new logger
    logger.setLevel(logging.DEBUG)
    # (Not expected) This does not print anything, despite the level is set to DEBUG
    logger.debug("MSG 2 Hello from a new logger myLogger")
    # (Expected) This does not print, since the default level is WARNING
    logging.info("MSG 3 Hello from the default logger")
    # This now prints, since the level is WARNING
    logger.warning("MSG 4 Hello from a new logger myLogger")
    logging.warning("MSG 5: Hello from the default logger")
