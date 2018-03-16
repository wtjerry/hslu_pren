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
        self._executor = ThreadPoolExecutor(max_workers=4)

        binding = Binding(self.on_target_found)
        self._target_detection = binding.target_detection
        self._movement = binding.movement
        self._x_position = binding.x_position
        self._balancer = binding.balancer
        self._load_position_comparer = binding.load_position_comparer
        self._telescope = binding.telescope
        self._magnet = binding.magnet

        ip = get_wlan_ip_address()
        connection_handler = ConnectionHandler()
        self._socket_server = SocketServer(connection_handler, address=ip)
        self._logger = Logger(connection_handler)
        self._position_sender = PositionSender(connection_handler)

    def listen_for_start(self):
        self._socket_server.start(self._enqueue_on_start)

    def _enqueue_on_start(self):
        self._executor.submit(self._on_start)

    def _on_start(self):
        self._logger.major_step("Switching to start")
        self._executor.submit(self._balancer.start)
        self._move_until_load_reached()

    def _move_until_load_reached(self):
        self._logger.major_step("Moving to load")
        self._position_sender.send(42, 1337)
        self._movement.start_moving()
        self._load_position_comparer.check_until_reached()
        self._movement.stop_moving()
        self._get_load()

    def _get_load(self):
        self._logger.major_step("Getting the load")
        self._telescope.down(100)
        self._magnet.start()
        time.sleep(1)
        self._telescope.up(100)
        self._move_until_target_reached()

    def _move_until_target_reached(self):
        self._logger.major_step("Moving to target")
        self._movement.start_moving()
        self._executor.submit(self._target_detection.start)

    def on_target_found(self):
        self._logger.major_step("Target found")
        time.sleep(0.3)
        self._movement.stop_moving()
        self._deliver_load()

    def _deliver_load(self):
        self._logger.major_step("Delivering Load")
        self._telescope.down(150)
        self._magnet.stop()
        time.sleep(0.5)
        self._movement.start_moving()
        time.sleep(1)
        self._movement.stop_moving()
        self._balancer.stop()
        self._logger.major_step("Finished")
        time.sleep(0.5)
        self._socket_server.stop()
