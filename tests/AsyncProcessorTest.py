import unittest
from unittest.mock import MagicMock, patch, call

from controlling.AsyncProcessor import AsyncProcessor

_EXCEPTION_TEXT = "something horrible went wrong"


class AsyncProcessorTest(unittest.TestCase):
    def test_enqueue_submits_action_to_ThreadPool(self):
        thread_pool_mock = MagicMock()
        asyncProcessor = AsyncProcessor(thread_pool_mock)

        asyncProcessor.enqueue(self._some_action)

        assert thread_pool_mock.submit.called

    @patch("builtins.print", autospec=True, side_effect=print)
    def test_enqueue_prints_exception_if_action_raises_one(self, print_mock):
        thread_pool_mock = MagicMock()
        asyncProcessor = AsyncProcessor(thread_pool_mock)
        thread_pool_mock.submit = lambda action, parameter: action(parameter)

        asyncProcessor.enqueue(self._raise_exception)

        calls = [call("*** EXCEPTION IN THREAD ***"), call(_EXCEPTION_TEXT)]
        print_mock.assert_has_calls(calls)

    def _raise_exception(self):
        raise Exception(_EXCEPTION_TEXT)

    def _some_action(self):
        print("hello world")
