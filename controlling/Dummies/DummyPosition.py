import math

from controlling.Dummies.sensors.DummyXPosition import DummyXPosition
import time


class DummyPosition:
    _xposition_sensor = None
    _movement_engine = None
    _telescope_engine = None
    _position_output = False
    _START_HEIGHT = 575
    _TELESCOPE_HEIGHT = 150

    def __init__(self, movement_engine, telescope_engine, x_pos):
        self._xposition_sensor = x_pos
        self._movement_engine = movement_engine
        self._telescope_engine = telescope_engine

    def calculate_x(self):
        return self._xposition_sensor.get_position()

    def calculate_z(self, x):
        return (math.tan(0.141897) * x) + self._START_HEIGHT - self._TELESCOPE_HEIGHT - self._telescope_engine.get_z()

    def show_position(self):
        while self._position_output:
            x = self.calculate_x()
            print("----------------------------")
            print("Output load position: X Position: ", x, " Y Position: ", self.calculate_z(x))
            print("----------------------------")
            # TODO: Output the current position.
            time.sleep(0.2)

    def start_position_output(self):
        self._position_output = True
        self.show_position()

    def stop_position_output(self):
        self._position_output = False
