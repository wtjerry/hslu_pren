from networking.CommandFactory import CommandFactory
from networking.IpProvider import get_wlan_ip_address
from networking.SocketServer import SocketServer


class StartSignalReceiver:
    def __init__(self, executor, start_function, enqueue_for_send_function):
        self._executor = executor
        self._start_function = start_function
        self._enqueue_for_send_function = enqueue_for_send_function

    def _startSocketServer(self):
        ip = get_wlan_ip_address()
        print("starting socket server")
        SocketServer(address=ip).start(self._start_function, self._enqueue_for_send_function)

    def start_listening(self):
        self._executor.submit(self._startSocketServer)
