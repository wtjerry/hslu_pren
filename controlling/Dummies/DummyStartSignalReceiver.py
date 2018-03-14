import time

class DummyStartSignalReceiver:
    def __init__(self, executor, start):
        self._executor = executor
        self._start_function = start

    @staticmethod
    def _startSocketServer():
        print("Started dummy listener")


    def StartListening(self):
        # if the start_function is not dispatched to another thread,
        # the socket server is blocked while the main algorithm is running
        # This is not desired once we need to send the current position back over the socket
        time.sleep(1)
        print("Start signal received")
        self._start_function()
