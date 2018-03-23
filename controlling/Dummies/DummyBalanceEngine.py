import random
import time

import math


class DummyBalanceEngine:
    def __init__(self, pos):
        self._lookup_table = []
        self._position = pos
        self._should_balance = True

    def start(self):
        self.get_lookup_table()
        self.start_balancing()

    def stop(self):
        self._should_balance = False

    def get_lookup_table(self):
        for i in range(0, 34):
            self._lookup_table.append(random.random())

    def start_balancing(self):
        print("Start balancing")
        while self._should_balance:
            x_position = self._position.calculate_x()
            print("Korriegiere neigung: ", self._lookup_table[math.floor(x_position / 100)])
            time.sleep(1)
