""""" lift functions """
# importing packages
from ctre import *
from wpilib import Compressor, DoubleSolenoid

__all__ = ["Lift"]


class Lift:

    __liftMotor: WPI_VictorSPX = None
    __compressor: Compressor = None
    __solenoid: DoubleSolenoid = None

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__liftMotor = WPI_VictorSPX(13)
        cls.__compressor = Compressor(0)
        cls.__solenoid = DoubleSolenoid(2, 3)

    @classmethod
    def dropDown(cls):
        # drops the lift to down position
        pass

    @classmethod
    def liftUp(cls):
        # moves the lift to up position
        pass

    @classmethod
    def manualRun(cls, power, *args):
        # runs motor at set power
        cls.__liftMotor.set(power, *args)
        return
