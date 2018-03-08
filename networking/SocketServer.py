import socket
from networking.ConnectionHandler import ConnectionHandler


class SocketServer(object):
    def __init__(self, address="localhost", port=12345):
        self.address = address
        self.port = port

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.address, self.port))
        sock.listen(1)

        while True:
            print("waiting for a connection")
            try:
                connection, client_address = sock.accept()
            except KeyboardInterrupt:
                sock.close()
                break
            ConnectionHandler().handle(connection)
