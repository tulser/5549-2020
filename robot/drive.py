""" drive functions """
# importing packages
from custom import ActiveBase
from wpilib import SpeedControllerGroup, DoubleSolenoid
import navx
from math import fabs
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
        cls.drive = cls.__tankDrive

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
        reqangle = angle
        while fabs(reqangle) >= 2:  # just proportional smoothing
            nspeed = reqangle / 90
            cls._leftDrive.set(nspeed)  # the sign on these might be backwards, needs testing.
            cls._rightDrive.set(-nspeed)
            reqangle = Vision.getTargetAngle()
        return

    @classmethod
    def autoSmoothTurn(cls):  # Align w/ navx
        if not Vision.getTargetVisible():
            return
        cls.__navx.reset()
        angle = Vision.getTargetAngle()
        diff = angle
        while diff >= 2:  # just proportional smoothing
            diff = angle-cls.__navx.getAngle()
            nspeed = diff / 90
            cls._leftDrive.set(nspeed)  # the sign on these might be backwards, needs testing.
            cls._rightDrive.set(-nspeed)
        return

    @classmethod
    def getGearStatus(cls):
        return cls._gearSolenoid.get()

    @classmethod
    def alternateGear(cls):
        gearval = cls._gearSolenoid.get() % 2 + 1
        cls._gearSolenoid.set(gearval)
        Dashboard.setDashboardGearStatus(gearval)
        return

    @classmethod
    def changeGear(cls, gear: DoubleSolenoid.Value):
        # switches gear mode
        if gear > 2 or gear < 0 or gear is cls._gearSolenoid.get():
            return
        cls._gearSolenoid.set(gear)
        Dashboard.setDashboardGearStatus(gear)
        return

    @classmethod
    def stopGear(cls):
        cls._gearSolenoid.set(0)
        return

    @classmethod
    def alternateDrive(cls):
        cls.changeDrive(cls.__driveMode ^ 0x1)
        return

    @classmethod
    def changeDrive(cls, mode: int):
        if cls.__driveMode is mode:
            return
        if mode == 0:
            cls.drive = cls.__tankDrive
        elif mode == 1:
            cls.drive = cls.__arcadeDrive
        cls.__driveMode = mode
        return

    @classmethod
    def drive(cls):
        pass

    @classmethod
    def forceTankDrive(cls, left: float, right: float):
        cls.__fullDrive.tankDrive(left, right)
        return

    @classmethod
    def __tankDrive(cls):
        # tank drive at set scaling
        cls.__fullDrive.tankDrive(SharedJoysticks.LeftJoystick.getRawAxis(1) * DRIVESCALING,
                                  SharedJoysticks.RightJoystick.getRawAxis(1) * DRIVESCALING)
        return

    @classmethod
    def __arcadeDrive(cls):
        # arcade drive at set scaling
        cls.__fullDrive.arcadeDrive(SharedJoysticks.LeftJoystick.getRawAxis(1) * DRIVESCALING,
                                    SharedJoysticks.LeftJoystick.getRawAxis(2) * ROTSCALING)
        return

    @classmethod
    def getAHRSYaw(cls):
        return cls.__navx.getYaw()
