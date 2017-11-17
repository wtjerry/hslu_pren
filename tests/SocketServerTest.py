import unittest
from unittest import mock
from unittest.mock import MagicMock

from prenNetworkConnection.socketserver import SocketServer


class SocketServerTest(unittest.TestCase):
    def test_start(self):
        with mock.patch("socket.socket") as socket_ctor_mock:
            local_socket_mock = MagicMock()

            socket_ctor_mock.return_value = local_socket_mock
            local_socket_mock.accept.return_value = (MagicMock(), "addr")

            expected_address = "someAddress"
            expected_port = 9999
            abc = SocketServer(address=expected_address, port=expected_port)
            abc.start()

            local_socket_mock.bind.assert_called_once_with((expected_address, expected_port))
            local_socket_mock.listen.assert_called_once_with(1)
