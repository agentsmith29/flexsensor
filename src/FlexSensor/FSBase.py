import logging
import time

from rich.logging import RichHandler


class FSBase:

    # ==================================================================================================================
    # Public methods
    # ==================================================================================================================
    def __init__(self):
        self._internal_logger = None
        self._internal_log_handler = None
        self.name = self.__class__.__name__

    def create_new_logger(self, logger_name: str, logger_handler: logging.Handler = logging.NullHandler(),
                          enabled=True, level=logging.DEBUG, propagate=True) -> logging.Logger:
        # logger_handler.setLevel(level)
        _internal_logger = logging.getLogger(logger_name)
        _internal_logger.handlers = [logger_handler]
        _internal_logger.propagate = propagate
        _internal_logger.setLevel(level)

        if enabled:
            _internal_logger.disabled = False
            _internal_logger.info(f"Logger {logger_name} created with ({len(_internal_logger.handlers)}) "
                                  f"handlers and has been enabled (Level {_internal_logger.level}).")
        else:
            _internal_logger.info(f"Logger {logger_name} created and has been disabled.")
            _internal_logger.disabled = True

        return _internal_logger

    def set_log_enabled(self, logger: logging.log, enable: bool) -> None:
        """
        Enables or disables internal logging. If disabled, the internal logger will be disabled and no messages will be
        emitted to the state queue.
        :param enable: True to enable, False to disable

        Args:
            logger:
        """
        if logger is not None:
            if enable:
                logger.disabled = False
                logger.info(f"Internal logger of {self.name} has been enabled.")

            else:
                logger.warning(f"Internal logger of {self.name} has been disabled.")
                logger.disabled = True
        else:
            raise Exception(f"Can't enable or disable {logger}.")  #

    def set_log_level(self, logger: logging.log, level: int) -> None:
        """
        Sets the internal logging level.
        :param level:
        :return:

        Args:
            logger:
        """
        if logger is not None:
            if level == logging.DEBUG:
                logger.info(f"Internal log level of {self.__class__.__name__} has been set to DEBUG.")
            elif level == logging.INFO:
                logger.info(f"Internal log level of {self.__class__.__name__} has been set to INFO.")
            elif level == logging.WARNING:
                logger.info(f"Internal log level of {self.__class__.__name__} has been set to WARNING.")
            elif level == logging.ERROR:
                logger.info(f"Internal log level of {self.__class__.__name__} has been set to ERROR.")
            elif level == logging.CRITICAL:
                logger.info(f"Internal log level of {self.__class__.__name__} has been set to CRITICAL.")
            else:
                logger.info(f"Internal log level of {self.__class__.__name__} has been set to level {level}.")
            logger.handlers[0].setLevel(level)
        else:
            raise Exception("Can't set internal log level. Internal logger not initialized")
