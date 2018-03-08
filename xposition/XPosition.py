import time
import sys
import RPi.GPIO as GPIO

sys.path.append("../py_libs/VL53L0X_rasp_python/python/")
import VL53L0X


class XPosition(object):
    _TRACK_LENGTH = 3500

    _BACK_SENSOR_PIN = 16
    _BACK_SENSOR_ADDRESS = 0x2D
    _BACK_SENSOR_DISTANCE_TO_CENTER = 177
    _back_sensor = None
    _back_sensor_cached_value = 137

    _FRONT_SENSOR_PIN = 20
    _FRONT_SENSOR_ADDRESS = 0x2B
    _FRONT_SENSOR_DISTANCE_TO_CENTER = 197.5
    _front_sensor = None
    _front_sensor_cached_value = _TRACK_LENGTH - _back_sensor_cached_value - \
                                 _BACK_SENSOR_DISTANCE_TO_CENTER - _FRONT_SENSOR_DISTANCE_TO_CENTER

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
        self._front_sensor = VL53L0X.VL53L0X(address=self._FRONT_SENSOR_ADDRESS)
        self._back_sensor = VL53L0X.VL53L0X(address=self._BACK_SENSOR_ADDRESS)

    def start(self):
        """
        Starts the position sensors.
        """
        GPIO.output(self._FRONT_SENSOR_PIN, GPIO.HIGH)
        GPIO.output(self._BACK_SENSOR_PIN, GPIO.HIGH)

        time.sleep(0.5)

        self._front_sensor.start_ranging(VL53L0X.VL53L0X_LONG_RANGE_MODE)
        self._back_sensor.start_ranging(VL53L0X.VL53L0X_LONG_RANGE_MODE)

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
        measurement = self._front_sensor.get_distance()

        if measurement > 0 and 8000 < measurement:
            self._front_sensor_cached_value = measurement

        return self._TRACK_LENGTH - self._front_sensor_cached_value - self._FRONT_SENSOR_DISTANCE_TO_CENTER

    def _get_back_sensor_measurement(self):
        """
        Returns the back sensor measurement in mm.
        :rtype: int
        """
        measurement = self._back_sensor.get_distance()

        if measurement > 0 and 8000 < measurement:
            self._back_sensor_cached_value = measurement

        return self._back_sensor_cached_value + self._BACK_SENSOR_DISTANCE_TO_CENTER
