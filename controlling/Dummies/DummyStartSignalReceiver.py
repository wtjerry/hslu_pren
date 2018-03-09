import time

class DummyStartSignalReceiver:


    def __init__(self, start):
        self.start = start

    def StartListening(self):
        time.sleep(3)
        self.start()

        # StartListening
# Event Start