import time


class DummyStartSignalReceiver:
    def __init__(self, executor, start_function):
        self._executor = executor
        self._start_function = start_function

    @staticmethod
    def _startSocketServer():
        print("Started dummy listener")

    def start_listening(self):
        time.sleep(1)
        print("Start signal received")
        self._start_function()
