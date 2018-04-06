import unittest
from unittest.mock import MagicMock
from networking.PositionSender import PositionSender


class PositionSenderTest(unittest.TestCase):
    def test_send(self):
        connection_handler_mock = MagicMock()
        sender = PositionSender(connection_handler_mock)
        x = 42
        z = 1337

        sender.send(x, z)

        expected_data = "new position x: '{x}' z: '{z}'\n".format(x=x, z=z)
        connection_handler_mock.enqueue_message.assert_called_once_with(expected_data)
