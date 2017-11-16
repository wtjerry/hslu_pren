import io
import unittest
from unittest import mock

from prenNetworkConnection.NetworkStreamReader import NetworkStreamReader
from prenNetworkConnection.StartCommand import StartCommand


class NetworkStreamReaderTest(unittest.TestCase):
    def test_read(self):
        with mock.patch("prenNetworkConnection.NetworkStreamDecoder.NetworkStreamDecoder.decode") as decoder_mock, \
                mock.patch("prenNetworkConnection.CommandFactory.CommandFactory.create") as factory_mock:
            test_stream = io.BytesIO(b"some test data")
            test_data = "some test data"
            decoder_mock.return_value = test_data
            factory_mock.return_value = StartCommand()

            command = NetworkStreamReader().read(test_stream)

            self.assertIsInstance(command, StartCommand)
            decoder_mock.assert_called_with(test_stream)
            factory_mock.assert_called_with(test_data)
