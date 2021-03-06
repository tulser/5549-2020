""" shooter functions """
# importing packages
from robot import *
from math import sqrt, pow
from ctre import *
from wpilib import SpeedControllerGroup
from custom import ActiveBase, PIDManager

__all__ = ["Shooter"]

SHOOTERTOLERANCE = 30

UP_P = 0.25
UP_I = 0.04
UP_D = 0.02
UP_F = 1

DN_P = 0.2
DN_I = 0.04
DN_D = 0.02
DN_F = 1

class Shooter(ActiveBase):
    __active = False

    __encoderTop: WPI_TalonSRX = None
    __encoderBot: WPI_TalonSRX = None
    __motorsUp: SpeedControllerGroup = None
    __motorsDown: SpeedControllerGroup = None
    __pidUp: PIDManager = None
    __pidDown: PIDManager = None

    presets = (
        [1700, 2700],
    )

    @classmethod
    def __init__(cls):
        if not cls.__active:
            cls.__startup()
            cls.__active = True
        return

    @classmethod
    def __startup(cls):
        cls.__encoderTop = WPI_TalonSRX(5)
        cls.__encoderBot = WPI_TalonSRX(7)

        cls.__motorsUp = SpeedControllerGroup(cls.__encoderTop, WPI_VictorSPX(6))
        cls.__motorsDown = SpeedControllerGroup(cls.__encoderBot, WPI_VictorSPX(8))

        cls.__pidUp = PIDManager(cls.__motorsUp, 0, UP_P, UP_I, UP_D, UP_F, cls.__encoderTop, cls.__encoderBot)
        cls.__pidDown = PIDManager(cls.__motorsDown, 0, DN_P, DN_I, DN_D, DN_F, cls.__encoderTop, cls.__encoderBot)

        cls.__pidUp.setTolerance(SHOOTERTOLERANCE)
        cls.__pidDown.setTolerance(SHOOTERTOLERANCE)
        return

    @classmethod
    def shootBoth(cls, rpm: float):
        cls.shootDifferent(rpm, rpm)
        return

    @classmethod
    def shootDesired(cls, rpm: float, whichmotor: int):  # 0: both, 1: up, 2: down
        if whichmotor == 0:
            cls.shootDifferent(rpm, rpm)
        if whichmotor == 1:
            cls.__pidUp.pause()
            cls.__pidUp.setSetpoint(rpm)
            cls.__pidUp.reset()
            cls.__pidUp.go(0.05)
        if whichmotor == 2:
            cls.__pidDown.pause()
            cls.__pidDown.setSetpoint(rpm)
            cls.__pidUp.reset()
            cls.__pidDown.go(0.05)
        return

    @classmethod
    def shootDifferent(cls, rpmUp: float, rpmDown: float):
        cls.__pidUp.pause()
        cls.__pidDown.pause()
        cls.__pidUp.setSetpoint(rpmUp)
        cls.__pidDown.setSetpoint(rpmDown)
        cls.__pidUp.reset()
        cls.__pidDown.reset()
        cls.__pidUp.go(0.05)
        cls.__pidDown.go(0.05)
        return

    @classmethod
    def shootPreset(cls, setting: int):
        cls.shootDifferent(cls.presets[setting][0], cls.presets[setting][1])
        return

    @classmethod
    def shootAuto(cls, force=False):
        if not Vision.getTargetVisible():
            return False
        dist = Vision.getTargetDistance()
        if dist < (TARGETHEIGHT-TARGETMARGINS) and not force:
            # Recommended to setup networktables feedback under this conditional.
            return False

        cls.__encoderTop.setSelectedSensorPosition(0)
        cls.__encoderBot.setSelectedSensorPosition(0)

        # automatically shoot balls given distance
        cls.shootBoth(sqrt(-9.81 * pow(dist, 2) / (TARGETHEIGHT - 0.5461 + TARGETHEIGHTBIAS - dist)) * 12832.661368899589)
        return True

    @classmethod
    @property
    def allready(cls) -> bool:
        return cls.__pidUp.achieved and cls.__pidDown.achieved
