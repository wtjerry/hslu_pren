import time

import math


class DummyTelescopeEngine:
    def __init__(self):
        self._is_lowered = False
        self.z = 0

    def down(self, height):
        print("lower telescope")
        for counter in range(0, math.floor(height)):
            self.z += 1
            time.sleep(0.001)
        self._is_lowered = True
        print("telescope lowered")

    def up(self, height):
        print("retract telescope")
        for counter in range(0, math.floor(height)):
            self.z -= 1
            time.sleep(0.001)

        self._is_lowered = False
        print("telescope retracted")

    def get_z(self):
        return self.z
