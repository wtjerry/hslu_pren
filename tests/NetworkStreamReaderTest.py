import io
import unittest

from prenNetworkConnection.NetworkStreamReader import NetworkStreamReader


class NetworkStreamReaderTest(unittest.TestCase):
    def test_read(self):
        test_data = b"some test data"
        self.assertEqual(test_data, NetworkStreamReader().read(io.BytesIO(test_data)))

        other_test_data = b"other test data"
        self.assertEqual(other_test_data, NetworkStreamReader().read(io.BytesIO(other_test_data)))


if __name__ == '__main__':
    unittest.main()
