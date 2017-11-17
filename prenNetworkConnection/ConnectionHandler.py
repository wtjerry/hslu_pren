from prenNetworkConnection.CommandFactory import CommandFactory
from prenNetworkConnection.Decoder import Decoder


class ConnectionHandler(object):
    def handle(self, connection, client_address):
        try:
            data = connection.recv(1024)
            if data:
                command_data = Decoder().decode(data)
                command = CommandFactory().create(command_data)
                command.execute()
        finally:
            connection.close()
