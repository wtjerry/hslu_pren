import socket

import time

from networking.ConnectionHandler import ConnectionHandler


class SocketServer(object):
    def __init__(self, address="localhost", port=12345):
        self.queue = []
        self._keep_socket_open = True
        self._sock = None
        self.address = address
        self.port = port

    def stop(self):
        self._keep_socket_open = False
        if self._sock:
            self._sock.close()

    def start(self, start_function):
        print("starting socket server")
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.bind((self.address, self.port))
            self._sock.listen(1)
            print("waiting for a connection")

            connection, client_address = self._sock.accept()
            self._handle_connection(connection, start_function)
        except KeyboardInterrupt as ex:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
            print(ex)
        print("socket server stopped")

    def _handle_connection(self, connection, start_function):
        data = connection.recv(1024)
        if self._contains_start_signal(data):
            start_function()
            while self._keep_socket_open:
                if len(self.queue) > 0:
                    connection.send(self.queue.pop().encode())
                    time.sleep(0.5)
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
            print("connection closed")

    @staticmethod
    def _contains_start_signal(data):
        return data.decode() == "start\n"
