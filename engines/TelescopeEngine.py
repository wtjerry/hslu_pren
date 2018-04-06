class TelescopeEngine(object):
    _UP_COMMAND = "HSup"
    _DOWN_COMMAND = "HSdn"
    _GET_Z_COMMAND = "HSgetz"
    _communication = None

    def __init__(self, communication):
        self._communication = communication

    def up(self, mm):
        mm_formatted = self._get_formatted_mm(mm)
        self._communication.execute(self._UP_COMMAND + str(mm_formatted))

    def down(self, mm):
        mm_formatted = self._get_formatted_mm(mm)
        self._communication.execute(self._DOWN_COMMAND + str(mm_formatted))

    def get_z(self):
        z = self._communication.execute(self._GET_Z_COMMAND)
        return int(z)

    def _get_formatted_mm(self, mm):
        mm_string = str(mm)
        while len(mm_string) < 3:
            mm_string = "0" + mm_string
        return mm_string