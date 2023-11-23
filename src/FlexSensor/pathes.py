# PLace here your interpreter startup folder relative to ./flexsensor
# e.g.
# -> interpreter path C:\flexsensor
# -> source path C:\flexsensor\flexsensorpy
# content_root = './flexsensorpy'
import os
import pathlib

content_root = "."

# DO not change this unless you know what you are doing!
image_root = str(pathlib.Path(f"{content_root}/../images").resolve().absolute())
libs_root = str(pathlib.Path(f"{content_root}/libs").resolve().absolute())
configs_root = str(pathlib.Path(f"{content_root}/../configs").resolve().absolute())
