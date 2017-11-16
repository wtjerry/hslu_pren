import io
import unittest

from prenNetworkConnection.CommandData import CommandData
from prenNetworkConnection.NetworkStreamReader import NetworkStreamReader


class NetworkStreamReaderTest(unittest.TestCase):
    def test_read(self):
        test_data_with_length = b"00011" + b"1" + b"123 567 90"
        actual_command_data = NetworkStreamReader().read(io.BytesIO(test_data_with_length))
        self.assertEqual(CommandData(1, "123 567 90"), actual_command_data)

        test_data_with_length = b"00013" + b"5" + b"abc def ghij"
        actual_command_data = NetworkStreamReader().read(io.BytesIO(test_data_with_length))
        self.assertEqual(CommandData(5, "abc def ghij"), actual_command_data)


if __name__ == '__main__':
    unittest.main()
