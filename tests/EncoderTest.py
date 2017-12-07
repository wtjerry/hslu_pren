import unittest

from networking.Encoder import Encoder


class EncoderTest(unittest.TestCase):
    def test_encode_position(self):
        self.assertEqual(b"00003225", Encoder().position(2, 5))
        self.assertEqual(b"00003291", Encoder().position(9, 1))
        self.assertEqual(b"0000524455", Encoder().position(44, 55))
