import time

from controlling.Config import Config
from controlling.processMessages import GOAL_FOUND


class DummyGoalDetection:
    listeners = []
    _distance_to_goal = 100

    def start(self, queue):
        print("searching target....")
        time.sleep(2)
        queue.put(70)
        time.sleep(1)
        queue.put(55)
        time.sleep(0.5)
        queue.put(25)
        time.sleep(0.5)
        queue.put(12)
        time.sleep(0.5)
        queue.put(1)
