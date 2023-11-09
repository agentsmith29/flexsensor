from MeasurementRoutines.view.Ui_MeasurementControlFlow import Ui_MeasurementControlFlow


class MeasurementControlFlow():
    def __init__(self, measurementRoutine: BaseMeasurementRoutine):
        # Init the UI file
        self._ui = Ui_MeasurementControlFlow()
        self._ui.setupUi(self)

