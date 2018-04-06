import time
from queue import Queue


class ConnectionHandler(object):
    def __init__(self):
        self._queue = Queue()
        self._keep_socket_open = True

    def stop(self):
        self._keep_socket_open = False

    def handle(self, connection, start_function):
        data = connection.recv(1024)
        if self._contains_start_signal(data):
            start_function()
            while self._keep_socket_open:
                if not self._queue.empty():
                    connection.send(self._queue.get().encode())
                    time.sleep(0.05)
            connection.close()

    def enqueue_message(self, message):
        self._queue.put(message)

    @staticmethod
    def _contains_start_signal(data):
        return data.decode() == "start\n"
