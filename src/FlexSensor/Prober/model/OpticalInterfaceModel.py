class OpticalInterfaceSignals():
    pass



class OpticalInterfaceModel():
    def __init__(self):
        # Motor position
        self._motor_out_x: float = 0.0
        self._motor_out_y: float = 0.0
        self._motor_out_z: float = 0.0

        self._motor_in_x: float = 0.0
        self._motor_in_y: float = 0.0
        self._motor_in_z: float = 0.0

        # PZT position
        self._pzt_out_x: float = 0.0
        self._pzt_out_y: float = 0.0
        self._pzt_out_z: float = 0.0

        self._pzt_in_x: float = 0.0
        self._pzt_in_y: float = 0.0
        self._pzt_in_z: float = 0.0

