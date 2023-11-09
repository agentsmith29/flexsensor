class OpticalInterfaceStoredData:
    def __init__(self):
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

    @property
    def motor_out_x(self):
        return self._motor_out_x

    @motor_out_x.setter
    def motor_out_x(self, value):
        self._motor_out_x = value

    @property
    def motor_out_y(self):
        return self._motor_out_y

    @motor_out_y.setter
    def motor_out_y(self, value):
        self._motor_out_y = value

    @property
    def motor_out_z(self):
        return self._motor_out_z

    @motor_out_z.setter
    def motor_out_z(self, value):
        self._motor_out_z = value

    @property
    def motor_in_x(self):
        return self._motor_in_x

    @motor_in_x.setter
    def motor_in_x(self, value):
        self._motor_in_x = value

    @property
    def motor_in_y(self):
        return self._motor_in_y

    @motor_in_y.setter
    def motor_in_y(self, value):
        self._motor_in_y = value

    @property
    def motor_in_z(self):
        return self._motor_in_z

    @motor_in_z.setter
    def motor_in_z(self, value):
        self._motor_in_z = value

    @property
    def pzt_out_x(self):
        return self._pzt_out_x

    @pzt_out_x.setter
    def pzt_out_x(self, value):
        self._pzt_out_x = value

    @property
    def pzt_out_y(self):
        return self._pzt_out_y

    @pzt_out_y.setter
    def pzt_out_y(self, value):
        self._pzt_out_y = value

    @property
    def pzt_out_z(self):
        return self._pzt_out_z

    @pzt_out_z.setter
    def pzt_out_z(self, value):
        self._pzt_out_z = value

    @property
    def pzt_in_x(self):
        return self._pzt_in_x

    @pzt_in_x.setter
    def pzt_in_x(self, value):
        self._pzt_in_x = value

    @property
    def pzt_in_y(self):
        return self._pzt_in_y

    @pzt_in_y.setter
    def pzt_in_y(self, value):
        self._pzt_in_y = value

    @property
    def pzt_in_z(self):
        return self._pzt_in_z

    @pzt_in_z.setter
    def pzt_in_z(self, value):
        self._pzt_in_z = value


