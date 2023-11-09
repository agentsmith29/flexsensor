import os

if os.environ.get('VELOX_SIM') is not None:
    print("Velox Simulator")
    from Prober.velox_api.simulator import VeloxSimulator as velox_api
    from Prober.velox_api.simulator.VeloxSimulator import (MessageServerInterface, SetChuckHome, SetMapHome,
                                                           ReadChuckPosition, ReadChuckHeights, MoveChuck,
                                                           SnapImage, GetDieDataAsColRow, StepToDie, ReportKernelVersion)
else:
    import Prober.velox_api.velox as velox_api
    from Prober.velox_api.velox import (MessageServerInterface, SetChuckHome, SetMapHome,
                                        ReadChuckPosition, ReadChuckHeights, MoveChuck,
                                        SnapImage, GetDieDataAsColRow, StepToDie, ReportKernelVersion)

from Prober.model.ProberModel import ProberModel as Model
from Prober.view.ProberControlWindow import ProberControlWindow as ControlWindow
from Prober.model.ProberModel import ProberSignals as Signals
from Prober.controller.ProberController import ProberController as Controller
from Prober.controller.ProberController import Probe as Probe
from Prober.controller.OpticalProbesPosition import OpticalProbesPosition as ProbePosition
