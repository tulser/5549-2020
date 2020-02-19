""" drive functions """
# importing packages
import wpilib
from math import fabs, ceil, log2
from sys import maxsize
from robot.shared import LeftJoystick, RightJoystick
from robot.dashboard import Dashboard
from robot.vision import Vision
from ctre import *
from wpilib.drive import DifferentialDrive

__all__ = ["Drive"]

DRIVEWHEELCIRCUM = 0  # need a measurement
DRIVEROTOUTPUT = 0.5
ROBOTDRIVERADIUS = 0.4  # meters, need a measurement
DRIVESCALING = 0.65


class Drive:

    _motorLeftEnc: WPI_TalonSRX = None
    _motorRightEnc: WPI_TalonSRX = None

    _leftDrive: wpilib.SpeedControllerGroup = None
    _rightDrive: wpilib.SpeedControllerGroup = None

    __fullDrive: DifferentialDrive = None

    _gearSolenoid: wpilib.DoubleSolenoid = None

    @classmethod
    def __call__(cls):
        cls.init()

    @classmethod
    def init(cls):
        # encoders
        cls.motorLeftEnc = WPI_TalonSRX(13)
        cls.motorRightEnc = WPI_TalonSRX(15)

        # drive train motor groups
        cls._leftDrive = wpilib.SpeedControllerGroup(cls._motorLeftEnc, WPI_VictorSPX(14))
        cls._rightDrive = wpilib.SpeedControllerGroup(cls._motorRightEnc, WPI_VictorSPX(16))

        # setting up differential drive
        cls.__fullDrive = DifferentialDrive(cls._leftDrive, cls._rightDrive)

        # pneumatic solenoid for gear shifting
        cls._gearSolenoid = wpilib.DoubleSolenoid(0, 1)

    @classmethod
    def inputTurn(cls, angle):
        raise NotImplementedError
        pass

    @classmethod
    def autoTurn(cls):
        raise NotImplementedError
        pass

    @classmethod
    def autoSmoothTurn(cls):
        angle = Vision.getTargetAngle()
        intlength = log2(maxsize * 2 + 1)
        sign = ceil(angle) >> (intlength-1)
        reqangle = fabs(angle)
        angle = None
        while reqangle >= 0.1:  # just proportional smoothing
            nspeed = sign * (reqangle + 0.05) / 1.570796
            cls._leftDrive.set(nspeed)  # the sign on these might be backwards, needs testing.
            cls._rightDrive.set(-nspeed)
            reqangle = fabs(Vision.getTargetAngle())
            sign = ceil(reqangle) >> (intlength - 1)
        return

    @classmethod
    def alternateGear(cls):
        cls._gearSolenoid.set(cls._gearSolenoid.get() % 2 + 1)
        Dashboard.setDashboardGearStatus()
        return

    @classmethod
    def changeGear(cls, toggle: wpilib.DoubleSolenoid.Value=0):
        # switches gear mode
        cls._gearSolenoid.set(toggle % 3)
        Dashboard.setDashboardGearStatus()
        return

    @classmethod
    def stopGear(cls):
        cls._gearSolenoid.set(0)
        return

    @classmethod
    def tankDrive(cls):
        # tank drive at set scaling
        cls.__fullDrive.tankDrive(LeftJoystick.getRawAxis(1) * DRIVESCALING, RightJoystick.getRawAxis(1) * DRIVESCALING)
        return

    @classmethod
    def arcadeDrive(cls):
        # arcade drive at set scaling
        cls.__fullDrive.arcadeDrive(LeftJoystick.getRawAxis(1) * DRIVESCALING, LeftJoystick.getRawAxis(2) * DRIVESCALING)
        return
