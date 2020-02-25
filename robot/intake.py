""" intake functions """
# importing packages
from ctre import *
from wpilib import SpeedControllerGroup
# from custom import SpeedControllerGroup_M

__all__ = ["Intake"]

FLIPSCALAR = 1.5
SECONDINTAKESCALAR = 1
LEXANSCALAR = 1
SEMICIRCLEOUTPUT = 1.5


class Intake:

    __intakeFlip: WPI_TalonSRX = None
    __intakeVertical: SpeedControllerGroup = None
    __intakeOverhead: WPI_VictorSPX = None
    __roller: WPI_TalonSRX = None  # semicircle

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__intakeFlip = WPI_TalonSRX(11)
        cls.__intakeVertical = SpeedControllerGroup(WPI_TalonSRX(9), WPI_VictorSPX(10))
        cls.__intakeOverhead = WPI_VictorSPX(15)
        cls.__intakeOverhead.setInverted()
        cls.__roller = WPI_TalonSRX(14)
        cls.__roller.setInverted()

    @classmethod
    def intake(cls):
        cls.__intakeFlip.set(FLIPSCALAR)
        cls.__intakeVertical.set(SECONDINTAKESCALAR)
        cls.__intakeOverhead.set(LEXANSCALAR)

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
        elif state is -1:  # puke
            cls.eject()
        elif state is -2:  # puke more
            cls.eject()
            cls.__roller.set(-SEMICIRCLEOUTPUT)
        return

    @classmethod
    def cycleThoseBalls(cls):
        cls.__intakeOverhead.set(LEXANSCALAR)
        cls.__roller.set(SEMICIRCLEOUTPUT)

    @classmethod
    def eject(cls):
        cls.__intakeFlip.set(-FLIPSCALAR)
        cls.__intakeVertical.set(-SECONDINTAKESCALAR)
        cls.__intakeOverhead.set(-LEXANSCALAR)
