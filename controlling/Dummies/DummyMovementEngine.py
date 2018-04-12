from concurrent.futures import ThreadPoolExecutor
from time import sleep

from controlling.AsyncProcessor import AsyncProcessor


class DummyMovementEngine:
    x_pos = 0
    speed = 0

    def __init__(self):
        self.is_moving = False
        self._executor = AsyncProcessor(ThreadPoolExecutor(max_workers=2))

    def start(self, speed):
        print("Started to move at speed", speed)
        self.set_speed(speed)
        self.is_moving = True
        self._executor.enqueue(self._calc_x)

    def stop(self):
        print("stopped moving")
        self.is_moving = False

    def set_speed(self, speed):
        self.speed = (speed*10) - 7

    def _calc_x(self):
        while self.is_moving:
            self.x_pos += self.speed
            sleep(0.025)

    def get_x(self):
        return self.x_pos

