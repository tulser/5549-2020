""" intake functions """
# importing packages
from custom import ActiveBase  # , SpeedControllerGroup_M
from ctre import *
from wpilib import SpeedControllerGroup, DigitalInput

__all__ = ["Intake"]

FLIPSCALAR = 1.5
SECONDINTAKESCALAR = 1
LEXANSCALAR = 1
SEMICIRCLEOUTPUT = 1.5


class Intake(ActiveBase):
    __limitSwitch: DigitalInput = None
    __balls = 0
    __limitSwitchTriggered = False

    __intakeFlip: WPI_TalonSRX = None
    __intakeVertical: SpeedControllerGroup = None
    __intakeOverhead: WPI_VictorSPX = None
    __roller: WPI_TalonSRX = None  # semicircle

    @classmethod
    def __init__(cls):
        if not cls.__active:
            cls.__startup()
            cls.__active = True
        return

    @classmethod
    def __startup(cls):
        cls.__limitSwitch = DigitalInput(0)
        cls.__intakeFlip = WPI_TalonSRX(11)
        cls.__intakeFlip.setInverted(True)
        cls.__intakeVertical = SpeedControllerGroup(WPI_TalonSRX(9), WPI_VictorSPX(10))
        cls.__intakeOverhead = WPI_VictorSPX(15)
        cls.__intakeOverhead.setInverted()
        cls.__roller = WPI_TalonSRX(14)
        cls.__roller.setInverted()
        return

    @classmethod
    def intake(cls):
        cls.__intakeFlip.set(FLIPSCALAR)
        cls.__intakeVertical.set(SECONDINTAKESCALAR)
        cls.__intakeOverhead.set(LEXANSCALAR)
        return

    @classmethod
    def moveThoseBalls(cls, state):
        # taking in the ball at set scaling
        if state is 0:  # stuck
            cls.__intakeFlip.set(0)
            cls.__intakeVertical.set(0)
            cls.__intakeOverhead.set(0)
            cls.__roller.set(0)
        elif state is 1:  # suck
            cls.__intakeFlip.set(FLIPSCALAR)
            cls.__intakeVertical.set(SECONDINTAKESCALAR)
            cls.__intakeOverhead.set(LEXANSCALAR)
        elif state is -1:  # huck
            cls.eject()
        elif state is -2:  # huck more
            cls.eject()
            cls.__roller.set(-SEMICIRCLEOUTPUT)
        return

    @classmethod
    def cycleThoseBalls(cls):
        cls.__intakeOverhead.set(LEXANSCALAR)
        cls.__roller.set(SEMICIRCLEOUTPUT)
        return

    @classmethod
    def eject(cls):
        cls.__intakeFlip.set(-FLIPSCALAR)
        cls.__intakeVertical.set(-SECONDINTAKESCALAR)
        cls.__intakeOverhead.set(-LEXANSCALAR)
        return
