from arduinocommunication.communication import Communication
from controlling.Dummies.Dummy import Dummy
from controlling.Dummies.DummyTiltEngine import DummyTiltEngine
from controlling.Dummies.DummyPosition import DummyPosition
from controlling.Dummies.DummyGoalDetection import DummyGoalDetection
from controlling.Dummies.DummyLoadPositionComparer import DummyLoadPositionComparer
from controlling.Dummies.DummyMagnet import DummyMagnet
from controlling.Dummies.DummyMovementEngine import DummyMovementEngine
from controlling.Dummies.DummyTelescopeEngine import DummyTelescopeEngine
from controlling.TiltController import TiltController
from engines.MovementEngine import MovementEngine
from engines.TelescopeEngine import TelescopeEngine
from engines.TiltEngine import TiltEngine


class Binding:
    _use_real_tilt_engine = False
    _use_real_goal_detection = False
    _use_real_load_position_comparer = False
    _use_real_magnet = False
    _use_real_movement = False
    _use_real_position_calculator = False
    _use_real_position_output = False
    _use_real_telescope = False
    _use_real_x_position = False
    _use_real_start_signal = False
    _use_real_position = False
    _use_real_communication = False

    def __init__(self, position_sender):
        # TODO replace Dummy(), it raises an error when initialized
        self._communication = Communication() if self._use_real_communication else object()
        self.movement_engine = MovementEngine(self._communication) if self._use_real_movement else DummyMovementEngine()
        self.goal_detection = Dummy() if self._use_real_goal_detection else DummyGoalDetection()
        self.magnet = self.get_real_magnet() if self._use_real_magnet else DummyMagnet()
        self.telescope_engine = TelescopeEngine(self._communication) if self._use_real_telescope else DummyTelescopeEngine()
        self.position = self._get_real_position(position_sender) if self._use_real_position \
            else DummyPosition(self.movement_engine, self.telescope_engine, position_sender)
        self.tilt_engine = TiltEngine(self._communication) if self._use_real_tilt_engine else DummyTiltEngine()
        self.load_position_comparer = Dummy() if self._use_real_load_position_comparer \
            else DummyLoadPositionComparer(self.position)

        self.tilt_controller = TiltController(self.position, self.tilt_engine)

    def _get_real_position(self, position_sender):

        from position.Position import Position
        return Position(self.movement_engine, self.telescope_engine, position_sender)


    def get_real_magnet(self):
        from magnet.Magnet import Magnet
        return Magnet()
