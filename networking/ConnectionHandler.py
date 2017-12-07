from networking.CommandFactory import CommandFactory
from networking.Decoder import Decoder


class ConnectionHandler(object):
    def handle(self, connection):
        try:
            data = connection.recv(1024)
            if data:
                command_id, parameter = Decoder().decode(data)
                command = CommandFactory().create(command_id, parameter)
                command.execute()
        except ValueError as e:
            print(e)
            connection.close
        finally:
            connection.close()
