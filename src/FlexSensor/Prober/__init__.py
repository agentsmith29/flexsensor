import os

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from .model.ProberModel import ProberModel as Model
from .model.ProberModel import ProberSignals as Signals

from .controller.OpticalProbesPosition import OpticalProbesPosition as ProbePosition
from .controller.OpticalInterface import OpticalInterface


from .controller.ProberController import ProberController as Controller
from .view.ProberControlWindow import ProberControlWindow as ControlWindow





if os.getenv("VELOX_SIM") == "TRUE":
    try:
        from .velox_api.simulator.VeloxSimulator import MessageServerInterface
        from .velox_api.simulator.VeloxSimulator import (MessageServerInterface, SetChuckHome, SetMapHome,
                                                               ReadChuckPosition, ReadChuckHeights, MoveChuck,
                                                               SnapImage, GetDieDataAsColRow, StepToDie,
                                                              ReportKernelVersion)
    except Exception as e:
        from .velox_api.simulator.VeloxSimulator import MessageServerInterface
        from .velox_api.simulator.VeloxSimulator import (MessageServerInterface, SetChuckHome, SetMapHome,
                                                         ReadChuckPosition, ReadChuckHeights, MoveChuck,
                                                         SnapImage, GetDieDataAsColRow, StepToDie,
                                                         ReportKernelVersion)
else:
    try:
        from .velox_api.velox.vxmessageserver import MessageServerInterface
        from .velox_api.velox import (MessageServerInterface, SetChuckHome, SetMapHome,
                                            ReadChuckPosition, ReadChuckHeights, MoveChuck,
                                            SnapImage, GetDieDataAsColRow, StepToDie, ReportKernelVersion)
    except Exception as e:
        from .velox_api.simulator.VeloxSimulator import MessageServerInterface
        from .velox_api.simulator.VeloxSimulator import (MessageServerInterface, SetChuckHome, SetMapHome,
                                                         ReadChuckPosition, ReadChuckHeights, MoveChuck,
                                                         SnapImage, GetDieDataAsColRow, StepToDie,
                                                         ReportKernelVersion)

