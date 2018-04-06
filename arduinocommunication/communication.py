import serial
import time


class Communication(object):
    _PORT = '/dev/ttyAMA0'
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
        print("Sending to Arduino: ", command)
        encoded_command = command.encode('utf-8')
        byteswritten = self._connection.write(encoded_command)

        if byteswritten == len(encoded_command):
            result = self._connection.readline().rstrip().decode('utf-8')
            print("Arduino returned ", result)
            return result
        else:
            raise IOError("Couldn't send to arduino!")
