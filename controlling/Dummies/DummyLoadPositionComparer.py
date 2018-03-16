import time


class DummyLoadPositionComparer:
    def __init__(self, x_pos):
        self._check_for_load = True
        self.x_position = x_pos

        # Load position in mm
        self._load_position = 650

    def check_until_reached(self):
        while self._check_for_load:
            position = self.x_position.get_position()
            if position >= self._load_position:
                print("Load Reached!")
                self._check_for_load = False
            else:
                print("goal not yet reached, position: ", position)

            time.sleep(0.5)
