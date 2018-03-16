import unittest
from unittest.mock import MagicMock
from controlling.Logger import Logger


class LoggerTest(unittest.TestCase):
    def test_info(self):
        connection_handler_mock = MagicMock()
        queue_mock = MagicMock()
        connection_handler_mock.queue = queue_mock
        logger = Logger(connection_handler_mock)
        test_data = "test data"

        logger.info(test_data)

        queue_mock.append.assert_called_once_with(test_data)

    def test_major_step(self):
        connection_handler_mock = MagicMock()
        queue_mock = MagicMock()
        connection_handler_mock.queue = queue_mock
        logger = Logger(connection_handler_mock)
        test_data = "test data"

        logger.major_step(test_data)

        expected_data = "\n" \
            + "----------------------------" + "\n" \
            + test_data + "\n" \
            + "----------------------------" + "\n" \
            + "                            " + "\n"
        queue_mock.append.assert_called_once_with(expected_data)
