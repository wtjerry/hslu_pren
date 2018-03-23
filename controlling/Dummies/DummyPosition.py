import math
import time


class DummyPosition:
    _movement_engine = None
    _telescope_engine = None
    _position_output = False
    _should_calc = True
    _x_pos = 320
    _START_HEIGHT = 575
    _TELESCOPE_HEIGHT = 150

    def __init__(self, movement_engine, telescope_engine):
        self._movement_engine = movement_engine
        self._telescope_engine = telescope_engine

    def start_calc_pos(self):
        while self._should_calc:
            if self._movement_engine.is_moving:
                self._x_pos += 5
                time.sleep(0.05)

    def calculate_x(self):
        return self._x_pos

    def calculate_z(self, x):
        return (math.tan(0.141897) * x) + self._START_HEIGHT - self._TELESCOPE_HEIGHT - self._telescope_engine.get_z()

    def show_position(self):
        while self._position_output:
            x = self.calculate_x()
            print("----------------------------")
            print("Output load position: X Position: ", x, " Z Position: ", self.calculate_z(x))
            print("----------------------------")
            # TODO: Output the current position.
            time.sleep(0.2)

    def start_position_output(self):
        self._position_output = True
        self.show_position()

    def stop(self):
        self._position_output = False
        self._should_calc = False
