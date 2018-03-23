class TiltEngine(object):
    _CORRECT_COMMAND = "WIcorrect"
    _communication = None

    def __init__(self, communication):
        self._communication = communication

    def correct(self, degrees):
        self._communication.execute(self._CORRECT_COMMAND + degrees)
