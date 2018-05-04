from controlling.Config import Config


class TelescopeEngine(object):
    _UP_COMMAND = "HSup"
    _DOWN_COMMAND = "HSdn"
    _GET_Z_COMMAND = "HSgetz"
    _communication = None

    def __init__(self, communication):
        self._z = 0
        self._communication = communication

    def up(self, mm):
        mm_formatted = self._get_formatted_mm(mm)
        self._communication.execute_multiple_return(self._UP_COMMAND + str(mm_formatted), self.set_z)

    def down(self, mm):
        mm_formatted = self._get_formatted_mm(mm)
        self._communication.execute_multiple_return(self._DOWN_COMMAND + str(mm_formatted), self.set_z)

    def get_z(self):
        return self._z

    def set_z(self, new_z):
        self._z = int(new_z)

    def _get_formatted_mm(self, mm):
        mm_string = str(mm)
        while len(mm_string) < 3:
            mm_string = "0" + mm_string
        return mm_string