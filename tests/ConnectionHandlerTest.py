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

            test_data = "some test data"
            decoder_mock.return_value = test_data

            command_mock = MagicMock()
            factory_mock.return_value = command_mock

            ConnectionHandler().handle(connection_mock, "client address")

            decoder_mock.assert_called_with(test_stream)
            factory_mock.assert_called_with(test_data)
            self.assertTrue(command_mock.execute.called)

    def test_handle_with_empty_data_received(self):
        connection_mock = MagicMock()
        test_data = b""
        connection_mock.recv.return_value = test_data

        ConnectionHandler().handle(connection_mock, "client address")

        connection_mock.sendall.assert_not_called()

    def test_handle_with_no_data_received(self):
        connection_mock = MagicMock()
        connection_mock.recv.return_value = None

        ConnectionHandler().handle(connection_mock, "client address")

        connection_mock.sendall.assert_not_called()
