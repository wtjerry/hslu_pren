class CommandData(object):
    def __init__(self, command_id, parameters):
        self.parameters = parameters
        self.command_id = command_id

    def __eq__(self, other):
        return isinstance(other, CommandData) \
               and self.command_id == other.command_id \
               and self.parameters == other.parameters
