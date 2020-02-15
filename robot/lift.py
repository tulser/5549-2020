""""" lift functions """
# importing packages
from ctre import *

__all__ = ["Lift"]

class Lift:

    __liftMotor: WPI_VictorSPX = None

    @classmethod
    def __call__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__liftMotor = WPI_VictorSPX(15)

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
