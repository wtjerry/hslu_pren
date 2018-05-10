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
                arduino_x = self._movement_engine.get_x()
                current_x = Config.POSITION_START_X_POS + \
                    (math.cos(Config.POSITION_GROUND_TO_CABLE_ANGLE) * arduino_x)
                print("Current x: ", current_x)
                self._x_pos = current_x

            self._z_pos = self._calculate_z_from_arduino_x(arduino_x)
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

    def _calculate_z_from_arduino_x(self, arduino_x):
        arduino_x = math.cos(Config.POSITION_GROUND_TO_CABLE_ANGLE) * arduino_x
        return (math.tan(Config.POSITION_GROUND_TO_CABLE_ANGLE) * arduino_x) \
            + Config.DISTANCE_BOTTOM_MAGNET_TO_TOP_LOAD \
            - self._telescope_engine.get_z()

    def get_current_x(self):
        return self._x_pos

    def get_current_z(self):
        return self._z_pos
