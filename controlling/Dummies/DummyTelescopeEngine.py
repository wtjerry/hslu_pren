import time

import math


class DummyTelescopeEngine:
    _GROUND_TO_CABLE_ANGLE = 0.141897
    def __init__(self):
        self._is_lowered = False
        self.z = 0

    def down(self, height):
        print("lower telescope")
        for counter in range(0, int(math.floor(height/5))):
            self.z += 5
            time.sleep(0.001)
        self._is_lowered = True
        print("telescope lowered")

    def up(self, height):
        print("retract telescope")
        for counter in range(0, int(math.floor(height/5))):
            self.z -= 5
            time.sleep(0.001)

        self._is_lowered = False
        print("telescope retracted")

    def get_z(self):
        (math.tan(self._GROUND_TO_CABLE_ANGLE) * 12)
        return int(self.z)
