
"""Determines the version of the sci module to import"""
from sys import version_info
from Prober.velox_api.velox.vxmessageserver import *

if (version_info[0] > 2 and version_info[1] >= 5):
    from Prober.velox_api.velox.sci35 import *
else:
    from Prober.velox_api.velox.sci27 import *
