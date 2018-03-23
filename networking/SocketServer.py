import socket


class SocketServer(object):
    def __init__(self, connection_handler, address="localhost", port=12345):
        self._sock = None
        self._connectionHandler = connection_handler
        self.address = address
        self.port = port

    def stop(self):
        self._connectionHandler.stop()
        if self._sock:
            self._sock.close()

    def start(self, start_function):
        print("starting socket server")
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._sock.bind((self.address, self.port))
            self._sock.listen(1)
            print("waiting for a connection")
            connection, client_address = self._sock.accept()
            self._connectionHandler.handle(connection, start_function)
        except KeyboardInterrupt as ex:
            self._sock.close()
            print(ex)
        print("socket server stopped")
