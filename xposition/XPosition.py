import time
import VL53L0X
import RPi.GPIO as GPIO


class XPosition(object):
    _TRACK_LENGTH = 3500

    _FRONT_SENSOR_PIN = 20
    _FRONT_SENSOR_ADDRESS = 0x2B
    _FRONT_SENSOR = None
    _FRONT_SENSOR_DISTANCE_TO_CENTER = 197.5
    _FRONT_SENSOR_CACHED_VALUE = 0

    _BACK_SENSOR_PIN = 16
    _BACK_SENSOR_ADDRESS = 0x2D
    _BACK_SENSOR = None
    _BACK_SENSOR_DISTANCE_TO_CENTER = 177
    _BACK_SENSOR_CACHED_VALUE = 0

    def __init__(self):
        """
        Constructor of the class.
        """

        # Setup pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._FRONT_SENSOR_PIN, GPIO.OUT)
        GPIO.setup(self._BACK_SENSOR_PIN, GPIO.OUT)

        # Turn off each sensor to reset
        GPIO.output(self._FRONT_SENSOR_PIN, GPIO.LOW)
        GPIO.output(self._BACK_SENSOR_PIN, GPIO.LOW)

        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.5)

        # Create the sensor objects
        self._FRONT_SENSOR = VL53L0X.VL53L0X(address=self._FRONT_SENSOR_ADDRESS)
        self._BACK_SENSOR = VL53L0X.VL53L0X(address=self._BACK_SENSOR_ADDRESS)

    def start(self):
        """
        Starts the position sensors.
        """
        GPIO.output(self._FRONT_SENSOR_PIN, GPIO.HIGH)
        GPIO.output(self._BACK_SENSOR_PIN, GPIO.HIGH)

        time.sleep(0.5)

        self._FRONT_SENSOR.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self._BACK_SENSOR.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    def get_position(self):
        """
        Returns the current xPosition in mm.
        :rtype: int
        """
        return (self._get_back_sensor_measurement() + self._get_front_sensor_measurement()) / 2

    def _get_front_sensor_measurement(self):
        """
        Returns the front sensor measurement in mm.
        :rtype: int
        """
        measurement = self._FRONT_SENSOR.get_distance() / 10

        if measurement > 0:
            self._FRONT_SENSOR_CACHED_VALUE = measurement

        return self._TRACK_LENGTH - self._FRONT_SENSOR_CACHED_VALUE - self._FRONT_SENSOR_DISTANCE_TO_CENTER

    def _get_back_sensor_measurement(self):
        """
        Returns the back sensor measurement in mm.
        :rtype: int
        """
        measurement = self._BACK_SENSOR.get_distance() / 10

        if measurement > 0:
            self._BACK_SENSOR_CACHED_VALUE = measurement

        return self._BACK_SENSOR_CACHED_VALUE + self._BACK_SENSOR_DISTANCE_TO_CENTER
