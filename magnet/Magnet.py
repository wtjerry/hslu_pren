import RPi.GPIO as GPIO


class Magnet(object):
    PIN = 17

    """
    Constructor of the class.
    """
    def __init__(self, yo):
        GPIO.setup(self.PIN, GPIO.OUT)

    """
    Starts the magnet.
    """
    def start(self):
        GPIO.output(self.PIN, GPIO.HIGH)

    """
    Stops the magnet.
    """
    def stop(self):
        GPIO.output(self.PIN, GPIO.LOW)
