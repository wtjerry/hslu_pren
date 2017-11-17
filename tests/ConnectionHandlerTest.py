import unittest
from unittest import mock
from unittest.mock import MagicMock

from prenNetworkConnection.ConnectionHandler import ConnectionHandler


class ConnectionHandlerTest(unittest.TestCase):
    def test_handle(self):
        with mock.patch("prenNetworkConnection.Decoder.Decoder.decode") as decoder_mock, \
                mock.patch("prenNetworkConnection.CommandFactory.CommandFactory.create") as factory_mock:
            test_stream = b"hello world"
            connection_mock = MagicMock()
            connection_mock.recv.return_value = test_stream

            command_id = 999
            command_parameter = "parameter"
            decoder_mock.return_value = (command_id, command_parameter)

            command_mock = MagicMock()
            factory_mock.return_value = command_mock

            ConnectionHandler().handle(connection_mock, "client address")

            decoder_mock.assert_called_with(test_stream)
            factory_mock.assert_called_with(command_id, command_parameter)
            self.assertTrue(command_mock.execute.called)
