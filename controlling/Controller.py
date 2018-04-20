import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Process

from controlling.AsyncProcessor import AsyncProcessor
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
    REVERT_MOVEMENT = 0
    START_DROP_ZONE = 900
    END_DROP_ZONE = 3300
    DISTANCE_TO_GOAL_STOP = 2
    DISTANCE_TO_GOAL_SLOWER = 50

    def __init__(self):
        self._executor = AsyncProcessor(ThreadPoolExecutor(max_workers=6))
        position_sender = self.get_position_sender()
        binding = Binding(position_sender)

        _goal_detection = binding.goal_detection

        self._movement = binding.movement_engine
        self._position = binding.position
        self._tilt_controller = binding.tilt_controller
        self._load_position_comparer = binding.load_position_comparer
        self._telescope = binding.telescope_engine
        self._magnet = binding.magnet
        self._goal_found = False

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
        self._executor.enqueue(self._on_start)

    def _on_start(self):
        self._logger.major_step("Switching to start")
        self._executor.enqueue(self._tilt_controller.start)
        self._executor.enqueue(self._position.start_calc_pos)
        self._move_until_load_reached()

    def _move_until_load_reached(self):
        self._logger.major_step("Moving to load")
        self._movement.start(self.MOVE_TO_LOAD_SPEED)
        self._load_position_comparer.check_until_reached()
        self._movement.stop()
        self._get_load()

    def _get_load(self):
        self._logger.major_step("Getting load")
        height = self._position.get_current_z()
        self._telescope.down(height)
        self._magnet.start()
        time.sleep(1)
        self._executor.enqueue(self._position.start_position_output)
        self._telescope.up(height)
        self._move_until_goal_reached()

    def _move_until_goal_reached(self):
        self._logger.major_step("Moving to goal")
        self._movement.start(self.SEARCH_GOAL_SPEED)
        self._search_goal_process.start()
        self._executor.enqueue(self._fail_safe)
        self._block_until_goal_found()

    def _block_until_goal_found(self):
        while not self._goal_found:
            value = self._queue.get()
            if value < self.DISTANCE_TO_GOAL_STOP:
                self._on_goal_found()
            elif value < self.DISTANCE_TO_GOAL_SLOWER:
                self._movement.set_speed(1)

    def _fail_safe(self):
        reverted = False

        while (not self._goal_found) and (not reverted):
            if self._position.get_current_x() >= self.END_DROP_ZONE:
                self._movement.set_speed(self.REVERT_MOVEMENT)
                reverted = True
            time.sleep(0.5)

        while (not self._goal_found) and reverted:
            if self._position.get_current_x() <= self.START_DROP_ZONE:
                self._movement.set_speed(self.SEARCH_GOAL_SPEED)
                reverted = False
            time.sleep(0.5)

    def _on_goal_found(self):
        self._logger.major_step("Goal found")
        self._goal_found = True
        self._movement.stop()
        self._deliver_load()

    def _deliver_load(self):
        self._logger.major_step("Delivering load")
        self._telescope.down(self._position.get_current_z())
        self._magnet.stop()
        time.sleep(2)
        self._movement.start(self.FINNISH_SPEED)
        self._position.stop_output()
        self._finish()

    def _finish(self):
        finished = False
        current_speed = self.FINNISH_SPEED;
        while not finished:
            print(self._position.get_current_x())
            if self._position.get_current_x() <= 3000 and current_speed != 5:
                self._movement.set_speed(5)
                current_speed = 5
            elif self._position.get_current_x() <= 3300 and current_speed != 3:
                self._movement.set_speed(3)
                current_speed = 3
            elif self._position.get_current_x() <= 3400 and current_speed != 1:
                self._movement.set_speed(1)
                current_speed = 1
            elif self._position.get_current_x() >= 3600:
                self._movement.stop()
                finished = True
            time.sleep(0.25)

        self._tilt_controller.stop()
        self._logger.major_step("Finished")
        time.sleep(1)
        self._socket_server.stop()
        exit()

    def stop_all(self):
        self._movement.stop()
        self._position.stop()
        self._tilt_controller.stop()
