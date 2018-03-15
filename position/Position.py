import time
from position.XPositionSensor import XPositionSensor


class Position(object):
    _xposition_sensor = None
    _movement_engine = None
    _telescope_engine = None
    _position_output = False

    def __init__(self, movement_engine, telescope_engine):
        self._xposition_sensor = XPositionSensor()
        self._movement_engine = movement_engine
        self._telescope_engine = telescope_engine

    def _calculate_x(self):
        return (self._xposition_sensor.get_position() + self._movement_engine.get_x()) / 2

    def _calculate_z(self):
        return 100

    def _show_position(self):
        while self._position_output:
            x = self._calculate_x()
            z = self._calculate_z()
            PosistionCommand.set_current_position(x, z)
            time.sleep(1)


    def start_position_output(self):
        self._position_output = True
        self._show_position()

    def stop_position_output(self):
        self._position_output = False
