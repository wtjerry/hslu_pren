from concurrent.futures import ThreadPoolExecutor
from time import sleep


class DummyMovementEngine:
    x_pos = 0
    speed = 0

    def __init__(self):
        self.is_moving = False
        self._executor = ThreadPoolExecutor(max_workers=2)

    def start(self, speed):
        print("Started to move at speed", speed)
        self.set_speed(speed)
        self.is_moving = True
        self._executor.submit(self._calc_x)

    def stop(self):
        print("stopped moving")
        self.is_moving = False

    def set_speed(self, speed):
        self.speed = (speed*20) - 15

    def _calc_x(self):
        while self.is_moving:
            self.x_pos += self.speed
            print(self.x_pos)
            sleep(0.025)

    def get_x(self):
        return self.x_pos

