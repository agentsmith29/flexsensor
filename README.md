
# Flexsensor




An automation software for [FormFactor Cascade Summit200](https://www.formfactor.com/product/probe-systems/200-mm-systems/summit200/) Probe Stations.
*FlexSensor* is a software that allows to automate measurements using the FormFactor Wafer Prober.

*FlexSensor* is a standalone Python application. Its versatility allows for immediate deployment, without prior programming knowledge. Particularly noteworthy are its post-processing capabilities, however, the software's core functionality is the use of the automated measurement routine to acquire the resonant spectra of photonic devices, integrated within a specialized measurement system, as detailed in Section 

## Still under construction*
This repository is under construction. The software is ready for deplyoment but is still in beta. 
If you find any bugs or have any suggestions, please open an issue.

![](https://upload.wikimedia.org/wikipedia/commons/f/f0/Baustelle-mittel.png)

# Installation
## Get the source files
Clone the repository to your local machine.
```bash
git clone git@gitlab.tugraz.at:flexsensor-public/flexsensor.git
```

Create a virtual environment (highly recommended) and install the dependencies.
```python
python -m venv .venv;
source .venv/Scripts/Activate;
pip install -r requirements.txt
```

# Starting the software
To start the software, simply run the `examples/main.py` file. 
```python
python main.py
```

# Defining a measurement routine
The measurement routine is defined in a python file. Each measurement routine must inherit from the `BaseMeasurementRoutine` class.
Note that the base class has an overloaded constructor that requires the following parameters:
- `prober`: The Prober.Controller object that is used to measure the structures
- `config`: The FlexSensorConfig object that is used to measure the structures
```python
import FlexSensor as fs

class MeasurementRoutine(fs.BaseMeasurementRoutine):

    def __init__(prober: Prober.Controller,
                 config: fs.FlexSensorConfig):
        super().__init__(prober, config)

    @Slot()
    def run(self): 
        # your code here
```
In the `run` method, the measurement routine is defined. 
The `run` method is called by the `MeasurementRoutineThread` class, which is a QThread object. This allows to run the method
in a separate thread, while the GUI remains responsive. 



# Measuring using FlexSensor
It is often useful to measure a large number of structures on a wafer. For this, the software allows to define a
measurement routine that is executed for each structure. 
The `vas`-File allows to define a list of structures that are measured. Thede file is parsed and passed
to the `MeasurementRoutine` class.
```python
import FlexSensor as fs
# ...
def readVasFile(self):
    self.parsed_file = fs.VASInputFileParser()
    
    selected_file, self.grouped_structures, self.bookmarks = self.parsed_file.read_file(
         input_file='structure_file.vas'
     )
# ...
```
The `VASInputFileParser` class parses the `vas`-File and returns a list of structures that are measured.
- `selected_file`: The selected file. In case the file is not found, the user is prompted to select a file by a file dialog.
- `grouped_structures`: A list of structures that are measured. Each structure is a python dictionary that contains the
  information on how to measure the structure.
- `bookmarks`: A list of bookmarks that are defined in the `vas`-File. These bookmarks are used to create a Klayout
  bookmark file that can be used to navigate to the structures in Klayout.
## Input Structure File
The measuring process relies on a ```vas```-File that store the positions to the structures. in priciple 
this file os a list of python dictionary in a predefined format, that allows the easy definiton
on how to measure the structures. 
The file allows python-style line comments using the ```#```-sign
### Comments and Bookmarks
```python
# First structure to measure  
# group="mrr1"
```
Sometimes it is useful to have the Klayout-positions bookmarked. Using the Klayout-Coordinates, the
software creates a readable Bookmark file that can be used in Klayout.
```python
# Bookmark this view
mrr1_bookmark = { 'x_left': 19012, 'x_right' : 20708, 'y_bottom' : 20185, 'y_top': 21866 }
```
### Defining a measurement point
Defining a measurement point requires the input position (`x_in`, `y_in`) and the output 
position (`x_out`, `y_out`). The keyword `repetitions` allows to define the number of repeated measurements of the same
structure (e.g., for statistical evaluation, etc.)
<br> 
**These positions are relative and measured from a predefined point (See Sec ...) on how
to select this point which can be chosen arbitrarily.**
```python
mrr1_ref = {'y_in' : -2120, 'x_in' : 960, 'y_out' : -2120, 'x_out' : -155, 'repetitions': 2}
```
Sometimes it is useful to define a group of measurement points that are equally spaced in x-direction. For this, the 
`spacing` and `num`-keyword can be used. Using these values, the software will automatically generate a list of 
`num` structures, equally spaced in x-direction using the `spacing` value. 
```python
mrr1     = {'y_in' : -1845, 'x_in' : 960, 'y_out' : -2015, 'x_out' : -155,  'num' : 6, 'spacing' : 100, 'repetitons': 200}
```

## Setup before measuring
1. Open the correct wafer map. 
Open the wafer Map under **Velox** -> **WaferMap**. Load the correct wafer file and select or deselect dies you do not 
want to capture. 
![](images/docs_img/open_wafer_map.png)
 **Note**: Make sure that the die and wafer size is correct.
2. Auto-Align the Wafer
 For this open the "AutoAlign" Wizard  and find a suitable alignment structure. 
![](images/docs_img/autoalign_wafer.png)
3. Place at "your" origin
The structure file relies on "relative" positions to a point you
find a suitable structur which is defined as the "die" origin. This is used to  measure the distance to the to/be measured strcutures. Use the same mark in zour Klayout file and on the wafer. 
![](images/docs_img/origina_at_wafer.JPG)
If you have not yet created a list for measuring your structure, you can use 
- the wafer prober find the right coordinates.
- the KLayout-File for measuring the structures
5. Set contact height
Set our fiber to the correct height. Then use the "Set Contact height". Otherwise the measurement routine will fail!
6. Train the Home Positions
This step is crucial and needed to train the output positions.


# Licence and usage
This software is licenced under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.de.html). 
If you use this software for your work or in your papers please cite me the following:



# FAQ&Issues
This section should cover the issues that may occure during usage or development. 
## Installation issues and running
There are some combinations of pyside6 and pyqtgraph that may lead to incompatibility
issues. Especially `PySide 6.5.0` and `pyqtgraph 0.13.2` installation lead to 
```python
TypeError: GraphicsWidgetAnchor.__init__() takes 1 positional argument but 2 were given
```
[Solution](https://stackoverflow.com/questions/76005506/pyqtgraphs-graphicswidgetanchor-class-incomplatible-with-pyside6?noredirect=1#comment134055507_76005506):
Remove your current installed pyqtgraph and install the latest version:
```python
pip install git+https://github.com/pyqtgraph/pyqtgraph@master
```