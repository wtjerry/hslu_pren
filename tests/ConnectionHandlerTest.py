import unittest
from unittest.mock import MagicMock

from prenNetworkConnection.ConnectionHandler import ConnectionHandler


class ConnectionHandlerTest(unittest.TestCase):
    def test_handle(self):
        connection_mock = MagicMock()
        test_data = b"hello world"
        connection_mock.recv.return_value = test_data

        ConnectionHandler().handle(connection_mock, "client address")

        connection_mock.sendall.assert_called_once_with(test_data)

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
