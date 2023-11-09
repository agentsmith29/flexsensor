from PySide6.QtCore import QObject, Signal

from MeasurementData.MeasuredData.SingleMeasuredData import SingleMeasuredData


class WorkerSignals(QObject):

    finished = Signal()

    error = Signal(tuple)

    warning = Signal(tuple)

    result = Signal(object)

    progress = Signal(float)

    # Reports the measured data and the iteration number
    routine_iteration_finished = Signal(SingleMeasuredData, int)

    write_log = Signal(str, str)

    report_info = Signal(dict)
