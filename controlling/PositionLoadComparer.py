import time

from controlling.Config import Config


class PositionLoadComparer(object):
    def __init__(self, pos):
        self._check_for_load = True
        self._position = pos
        # Load position in mm

    def check_until_reached(self):
        while self._check_for_load:
            position = self._position.get_current_x()
            if position >= Config.COMPARER_LOAD_POSITION:
                print("Load Reached!")
                self._check_for_load = False
            else:
                print("load  not yet reached, position: ", position)

            time.sleep(0.05)
