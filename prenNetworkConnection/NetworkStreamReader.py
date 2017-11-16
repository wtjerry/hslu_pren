from prenNetworkConnection.CommandFactory import CommandFactory
from prenNetworkConnection.NetworkStreamDecoder import NetworkStreamDecoder


class NetworkStreamReader(object):
    def read(self, stream):
        command_data = NetworkStreamDecoder().decode(stream)
        return CommandFactory().create(command_data)
