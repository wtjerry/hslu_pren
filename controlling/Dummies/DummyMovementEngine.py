class DummyMovementEngine:
    def __init__(self):
        self.is_moving = False

    def start(self, speed):
        print("Started to move at speed", speed)
        self.is_moving = True

    def stop(self):
        print("stopped moving")
        self.is_moving = False

    def get_x(self):
        return 42
