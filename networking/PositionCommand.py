class PositionCommand(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, PositionCommand) \
               and self.x == other.x \
               and self.y == other.y
