""" intake functions """
# importing packages
from custom import ActiveBase  # , SpeedControllerGroup_M
from robot import SharedJoysticks, Shooter
from ctre import *
from wpilib import SpeedControllerGroup, DigitalInput, I2C
from rev.color import ColorSensorV3

__all__ = ["Intake"]

FIRSTINTAKESCALAR = 0.5
SECONDINTAKESCALAR = 0.75
THIRDINTAKESCALAR = 1
COLORSENSITIVITY = 160


class Intake(ActiveBase):
    __limitSwitch: DigitalInput = None
    __balls = 0
    __limitSwitchTriggered = False

    __intakeFlip: WPI_TalonSRX = None
    __intakeIndexer: SpeedControllerGroup = None
    __intakeOverhead: WPI_VictorSPX = None
    __roller: WPI_TalonSRX = None  # semicircle

    __colorSensor: ColorSensorV3

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

        one = WPI_TalonSRX(9)
        two = WPI_VictorSPX(10)
        bed = WPI_TalonSRX(12)
        one.setInverted(True)
        two.setInverted(True)
        bed.setInverted(True)
        cls.__intakeIndexer = SpeedControllerGroup(one, two, bed)

        cls.__intakeOverhead = WPI_VictorSPX(15)
        cls.__intakeOverhead.setInverted(True)

        cls.__roller = WPI_TalonSRX(14)
        cls.__roller.setInverted(True)

        cls.__colorSensor = ColorSensorV3(I2C.Port.kOnboard)
        return

    @classmethod
    def setPrimaryIntake(cls, speed: float = 0):
        cls.__intakeFlip.set(speed * FIRSTINTAKESCALAR)
        return
    
    @classmethod
    def setSecondaryIntake(cls, speed: float = 0):
        cls.__intakeIndexer.set(speed * SECONDINTAKESCALAR)
        return 
    
    @classmethod
    def setTernaryIntake(cls, speed: float = 0):
        if speed is not 0:
            cls.__intakeOverhead.set(speed * THIRDINTAKESCALAR)
        else:
            cls.__intakeOverhead.stopMotor()
        return

    @classmethod
    def setMultipleIntake(cls, first: float = 0, second: float = 0, third: float = 0):
        cls.setPrimaryIntake(first)
        cls.setSecondaryIntake(second)
        cls.setTernaryIntake(third)

    @classmethod
    def intake(cls):
        if not SharedJoysticks.XBox.getRawButton(7):
            if SharedJoysticks.XBox.getRawAxis(3) < 0.25:
                Shooter.shootPreset(0)
                if Shooter.allready:
                    cls.setMultipleIntake(1, 1, 1)
                cls.__balls = 0
            else:
                dpadValue = SharedJoysticks.XBox.getPOV()
                if dpadValue is 315 or dpadValue is 0 or dpadValue is 45:
                    cls.setMultipleIntake(-1, 0, 0)

                elif dpadValue is 135 or dpadValue is 180 or dpadValue is 225:
                    colorprox = cls.__colorSensor.getProximity()
                    secondaryspeed = 1
                    ternaryspeed = 0
                    if colorprox >= COLORSENSITIVITY:
                        ternaryspeed = 1

                    if cls.__balls > 2:
                        secondaryspeed = 0

                    cls.setMultipleIntake(1, secondaryspeed, ternaryspeed)

                else:
                    cls.setMultipleIntake()

        else:
            cls.setMultipleIntake(-1, -1, -1)


    @classmethod
    def eject(cls):
        cls.setPrimaryIntake(-1)
        cls.setSecondaryIntake(-1)
        return

    @classmethod
    def ejectAll(cls):
        cls.eject()
        cls.__intakeOverhead.set(-1)
