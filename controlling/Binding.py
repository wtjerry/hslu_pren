from arduinocommunication.communication import Communication
from controlling.Config import Config
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

    def __init__(self, position_sender):
        self._communication = Communication() if Config.BINDING_USE_REAL_MOVEMENT or Config.BINDING_USE_REAL_POSITION else DummyCommunication()
        self.movement_engine = MovementEngine(self._communication) if Config.BINDING_USE_REAL_MOVEMENT else DummyMovementEngine()
        self.goal_detection = self._get_real_goal_detection() if Config.BINDING_USE_REAL_GOAL_DETECTION else DummyGoalDetection()
        self.magnet = self.get_real_magnet() if Config.BINDING_USE_REAL_MAGNET else DummyMagnet()
        self.telescope_engine = TelescopeEngine(self._communication) if Config.BINDING_USE_REAL_TELESCOPE else DummyTelescopeEngine()
        self.position = self._get_real_position(position_sender) if Config.BINDING_USE_REAL_POSITION \
            else DummyPosition(self.movement_engine, self.telescope_engine, position_sender)
        self.tilt_engine = TiltEngine(self._communication) if Config.BINDING_USE_REAL_TILT_ENGINE else DummyTiltEngine()
        self.load_position_comparer = PositionLoadComparer(self.position) if Config.BINDING_USE_REAL_LOAD_POSITION_COMPARER \
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
