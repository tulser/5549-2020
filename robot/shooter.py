""" shooter functions """
# importing packages
from robot import *
import math
from ctre import *
from custom import *

__all__ = ["Shooter"]

class Shooter:

    __motors: SpeedControllerGroup_M = None

    @classmethod
    def __call__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__motors = SpeedControllerGroup_M(WPI_TalonSRX(4), WPI_TalonSRX(5), WPI_TalonSRX(6), WPI_TalonSRX(7))

    @classmethod
    def shootAuto(cls, force=False):
        dist = Vision.getDistance()
        if (dist < (TARGETHEIGHT-TARGETMARGINS) or dist > (TARGETHEIGHT-TARGETMARGINS)) and not force:
            # Recommended to setup networktables feedback under this conditional.
            return

        # automatically shoot balls given distance
        cls.__motors.set(math.sqrt(-9.81*math.pow(dist, 2)/(TARGETHEIGHT-SHOOTERHEIGHT+TARGETHEIGHTBIAS-dist)), WPI_TalonSRX.ControlMode.Velocity)
        return
