import unittest
from unittest import mock
from unittest.mock import MagicMock
from networking.SocketServer import SocketServer


class SocketServerTest(unittest.TestCase):
    @unittest.skip(
        'This is an example test how to work with mocks. '
        'It will not work as the tested code uses an endless loop.')
    def test_start(self):
        with mock.patch("socket.socket") as socket_ctor_mock:
            local_socket_mock = MagicMock()

            socket_ctor_mock.return_value = local_socket_mock
            connection_mock = MagicMock()
            local_socket_mock.accept.return_value = (connection_mock, "client address")

            expected_address = "someAddress"
            expected_port = 9999
            server = SocketServer(address=expected_address, port=expected_port)
            server.start(lambda: print("starting now.."))

            local_socket_mock.bind.assert_called_once_with((expected_address, expected_port))
            local_socket_mock.listen.assert_called_once_with(1)
