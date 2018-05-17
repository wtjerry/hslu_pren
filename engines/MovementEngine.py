import math


class MovementEngine(object):
    _RESET_COMMAND = "RS"
    _START_COMMAND = "FBstart"
    _CHANGE_SPEED_COMMAND = "FBsetspeed"
    _STOP_COMMAND = "FBstop"
    _GET_X_COMMAND = "FBgetx"
    _communication = None
    _GROUND_TO_CABLE_ANGLE = 0.141897

    def __init__(self, communication):
        self._communication = communication
        self.is_moving = False

    def reset(self):
        self._communication.execute(self._RESET_COMMAND)

    def start(self, speed):
        self._communication.execute(self._START_COMMAND + str(speed))
        self.is_moving = True

    def stop(self):
        self._communication.execute(self._STOP_COMMAND)
        self.is_moving = False

    def set_speed(self, speed):
        self._communication.execute(self._CHANGE_SPEED_COMMAND + str(speed))

    def get_x(self):
        x_on_rope = int(self._communication.execute(self._GET_X_COMMAND))
        x = x_on_rope * math.cos(self._GROUND_TO_CABLE_ANGLE)
        return int(x)
