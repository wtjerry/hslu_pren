import time


class ConnectionHandler(object):
    def __init__(self):
        self.queue = []
        self._keep_socket_open = True

    def stop(self):
        self._keep_socket_open = False

    def handle(self, connection, start_function):
        data = connection.recv(1024)
        if self._contains_start_signal(data):
            start_function()
            while self._keep_socket_open:
                if len(self.queue) > 0:
                    connection.send(self.queue.pop().encode())
                    time.sleep(0.25)
            connection.close()

    @staticmethod
    def _contains_start_signal(data):
        return data.decode() == "start\n"
