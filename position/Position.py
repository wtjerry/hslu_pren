import time
import math

from position.XPositionSensor import XPositionSensor


class Position(object):
    _xposition_sensor = None
    _movement_engine = None
    _telescope_engine = None
    _position_output = False
    _START_HEIGHT = 600
    _TELESCOPE_HEIGHT = 150

    def __init__(self, movement_engine, telescope_engine):
        self._xposition_sensor = XPositionSensor()
        self._movement_engine = movement_engine
        self._telescope_engine = telescope_engine

    def calculate_x(self):
        return (self._xposition_sensor.get_position() + self._movement_engine.get_x()) / 2

    def calculate_z(self, x):
        return (math.tan(0.141897) * x) + self._START_HEIGHT - self._TELESCOPE_HEIGHT - self._telescope_engine.get_z()

    def show_position(self):
        while self._position_output:
            x = self.calculate_x()
            z = self.calculate_z(x)
            # TODO: Output the current position.
            time.sleep(1)

    def start_position_output(self):
        self._position_output = True
        self.show_position()

    def stop_position_output(self):
        self._position_output = False
