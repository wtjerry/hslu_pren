import time
from concurrent.futures import ThreadPoolExecutor

from controlling.Binding import Binding
from networking.IpProvider import get_wlan_ip_address
from networking.SocketServer import SocketServer


class Controller(object):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._socket_server_executor = ThreadPoolExecutor(max_workers=1)
        binding = Binding(self.executor, self.on_start, self.on_target_found)
        self.target_detection = binding.target_detection
        self._movement = binding.movement
        self.x_position = binding.x_position
        self._balancer = binding.balancer
        self.load_position_comparer = binding.load_position_comparer
        self.telescope = binding.telescope
        self.magnet = binding.magnet
        ip = get_wlan_ip_address()
        self._socket_server = SocketServer(address=ip)

    def _startSocketServer(self):
        self._socket_server.start(self._on_start)

    def listen_for_start(self):
        print("----------------------------")
        print("Listening for start")
        print("----------------------------")
        print("                            ")
        self._socket_server_executor.submit(self._startSocketServer)

    def _on_start(self):
        print("----------------------------")
        print("switching to start now..")
        print("----------------------------")
        print("                            ")
        self.executor.submit(self._balancer.start)
        self._move_until_load_reached()
        self._socket_server.queue.append("+++++++++++++++++++++++++++++++++++++")

    def _move_until_load_reached(self):
        print("----------------------------")
        print("Move until load reached")
        print("----------------------------")
        print("                            ")
        self._movement.start_moving()
        self.load_position_comparer.check_until_reached()
        self._movement.stop_moving()
        self._get_load()

    def _get_load(self):
        print("----------------------------")
        print("getting the load")
        print("----------------------------")
        print("                            ")
        self.telescope.down(100)
        self.magnet.activate()
        time.sleep(1)
        self.telescope.up(100)
        self._move_until_target_reached()

    def _move_until_target_reached(self):
        print("----------------------------")
        print("move until target reached")
        print("----------------------------")
        print("                            ")
        self._movement.start_moving()
        self.executor.submit(self.target_detection.start)

    def on_target_found(self):
        print("----------------------------")
        print("Target found!")
        print("----------------------------")
        print("                            ")
        print("Moving until target reached")
        time.sleep(0.3)
        print("Target reached")
        self._movement.stop_moving()
        self._deliver_load()

    def _deliver_load(self):
        print("----------------------------")
        print("Deliver Load")
        print("----------------------------")
        print("                            ")
        self.telescope.down(150)
        self.magnet.deactivate()
        time.sleep(0.5)
        print("move until finnished")
        self._movement.start_moving()
        time.sleep(1)
        self._movement.stop_moving()
        print("finished")
