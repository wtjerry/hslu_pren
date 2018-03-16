from controlling.Dummies.Dummy import Dummy
from controlling.Dummies.DummyBalancer import DummyBalancer
from controlling.Dummies.DummyTargetDetection import DummyTargetDetection
from controlling.Dummies.DummyLoadPositionComparer import DummyLoadPositionComparer
from controlling.Dummies.DummyMagnet import DummyMagnet
from controlling.Dummies.DummyMovement import DummyMovement
from controlling.Dummies.DummyStartSignalReceiver import DummyStartSignalReceiver
from controlling.Dummies.DummyTelescope import DummyTelescope
from controlling.Dummies.sensors.DummyXPosition import DummyXPosition
from controlling.StartSignalReceiver import StartSignalReceiver


class Binding:
    use_real_balancer = False
    use_real_goal_detection = False
    use_real_load_position_comparer = False
    use_real_magnet = False
    use_real_movement = False
    use_real_position_calculator = False
    use_real_position_output = False
    use_real_telescope = False
    use_real_x_position = False
    use_real_socket_server = False

    def __init__(self, executor, start_function, goalfound_function):
        # TODO replace Dummy(), it raises an error when initialized
        self.movement = Dummy() if self.use_real_movement else DummyMovement()
        self.x_position = Dummy() if self.use_real_x_position else DummyXPosition(self.movement)
        self.balancer = Dummy() if self.use_real_balancer else DummyBalancer(self.x_position)
        self.target_detection = Dummy() if self.use_real_goal_detection else DummyTargetDetection(goalfound_function)
        self.load_position_comparer = Dummy() if self.use_real_load_position_comparer \
            else DummyLoadPositionComparer(self.x_position)

        self.magnet = Dummy() if self.use_real_magnet else DummyMagnet()
        # self.position_calculator = Dummy() if self.use_real_position_calculator else DummyPositionCalculator()
        # self.position_output = Dummy() if self.use_real_position_output else DummyPositionOutput()
        self.telescope = Dummy() if self.use_real_telescope else DummyTelescope()
        self.start_socket_server = StartSignalReceiver(executor, start_function) if self.use_real_socket_server \
            else DummyStartSignalReceiver(executor, start_function)
