from controlling.Dummies.Balancer import Balancer
import time

from controlling.Dummies.GoalDetection import GoalDetection
from controlling.Dummies.LoadPositionComparer import LoadPositionComparer
from controlling.Dummies.Magnet import Magnet
from controlling.Dummies.Movement import Movement
from controlling.Dummies.Telescope import Telescope
from controlling.Dummies.sensors.DummyXPosition import DummyXPosition


class Controller(object):

    def __init__(self, executor):
        self.goal_detection = GoalDetection(self.goal_found)
        self.executor = executor
        self._movement = Movement()
        self.dummy_x_position = DummyXPosition(self._movement)
        self._balancer = Balancer(self.dummy_x_position)
        self.load_position_comparer = LoadPositionComparer(self.dummy_x_position)
        self.executor.submit(self._balancer.start)
        self.telescope = Telescope()
        self.magnet = Magnet()

    def switch_to_start(self):
        print("----------------------------")
        print("switching to start now..")
        print("----------------------------")
        print("                            ")
        self._move_until_load_reached()
        self._get_load()
        self._move_until_goal_reached()

    def _get_load(self):
        print("----------------------------")
        print("getting the load")
        print("----------------------------")
        print("                            ")
        self.telescope.down(100)
        self.magnet.activate()
        time.sleep(1)
        self.telescope.up(100)

    def _move_until_load_reached(self):
        print("----------------------------")
        print("Move until load reached")
        print("----------------------------")
        print("                            ")
        self._movement.start_moving()
        self.load_position_comparer.check_until_reached()
        self._movement.stop_moving()

    def _move_until_goal_reached(self):
        print("----------------------------")
        print("move until goal reached")
        print("----------------------------")
        print("                            ")
        self._movement.start_moving()
        self.executor.submit(self.goal_detection.start)

    def goal_found(self):
        print("----------------------------")
        print("Goal found!")
        print("----------------------------")
        print("                            ")
        print("Moving until goal reached")
        time.sleep(0.3)
        print("Goal reached")
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
        print("finished")

# States
#
# WaitForStart
## startsignalreceiver
# MoveToLoad
## movement
# GetLoad
## telescope
## positionoutput
## magnet
# SearchGoal
## movement
## positionoutput
# DeliverLoad
## telescope
## positionoutput
## magnet
# Finnish
## movement

