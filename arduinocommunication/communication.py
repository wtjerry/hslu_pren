import serial
import sys


class Communication(object):
    _PORT = '/dev/ttyACM0'
    _BAUDRATE = 115200
    _TIMEOUT = None

    def __init__(self):
        self._connection = serial.Serial(self._PORT, self._BAUDRATE, timeout=self._TIMEOUT)

    def execute(self, command):
        """
        Sends a given command over the serial communication line.
        :param command: The command to send.
        :return: A bytearray with the return message.
        """
        encoded_command = command.encode('utf-8')
        byteswritten = self._connection.write(encoded_command)

        if byteswritten == sys.getsizeof(encoded_command):
            return self._connection.read(2)
        else:
            raise IOError("Couldn't send to arduino!")
