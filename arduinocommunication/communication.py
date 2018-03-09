import serial
import sys


class Communication(object):
    _connection = None
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
        byteswritten = self._connection.write(command.encode('utf-8'))

        if byteswritten == sys.getsizeof(command.encode('utf-8')):
            return self._connection.read(2)
        else:
            raise IOError("Couldn't send to arduino!")
