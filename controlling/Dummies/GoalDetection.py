import random
import time

class GoalDetection:
    listeners = []

    def __init__(self, goalfound):
        self.goal_found = goalfound

    def start(self):
        print("searching goal....")
        time.sleep(5)
        print("goal found!")
        self.goal_found()



# start
# event GoalDetected