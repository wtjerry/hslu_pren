from prenNetworkConnection.CommandData import CommandData


class NetworkStreamReader(object):
    def read(self, stream):
        with stream as s:
            length = int(s.read(5))
            command_id = int(s.read(1).decode("utf8"))
            parameters = s.read(length-1).decode("utf8")
            return CommandData(command_id, parameters)
