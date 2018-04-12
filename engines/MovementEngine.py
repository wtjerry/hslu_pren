import math


class MovementEngine(object):
    _START_COMMAND = "FBstart"
    _STOP_COMMAND = "FBstop"
    _GET_X_COMMAND = "FBgetx"
    _communication = None

    def __init__(self, communication):
        self._communication = communication
        self.is_moving = False

    def start(self, speed):
        self._communication.execute(self._START_COMMAND + str(speed))
        self.is_moving = True

    def stop(self):
        self._communication.execute(self._STOP_COMMAND)
        self.is_moving = False

    def get_x(self):
        x_on_rope = self._communication.execute(self._GET_X_COMMAND)
        alpha_angle = 8.13
        x = x_on_rope * math.cos(alpha_angle)
        return int(x)
