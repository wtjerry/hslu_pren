
class Movement:
    def __init__(self):
        self.is_moving = False

    def start_moving(self):
        print("Started to move")
        self.is_moving = True

    def stop_moving(self):
        print("stopped moving")
        self.is_moving = False

# Start Moving
# Stop Moving