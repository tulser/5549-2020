""" drive functions """
# importing packages
from custom import ActiveBase
from wpilib import SpeedControllerGroup, DoubleSolenoid
import navx
from math import fabs, ceil, log2
from sys import maxsize
from robot import *
from ctre import *
from wpilib.drive import DifferentialDrive

__all__ = ["Drive"]

DRIVEWHEELCIRCUM = 0  # need a measurement
DRIVEROTOUTPUT = 0.5
ROBOTDRIVERADIUS = 0.4  # meters, need a measurement
DRIVESCALING = 0.65
ROTSCALING = 1


class Drive(ActiveBase):

    _motorLeftEnc: WPI_TalonSRX = None
    _motorRightEnc: WPI_TalonSRX = None

    _leftDrive: SpeedControllerGroup = None
    _rightDrive: SpeedControllerGroup = None

    __fullDrive: DifferentialDrive = None

    __driveFunc = None
    __driveMode: int = 0

    __navx: navx.AHRS = None
    _gearSolenoid: DoubleSolenoid = None

    @classmethod
    def __init__(cls):
        if not cls.__active:
            cls.__startup()
            cls.__active = True
        return

    @classmethod
    def __startup(cls):
        # encoders
        cls.motorLeftEnc = WPI_TalonSRX(1)
        cls.motorRightEnc = WPI_TalonSRX(3)

        # drive train motor groups
        cls._leftDrive = SpeedControllerGroup(cls._motorLeftEnc, WPI_VictorSPX(2))
        cls._rightDrive = SpeedControllerGroup(cls._motorRightEnc, WPI_VictorSPX(4))

        # setting up differential drive
        cls.__fullDrive = DifferentialDrive(cls._leftDrive, cls._rightDrive)

        cls.__driveFunc = cls.tankDrive
        cls.__driveMode = 0

        cls.__navx = navx.AHRS.create_spi()

        # pneumatic solenoid for gear shifting
        cls._gearSolenoid = DoubleSolenoid(0, 1)
        return

    @classmethod
    def inputTurn(cls, angle):
        raise NotImplementedError
        pass

    @classmethod
    def autoTurn(cls):
        raise NotImplementedError
        pass

    @classmethod
    def auxAutoSmoothTurn(cls):  # Align to target w/o navx, don't recommend using
        angle = Vision.getTargetAngle()
        intlength = int(log2(maxsize * 2 + 1))
        sign = ceil(angle) >> (intlength-1)
        reqangle = fabs(angle)
        while reqangle >= 0.1:  # just proportional smoothing
            nspeed = sign * (reqangle + 0.05) / 1.570796
            cls._leftDrive.set(nspeed)  # the sign on these might be backwards, needs testing.
            cls._rightDrive.set(-nspeed)
            reqangle = fabs(Vision.getTargetAngle())
            sign = ceil(reqangle) >> (intlength - 1)
        return

    @classmethod
    def autoSmoothTurn(cls):  # Align w/ navx
        cls.__navx.reset()
        angle = Vision.getTargetAngle()
        diff = 4
        while diff >= 0.1:  # just proportional smoothing
            diff = angle-cls.__navx.getAngle()
            nspeed = diff / 1.570796
            cls._leftDrive.set(nspeed)  # the sign on these might be backwards, needs testing.
            cls._rightDrive.set(-nspeed)
        return

    @classmethod
    def alternateGear(cls):
        gearval = cls._gearSolenoid.get() % 2 + 1
        cls._gearSolenoid.set(gearval)
        Dashboard.setDashboardGearStatus(gearval)
        return

    @classmethod
    def changeGear(cls, gear: DoubleSolenoid.Value = 0):
        # switches gear mode
        mode = gear % 3
        cls._gearSolenoid.set(mode)
        Dashboard.setDashboardGearStatus(mode)
        return

    @classmethod
    def stopGear(cls):
        cls._gearSolenoid.set(0)
        return

    @classmethod
    def changeDrive(cls, mode: int):
        if mode == cls.__driveMode: return
        if mode == 0:
            cls.__driveFunc = cls.tankDrive
        if mode == 1:
            cls.__driveFunc = cls.arcadeDrive
        return

    @classmethod
    def drive(cls):
        cls.__driveFunc()

    @classmethod
    def forceTankDrive(cls, left: float, right: float):
        cls.__fullDrive.tankDrive(left, right)
        return

    @classmethod
    def tankDrive(cls):
        # tank drive at set scaling
        cls.__fullDrive.tankDrive(SharedJoysticks.LeftJoystick.getRawAxis(1) * DRIVESCALING,
                                  SharedJoysticks.RightJoystick.getRawAxis(1) * DRIVESCALING)
        return

    @classmethod
    def arcadeDrive(cls):
        # arcade drive at set scaling
        cls.__fullDrive.arcadeDrive(SharedJoysticks.LeftJoystick.getRawAxis(1) * DRIVESCALING,
                                    SharedJoysticks.LeftJoystick.getRawAxis(2) * ROTSCALING)
        return

    @classmethod
    def getAHRSYaw(cls):
        return cls.__navx.getYaw()
