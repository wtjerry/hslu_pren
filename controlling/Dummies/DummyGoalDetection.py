import time


class DummyGoalDetection:
    listeners = []

    def __init__(self, goalfound_function):
        self.goal_found = goalfound_function

    def start(self):
        print("searching goal....")
        time.sleep(5)
        print("goal found!")
        self.goal_found()
