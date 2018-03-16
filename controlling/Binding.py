from controlling.Dummies.Dummy import Dummy
from controlling.Dummies.DummyBalanceEngine import DummyBalanceEngine
from controlling.Dummies.DummyTargetDetection import DummyTargetDetection
from controlling.Dummies.DummyLoadPositionComparer import DummyLoadPositionComparer
from controlling.Dummies.DummyMagnet import DummyMagnet
from controlling.Dummies.DummyMovement import DummyMovement
from controlling.Dummies.DummyTelescope import DummyTelescope
from controlling.Dummies.sensors.DummyXPosition import DummyXPosition


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

    def __init__(self, goal_found_function):
        # TODO replace Dummy(), it raises an error when initialized
        self.movement = Dummy() if self.use_real_movement else DummyMovement()
        self.x_position = Dummy() if self.use_real_x_position else DummyXPosition(self.movement)
        self.balancer = Dummy() if self.use_real_balancer else DummyBalanceEngine(self.x_position)
        self.target_detection = Dummy() if self.use_real_goal_detection else DummyTargetDetection(goal_found_function)
        self.load_position_comparer = Dummy() if self.use_real_load_position_comparer \
            else DummyLoadPositionComparer(self.x_position)
        self.magnet = self._get_real_magnet() if self.use_real_magnet else DummyMagnet()
        self.telescope = Dummy() if self.use_real_telescope else DummyTelescope()

    def _get_real_magnet(self):
        from magnet.Magnet import Magnet
        return Magnet()
