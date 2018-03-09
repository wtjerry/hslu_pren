import random


class DummyXPosition:
    def __init__(self, movement):
        self.x_position = 0
        self._movement = movement

    def get_position(self):
        """
        Returns the current xPosition in mm.
        :rtype: int
        """
        if self._movement.is_moving:
            self.x_position += random.random() * 30

        return self.x_position
