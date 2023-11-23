import os
import pathlib
import sys

from .__version__ import __version__

#from .Prober import Prober


from .generics import ConsoleWindow as Console

from .__version__ import __version__
from .MainWindow.controller.MainThreadController import MainThreadController
from .MainWindow.model.MainThreadModel import MainThreadModel
from .MainWindow.view.MainThreadView import MainWindow
from .MainWindow.view.SplashScreen import SplashScreen
from .generics.ApplicationInit import ApplicationInit
from .generics.ConsoleWindow import ConsoleWindow
from .pathes import configs_root