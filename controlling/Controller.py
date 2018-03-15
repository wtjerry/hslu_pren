import time
from concurrent.futures import ThreadPoolExecutor

from controlling.Binding import Binding


class Controller(object):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        binding = Binding(self.executor, self.on_start, self.on_target_found)
        self.target_detection = binding.target_detection
        self._movement = binding.movement
        self.x_position = binding.x_position
        self._balancer = binding.balancer
        self.load_position_comparer = binding.load_position_comparer
        self.telescope = binding.telescope
        self.magnet = binding.magnet
        self.start_signal_receiver = binding.start_signal_receiver

    def listen_for_start(self):
        print("----------------------------")
        print("Listening for start")
        print("----------------------------")
        print("                            ")
        self.start_signal_receiver.start_listening()

    def on_start(self):
        print("----------------------------")
        print("switching to start now..")
        print("----------------------------")
        print("                            ")
        self.executor.submit(self._balancer.start)
        self._move_until_load_reached()

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
