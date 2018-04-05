import time

from controlling.processMessages import GOAL_FOUND


class DummyGoalDetection:
    listeners = []

    def start(self, queue):
        print("searching target....")
        time.sleep(5)
        queue.put(GOAL_FOUND)
