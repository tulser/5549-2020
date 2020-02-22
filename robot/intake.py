""" intake functions """
# importing packages
from ctre import *
from wpilib import SpeedControllerGroup
# from custom import SpeedControllerGroup_M

__all__ = ["Intake"]

INTOPSCALAR = 2
INBOTSCALAR = 1.5
SECONDINTAKESCALAR = 1
LEXANSCALAR = 1
SEMICIRCLEOUTPUT = 1.5


class Intake:

    __intakeFlipTop: WPI_TalonSRX = None
    __intakeFlipBot: WPI_TalonSRX = None
    __intakeIntermediate: SpeedControllerGroup = None
    __intakeOverhead: WPI_VictorSPX = None
    __roller: WPI_TalonSRX = None  # semicircle

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__intakeFlipTop = WPI_TalonSRX(11)
        cls.__intakeFlipBot = WPI_TalonSRX(12)
        cls.__intakeIntermediate = SpeedControllerGroup(WPI_TalonSRX(9), WPI_VictorSPX(10))
        cls.__intakeOverhead = WPI_VictorSPX(15)
        cls.__intakeOverhead.setInverted()
        cls.__roller = WPI_TalonSRX(14)
        cls.__roller.setInverted()

    @classmethod
    def getThoseBalls(cls):
        # taking in the ball at set scaling
        cls.__intakeFlipTop.set(INTOPSCALAR)
        cls.__intakeFlipBot.set(INBOTSCALAR)
        cls.__intakeIntermediate.set(SECONDINTAKESCALAR)
        cls.__intakeOverhead.set(LEXANSCALAR)
        return

    @classmethod
    def cycleThoseBalls(cls):
        cls.__intakeOverhead.set(LEXANSCALAR)
        cls.__roller.set(SEMICIRCLEOUTPUT)

    @classmethod
    def eject(cls):
        # ejecting ball at set scaling
        cls.__intakeFlipTop.set(-INTOPSCALAR)
        cls.__intakeFlipBot.set(-INBOTSCALAR)
        cls.__intakeIntermediate.set(-SECONDINTAKESCALAR)
        cls.__intakeOverhead.set(-LEXANSCALAR)
        cls.__roller.set(-SEMICIRCLEOUTPUT)
        return
