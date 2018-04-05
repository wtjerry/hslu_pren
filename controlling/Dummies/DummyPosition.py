import math
import time


class DummyPosition:
    _movement_engine = None
    _telescope_engine = None
    _should_calc = None
    _position_output = None
    _x_pos = 320
    _z_pos = 0
    _START_HEIGHT = 575
    _TELESCOPE_HEIGHT = 150
    _GROUND_TO_CABLE_ANGLE = 0.141897

    def __init__(self, movement_engine, telescope_engine, position_sender):
        self._movement_engine = movement_engine
        self._telescope_engine = telescope_engine
        self._position_sender = position_sender

    def start_calc_pos(self):
        self._should_calc = True

        while self._should_calc:
            if self._movement_engine.is_moving:
                self._x_pos += 5
                time.sleep(0.05)

            self._z_pos = self._calculate_z_from_x(self._x_pos)

    def start_position_output(self):
        self._position_output = True
        while self._position_output:
            self._position_sender.send(self._x_pos, self._z_pos)
            time.sleep(0.2)

    def stop(self):
        self._position_output = False
        self._should_calc = False

    def _calculate_z_from_x(self, x):
        return (math.tan(self._GROUND_TO_CABLE_ANGLE) * x) \
               + self._START_HEIGHT \
               - self._TELESCOPE_HEIGHT \
               - self._telescope_engine.get_z()

    def get_current_x(self):
        return self._x_pos

    def get_current_z(self):
        return self._z_pos
