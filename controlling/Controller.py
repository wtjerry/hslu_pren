import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Process

from controlling.Binding import Binding
from controlling.Logger import Logger
from controlling.processMessages import GOAL_FOUND
from networking.ConnectionHandler import ConnectionHandler
from networking.IpProvider import get_wlan_ip_address
from networking.PositionSender import PositionSender
from networking.SocketServer import SocketServer


class Controller(object):
    MOVE_TO_LOAD_SPEED = 4
    SEARCH_GOAL_SPEED = 2
    FINNISH_SPEED = 1

    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=4)
        position_sender = self.get_position_sender()
        binding = Binding(position_sender)

        _goal_detection = binding.goal_detection

        self._movement = binding.movement_engine
        self._position = binding.position
        self._tilt_controller = binding.tilt_controller
        self._load_position_comparer = binding.load_position_comparer
        self._telescope = binding.telescope_engine
        self._magnet = binding.magnet

        self._queue = Queue()
        self._search_goal_process = Process(target=_goal_detection.start, args=(self._queue,))

    def get_position_sender(self):
        ip = get_wlan_ip_address()
        connection_handler = ConnectionHandler()
        self._socket_server = SocketServer(connection_handler, address=ip)
        self._logger = Logger(connection_handler)
        position_sender = PositionSender(connection_handler)
        return position_sender

    def listen_for_start(self):
        self._socket_server.start(self._enqueue_on_start)

    def _enqueue_on_start(self):
        self._executor.submit(self._on_start)

    def _on_start(self):
        self._logger.major_step("Switching to start")
        self._executor.submit(self._tilt_controller.start)
        self._executor.submit(self._position.start_calc_pos)
        self._move_until_load_reached()

    def _move_until_load_reached(self):
        self._logger.major_step("Moving to load")
        self._movement.start_moving(self.MOVE_TO_LOAD_SPEED)
        self._load_position_comparer.check_until_reached()
        self._movement.stop_moving()
        self._get_load()

    def _get_load(self):
        self._logger.major_step("Getting load")
        height = self._position.get_current_z()
        self._telescope.down(height)
        self._magnet.start()
        time.sleep(1)
        self._executor.submit(self._position.start_position_output)
        self._telescope.up(height)
        self._move_until_goal_reached()

    def _move_until_goal_reached(self):
        self._logger.major_step("Moving to goal")
        self._movement.start_moving(self.SEARCH_GOAL_SPEED)
        self._search_goal_process.start()
        self._block_until_goal_found()

    def _block_until_goal_found(self):
        if self._queue.get() == GOAL_FOUND:
            self._on_goal_found()

    def _on_goal_found(self):
        self._logger.major_step("Goal found")
        time.sleep(0.3)
        self._movement.stop_moving()
        self._deliver_load()

    def _deliver_load(self):
        self._logger.major_step("Delivering load")
        self._telescope.down(self._position.get_current_z())
        self._magnet.stop()
        time.sleep(2)
        self._position.stop()
        self._movement.start_moving(self.FINNISH_SPEED)
        time.sleep(0.5)
        self._finish()

    def _finish(self):
        self._tilt_controller.stop()
        self._logger.major_step("Finished")
        time.sleep(1)
        self._socket_server.stop()
        exit()
