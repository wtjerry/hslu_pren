from time import sleep
from math import floor
from random import random

class TiltController:
    def __init__(self, pos, tilt_engine):
        self._lookup_table = []
        self._position = pos
        self._should_balance = True
        self._tile_engine = tilt_engine

    def start(self):
        self.get_lookup_table()
        self.start_balancing()

    def stop(self):
        self._should_balance = False

    def get_lookup_table(self):
        for i in range(0, 34):
            self._lookup_table.append(random())

    def start_balancing(self):
        print("Start balancing")
        while self._should_balance:
            x_position = self._position.calculate_x()
            self._tile_engine.correct(self._lookup_table[floor(x_position / 100)])
            sleep(1)
