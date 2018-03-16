import socket

import time

from networking.ConnectionHandler import ConnectionHandler


class SocketServer(object):
    def __init__(self, address="localhost", port=12345):
        self.queue = []
        self._keep_socket_open = True
        self.address = address
        self.port = port

    def stop(self):
        self._keep_socket_open = False

    def start(self, start_function):
        print("starting socket server")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.address, self.port))
        sock.listen(1)

        print("waiting for a connection")
        try:
            connection, client_address = sock.accept()
            self._handle_connection(connection, start_function)
        except KeyboardInterrupt:
            sock.close()

    def _handle_connection(self, connection, start_function):
        data = connection.recv(1024)
        if self._contains_start_signal(data):
            start_function()
            while self._keep_socket_open:
                if len(self.queue) > 0:
                    connection.send(self.queue.pop())
                    time.sleep(0.5)

    @staticmethod
    def _contains_start_signal(data):
        return data == "start"
