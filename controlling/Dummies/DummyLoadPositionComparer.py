import time


class DummyLoadPositionComparer:
    def __init__(self, pos):
        self._check_for_load = True
        self._position = pos

        # Load position in mm
        self._load_position = 650

    def check_until_reached(self):
        while self._check_for_load:
            position = self._position.calculate_x()
            if position >= self._load_position:
                print("Load Reached!")
                self._check_for_load = False
            else:
                print("goal not yet reached, position: ", position)

            time.sleep(0.5)
