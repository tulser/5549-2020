""""" lift functions """
# importing packages
import wpilib
from ctre import *

__all__ = ["Lift"]

class Lift:

    __liftMotor = WPI_VictorSPX(15)

    @classmethod
    def dropDown(cls):
        # drops the lift to down position
        pass

    @classmethod
    def liftUp(cls):
        # moves the lift to up position
        pass

    @classmethod
    def runMotor(cls, power, *args):
        # runs motor at set power
        cls.__liftMotor.set(power, *args)
        return
