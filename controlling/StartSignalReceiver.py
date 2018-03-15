from networking.CommandFactory import CommandFactory
from networking.IpProvider import get_wlan_ip_address
from networking.SocketServer import SocketServer


class StartSignalReceiver:
    def __init__(self, executor, start):
        self._executor = executor
        self._start_function = start

    @staticmethod
    def _startSocketServer():
        ip = get_wlan_ip_address()
        print("starting socket server")
        SocketServer(address=ip).start()

    def start_listening(self):
        # if the start_function is not dispatched to another thread,
        # the socket server is blocked while the main algorithm is running
        # This is not desired once we need to send the current position back over the socket
        CommandFactory.setup_start(self._start_function)
        self._executor.submit(self._startSocketServer)
