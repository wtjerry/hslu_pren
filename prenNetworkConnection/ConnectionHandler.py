from prenNetworkConnection.CommandFactory import CommandFactory
from prenNetworkConnection.Decoder import Decoder


class ConnectionHandler(object):
    def handle(self, connection, client_address):
        try:
            data = connection.recv(1024)
            if data:
                command_id, parameter = Decoder().decode(data)
                command = CommandFactory().create(command_id, parameter)
                command.execute()
        finally:
            connection.close()
