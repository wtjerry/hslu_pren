import time
import math

from controlling.Config import Config


class Position(object):
    _movement_engine = None
    _telescope_engine = None
    _should_calc = None
    _position_output = None
    _x_pos_horizontal = 0
    _z_pos_bottom_magnet_when_telescope_in = 0

    def __init__(self, x_position_sensor, movement_engine, telescope_engine, position_sender):
        self._xposition_sensor = x_position_sensor
        self._movement_engine = movement_engine
        self._telescope_engine = telescope_engine
        self._position_sender = position_sender

    def start_calc_pos(self):
        self._should_calc = True
        while self._should_calc:
            if self._movement_engine.is_moving:
                x_pos_on_rope = self._movement_engine.get_x()
                self._x_pos_horizontal = self._calculate_x_horizontal(x_pos_on_rope)
                self._z_pos_bottom_magnet_when_telescope_in = self._calculate_z_bottom_magnet_when_telescope_in(
                    self._x_pos_horizontal)
                print("Horizontal x: {x}, Telescope in z: {z_telescope_in}"
                      .format(x=self._x_pos_horizontal, z_telescope_in=self.get_current_z_telescope_when_in()))
            time.sleep(0.05)

    def start_position_output(self):
        self._position_output = True
        while self._position_output:
            print("Horizontal x: {x}, Telescope moving z: {z_telescope_moving}"
                  .format(x=self._x_pos_horizontal, z_telescope_moving=self.get_current_z_while_telescope_is_moving()))
            self._position_sender.send(self.get_current_x(), self.get_current_z_while_telescope_is_moving())
            time.sleep(0.2)

    def stop_output(self):
        self._position_output = False

    def stop(self):
        self._position_output = False
        self._should_calc = False

    def _calculate_x_horizontal(self, x_pos_on_rope):
        return 0.9868 * x_pos_on_rope + 287.12

    def _calculate_z_bottom_magnet_when_telescope_in(self, x_pos_horizontal):
        return -0.000000000006079 * x_pos_horizontal ** 4 \
               + 0.000000042190949 * x_pos_horizontal ** 3 \
               - 0.000041455473666 * x_pos_horizontal ** 2 \
               - 0.107742650963210 * x_pos_horizontal \
               + 1.370961454271310 - 465 + (100 + x_pos_horizontal) * 0.142857 + 600

    def get_current_x(self):
        return self._x_pos_horizontal

    def get_current_z_telescope_when_in(self):
        return self._z_pos_bottom_magnet_when_telescope_in - Config.POSITION_LOAD_HEIGHT

    def get_current_z_while_telescope_is_moving(self):
        return self.get_current_z_telescope_when_in() - self._telescope_engine.get_z()
