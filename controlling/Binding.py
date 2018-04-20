from arduinocommunication.communication import Communication
from controlling.Dummies.Dummy import Dummy
from controlling.Dummies.DummyCommunication import DummyCommunication
from controlling.Dummies.DummyTiltEngine import DummyTiltEngine
from controlling.PositionLoadComparer import PositionLoadComparer
from controlling.TiltController import TiltController
from engines.TelescopeEngine import TelescopeEngine
from engines.TiltEngine import TiltEngine
from controlling.Dummies.DummyPosition import DummyPosition
from controlling.Dummies.DummyGoalDetection import DummyGoalDetection
from controlling.Dummies.DummyLoadPositionComparer import DummyLoadPositionComparer
from controlling.Dummies.DummyMagnet import DummyMagnet
from controlling.Dummies.DummyMovementEngine import DummyMovementEngine
from controlling.Dummies.DummyTelescopeEngine import DummyTelescopeEngine
from engines.MovementEngine import MovementEngine



class Binding(object):
    use_real_movement = False
    use_real_goal_detection = False
    use_real_magnet = False
    use_real_telescope = False
    use_real_position = False
    use_real_balancer = False
    use_real_load_position_comparer = False
    use_real_tilt_engine = False

    def __init__(self, position_sender):
        # TODO replace Dummy(), it raises an error when initialized

        self._communication = Communication() if self.use_real_movement or self.use_real_position else DummyCommunication()
        self.movement_engine = MovementEngine(self._communication) if self.use_real_movement else DummyMovementEngine()
        self.goal_detection = self._get_real_goal_detection() if self.use_real_goal_detection else DummyGoalDetection()
        self.magnet = self.get_real_magnet() if self.use_real_magnet else DummyMagnet()
        self.telescope_engine = TelescopeEngine(self._communication) if self.use_real_telescope else DummyTelescopeEngine()
        self.position = self._get_real_position(position_sender) if self.use_real_position \
            else DummyPosition(self.movement_engine, self.telescope_engine, position_sender)
        self.tilt_engine = TiltEngine(self._communication) if self.use_real_tilt_engine else DummyTiltEngine()
        self.load_position_comparer = PositionLoadComparer() if self.use_real_load_position_comparer \
            else DummyLoadPositionComparer(self.position)

        self.tilt_controller = TiltController(self.position, self.tilt_engine)

    def _get_real_position(self, position_sender):
        from position.XPositionSensor import XPositionSensor
        from position.Position import Position
        return Position(XPositionSensor(), self.movement_engine, self.telescope_engine, position_sender)

    def _get_real_goal_detection(self):
        from goaldetection.GoalDetection import GoalDetection
        return GoalDetection()

    @staticmethod
    def get_real_magnet():
        from magnet.Magnet import Magnet
        return Magnet()
