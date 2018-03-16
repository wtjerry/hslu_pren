import time


class DummyTargetDetection:
    listeners = []

    def __init__(self, target_function):
        self.target_found = target_function

    def start(self):
        print("searching target....")
        time.sleep(5)
        self.target_found()
