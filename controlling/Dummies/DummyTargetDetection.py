import time

from controlling.processMessages import TARGET_FOUND


class DummyTargetDetection:
    listeners = []

    def start(self, queue):
        print("searching target....")
        time.sleep(5)
        queue.put(TARGET_FOUND)
