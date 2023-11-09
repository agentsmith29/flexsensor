import logging

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal
from rich.logging import RichHandler
from scipy.signal import find_peaks#, find_peaks_cwt
import os
#from PySide6.QtNetwork import QAbstractSocket
from os import mkdir
from multiprocessing import Pool, Value
import os.path
from datetime import datetime
# Needed for Digilent Analog Discovery 2 data acquisition	
from ctypes import *
try:
    from generics.ConsoleWindow import ConsoleWindow
except:
    pass


class QTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = Signal(str)

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)


class Logger:
   
    log_file_full = None
    @staticmethod
    def set_output_file(logfile):
        Logger.log_file_full = logfile
        print("%s" % Logger.log_file_full)

    FORMAT="%Y-%m-%d %H-%M-%S.%f"

    @staticmethod
    def check_or_create_log_file():
        if log_file_full is None:
            raise ValueError("Log file can't be None")
        if not os.path.exists(os.path.dirname(Logger.log_file_full)):
            try:
                os.makedirs(os.path.dirname(Logger.log_file_full))
            except OSError as exc:  
                    raise  Exception("Could not create log file.")
        Logger.info("Log file created: %s" % Logger.log_file_full)

    @staticmethod 
    def debug(*args):
        msg =  datetime.now().strftime(Logger.FORMAT) + " [DEBUG] " + "".join(str(arg) for arg in args)
        # check if folder exists
        #logger.check_or_create_log_file()

        with open(Logger.log_file_full, "a+") as f:
            f.write(msg+ "\n")
            
        #status_bar.showMessage("[DEBUG] " + "".join(str(arg) for arg in args))
        #status_bar.setStyleSheet('border: 0; color:  blue;')
        print(msg)
        return msg

    @staticmethod
    def info(*args):
        msg =   datetime.now().strftime(Logger.FORMAT) + "  [INFO] " + "".join(str(arg) for arg in args)
        # check if folder exists
        #logger.check_or_create_log_file()

        with open(Logger.log_file_full, "a+") as f:
            f.write(msg + "\n")
        
        #status_bar.showMessage("[INFO] " + "".join(str(arg) for arg in args))
        #status_bar.setStyleSheet('border: 0; color:  black;')
        print(msg)
        return msg

    @staticmethod
    def warning(*args):
        msg =  datetime.now().strftime(Logger.FORMAT) + "  [WARN] " + "".join(str(arg) for arg in args)
        # check if folder exists
        #logger.check_or_create_log_file()

        with open(Logger.log_file_full, "a+") as f:
            f.write(msg+ "\n")

        #status_bar.showMessage("[WARN] " + "".join(str(arg) for arg in args))
        #status_bar.setStyleSheet('border: 0; color:  orange;')
        print(msg)
        return msg

    @staticmethod
    def error(*args):
        msg =  datetime.now().strftime(Logger.FORMAT) + " [ERROR] " + "".join(str(arg) for arg in args)
        # check if folder exists
        #logger.check_or_create_log_file()

        with open(Logger.log_file_full, "a+") as f:
            f.write(msg + "\n")
        
        #status_bar.showMessage("[ERROR] " + "".join(str(arg) for arg in args))
        #status_bar.setStyleSheet('border: 0; color:  red;')
        print(msg)
        return msg
    
    @staticmethod
    def fatal(*args):
        msg =   datetime.now().strftime(Logger.FORMAT) + " [FATAL] " + "".join(str(arg) for arg in args)
        # check if folder exists
        #logger.check_or_create_log_file()

        with open(Logger.log_file_full, "a+") as f:
            f.write(msg + "\n")
        
        #status_bar.showMessage("[FATAL] " + "".join(str(arg) for arg in args))
        #status_bar.setStyleSheet('border: 0; color:  red;')
        print(msg)
        return msg


def setup_logging(window: ConsoleWindow = None):
    for log_name, log_obj in logging.Logger.manager.loggerDict.items():
        if log_name != '<module name>':
            log_obj.disabled = True
    # Format the Rich logger
    FORMAT = "%(message)s"
    if window is not None:
        logging.basicConfig(
            level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                RichHandler(rich_tracebacks=True), window.handler
            ]
        )
    else:
        logging.basicConfig(
            level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                RichHandler(rich_tracebacks=True)
            ]
        )