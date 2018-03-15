import time


class DummyTelescope:
    def __init__(self):
        self._is_lowered = False

    def up(self, height):
        print("retract telescope")
        time.sleep(height / 50)
        self._is_lowered = False
        print("telescope retracted")

    def down(self, height):
        print("lower telescope")
        time.sleep(height / 50)
        self._is_lowered = True
        print("telescope lowered")
