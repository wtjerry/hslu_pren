import time
import math

from controlling.Config import Config


class Position(object):
    _movement_engine = None
    _telescope_engine = None
    _should_calc = None
    _position_output = None
    _x_pos = 0
    _z_pos = 0


    def __init__(self, x_position_sensor, movement_engine, telescope_engine, position_sender):
        self._xposition_sensor = x_position_sensor
        self._movement_engine = movement_engine
        self._telescope_engine = telescope_engine
        self._position_sender = position_sender

    def start_calc_pos(self):
        self._should_calc = True
        while self._should_calc:
            if self._movement_engine.is_moving:
                self._x_pos = self._calculate_x()

            self._z_pos = self._calculate_z_from_x(self._x_pos)
            time.sleep(0.05)

    def start_position_output(self):
        self._position_output = True
        while self._position_output:
            self._position_sender.send(self._x_pos, self._z_pos)
            time.sleep(0.2)

    def stop_output(self):
        self._position_output = False

    def stop(self):
        self._position_output = False
        self._should_calc = False

    def _calculate_x(self):
        # return (self._xposition_sensor.get_position() +
        #        (self._START_X_POS + self._movement_engine.get_x())) \
        #       / 2
        current_x = Config.POSITION_START_X_POS + self._movement_engine.get_x()
        print("Current x: ", current_x)
        return current_x

    def _calculate_z_from_x(self, x):
        return (math.tan(Config.POSITION_GROUND_TO_CABLE_ANGLE) * x) \
               + Config.POSITION_START_HEIGHT \
               - self._telescope_engine.get_z()

    def get_current_x(self):
        return self._x_pos

    def get_current_z(self):
        return self._z_pos
