import unittest

from prenNetworkConnection.CommandData import CommandData
from prenNetworkConnection.Decoder import Decoder


class DecoderTest(unittest.TestCase):
    def test_decode(self):
        test_data_with_length = b"00011" + b"1" + b"123 567 90"
        actual_command_data = Decoder().decode(test_data_with_length)
        self.assertEqual(CommandData(1, "123 567 90"), actual_command_data)

        test_data_with_length = b"00013" + b"5" + b"abc def ghij"
        actual_command_data = Decoder().decode(test_data_with_length)
        self.assertEqual(CommandData(5, "abc def ghij"), actual_command_data)

    def test_decode_data_to_short(self):
        test_data_with_length = b"00011" + b"1" + b"123 5"
        with self.assertRaises(ValueError):
            Decoder().decode(test_data_with_length)

    def test_decode_data_to_long(self):
        test_data_with_length = b"00011" + b"1" + b"123 567 901 23"
        with self.assertRaises(ValueError):
            Decoder().decode(test_data_with_length)
