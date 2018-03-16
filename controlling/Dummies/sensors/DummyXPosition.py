import random
import time
from concurrent.futures import ThreadPoolExecutor


class DummyXPosition:
    def __init__(self, movement):
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.x_position = 0
        self._movement = movement
        self.executor.submit(self._calc_pos)

    def _calc_pos(self):
        while True:
            if self._movement.is_moving:
                self.x_position += random.random() * 60
                time.sleep(0.3)

    def get_position(self):
        """
        Returns the current xPosition in mm.
        :rtype: int
        """
        return self.x_position
