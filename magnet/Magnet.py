import RPi.GPIO as GPIO


class Magnet(object):
    _PIN = 17

    def __init__(self):
        """
        Constructor of the class.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._PIN, GPIO.OUT)

    def start(self):
        """
        Starts the magnet.
        """
        GPIO.output(self._PIN, GPIO.HIGH)

    def stop(self):
        """
        Stops the magnet.
        """
        GPIO.output(self._PIN, GPIO.LOW)
