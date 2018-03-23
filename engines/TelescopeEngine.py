class TelescopeEngine(object):
    _UP_COMMAND = "HSup"
    _DOWN_COMMAND = "HSdown"
    _GET_Z_COMMAND = "HSgetz"
    _communication = None

    def __init__(self, communication):
        self._communication = communication

    def up(self, mm):
        self._communication.execute(self._UP_COMMAND + mm)

    def down(self, mm):
        self._communication.execute(self._DOWN_COMMAND + mm)

    def get_z(self):
        z = self._communication.execute(self._GET_Z_COMMAND)
        return int(z)
