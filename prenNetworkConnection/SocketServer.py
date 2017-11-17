import socket

from prenNetworkConnection.ConnectionHandler import ConnectionHandler


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
            connection, client_address = sock.accept()
            ConnectionHandler().handle(connection)


if __name__ == '__main__':
    SocketServer().start()
