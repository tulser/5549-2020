""""" lift functions """
# importing packages
from custom import ActiveBase
from robot import SharedPneumatics
from ctre import *

__all__ = ["Lift"]


class Lift(ActiveBase):
    __liftMotor: WPI_VictorSPX = None
    __pneumaticsLiftSolenoid: int = None

    @classmethod
    def __init__(cls):
        if not cls.__active:
            cls.__startup()
            cls.__active = True
        return

    @classmethod
    def __startup(cls):
        cls.__liftMotor = WPI_VictorSPX(13)
        if SharedPneumatics.getActive():
            cls.__pneumaticsLiftSolenoid = SharedPneumatics.registerNewDoubleSolenoid(2, 3)
        return

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
