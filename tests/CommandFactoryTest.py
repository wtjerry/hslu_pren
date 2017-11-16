import unittest

from prenNetworkConnection.CommandData import CommandData
from prenNetworkConnection.CommandFactory import CommandFactory
from prenNetworkConnection.PositionCommand import PositionCommand
from prenNetworkConnection.StartCommand import StartCommand


class CommandFactoryTest(unittest.TestCase):
    def test_create_id1_creates_start_command(self):
        command = CommandFactory().create(CommandData(1, ""))
        self.assertIsInstance(command, StartCommand)

    def test_create_id2_creates_position_command(self):
        command = CommandFactory().create(CommandData(2, "1,2"))
        self.assertEqual(command, PositionCommand(1, 2))

        command = CommandFactory().create(CommandData(2, "333,0571"))
        self.assertEqual(command, PositionCommand(333, 571))
