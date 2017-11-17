import unittest
from unittest import mock
from unittest.mock import MagicMock

from prenNetworkConnection.ConnectionHandler import ConnectionHandler


class IntegrationTest(unittest.TestCase):
    def test_connection_handling(self):
        with mock.patch("prenNetworkConnection.StartCommand.StartCommand.execute") as start_signal_mock:
            connection_mock = MagicMock()
            test_data = b"000011"
            connection_mock.recv.return_value = test_data

            ConnectionHandler().handle(connection_mock)

            self.assertTrue(start_signal_mock.called)
