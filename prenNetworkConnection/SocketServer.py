import os
import socket
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prenNetworkConnection.ConnectionHandler import ConnectionHandler
from prenNetworkConnection.IpProvider import get_wlan_ip_address


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


if __name__ == '__main__':
    ip = get_wlan_ip_address()
    SocketServer(address=ip).start()
