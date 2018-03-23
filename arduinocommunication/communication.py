import serial
import time


class Communication(object):
    _PORT = '/dev/ttyACM0'
    _BAUDRATE = 115200
    _TIMEOUT = None
    _COMMAND_TERMINATOR = ";"

    def __init__(self):
        self._connection = serial.Serial(self._PORT, self._BAUDRATE, timeout=self._TIMEOUT)
        time.sleep(2)

    def execute(self, command):
        """
        Sends a given command over the serial communication line.
        :param command: The command to send.
        :return: A string with the return message.
        """
        command = command + self._COMMAND_TERMINATOR
        encoded_command = command.encode('utf-8')
        byteswritten = self._connection.write(encoded_command)

        if byteswritten == len(encoded_command):
            return self._connection.readline().rstrip().decode('utf-8')
        else:
            raise IOError("Couldn't send to arduino!")
