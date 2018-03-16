import time
from concurrent.futures import ThreadPoolExecutor

from controlling.Binding import Binding
from controlling.Logger import Logger
from networking.ConnectionHandler import ConnectionHandler
from networking.IpProvider import get_wlan_ip_address
from networking.PositionSender import PositionSender
from networking.SocketServer import SocketServer


class Controller(object):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        binding = Binding(self.on_target_found)
        self.target_detection = binding.target_detection
        self._movement = binding.movement
        self.x_position = binding.x_position
        self._balancer = binding.balancer
        self.load_position_comparer = binding.load_position_comparer
        self.telescope = binding.telescope
        self.magnet = binding.magnet
        ip = get_wlan_ip_address()
        handler = ConnectionHandler()
        self._socket_server = SocketServer(handler, address=ip)
        self._logger = Logger(handler)
        self._position_sender = PositionSender(handler)

    def listen_for_start(self):
        print("----------------------------")
        print("Listening for start")
        print("----------------------------")
        print("                            ")
        self._socket_server.start(self._enqueue_on_start)

    def _enqueue_on_start(self):
        self.executor.submit(self._on_start)

    def _on_start(self):
        print("----------------------------")
        print("switching to start now..")
        print("----------------------------")
        print("                            ")
        self.executor.submit(self._balancer.start)
        self._move_until_load_reached()

    def _move_until_load_reached(self):
        self._logger.major_step("Move until load reached")
        self._position_sender.send(42, 1337)
        self._movement.start_moving()
        self.load_position_comparer.check_until_reached()
        self._movement.stop_moving()
        self._get_load()

    def _get_load(self):
        self._logger.major_step("getting the load")
        self.telescope.down(100)
        self.magnet.start()
        time.sleep(1)
        self.telescope.up(100)
        self._move_until_target_reached()

    def _move_until_target_reached(self):
        self._logger.major_step("move until target reached")
        self._movement.start_moving()
        self.executor.submit(self.target_detection.start)

    def on_target_found(self):
        self._logger.major_step("Target found!")
        time.sleep(0.3)
        self._movement.stop_moving()
        self._deliver_load()

    def _deliver_load(self):
        self._logger.major_step("Deliver Load")
        self.telescope.down(150)
        self.magnet.stop()
        time.sleep(0.5)
        print("move until finnished")
        self._movement.start_moving()
        time.sleep(1)
        self._movement.stop_moving()
        self._balancer.stop()
        self._logger.major_step("finished")
        time.sleep(0.5)
        self._socket_server.stop()
