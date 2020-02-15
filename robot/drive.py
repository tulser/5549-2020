""" drive functions """
# importing packages
import wpilib
from robot.shared import LeftJoystick, RightJoystick
from robot.dashboard import Dashboard
from ctre import *
from wpilib.drive import DifferentialDrive

__all__ = ["Drive"]

DRIVESCALING = 0.65

class Drive:

    # drive train motor groups
    _leftDrive = wpilib.SpeedControllerGroup(WPI_TalonSRX(1), WPI_TalonSRX(2))
    _rightDrive = wpilib.SpeedControllerGroup(WPI_TalonSRX(3), WPI_TalonSRX(4))

    # setting up differential drive
    __fullDrive = DifferentialDrive(_leftDrive, _rightDrive)

    # pneumatic solenoid for gear shifting
    _gearSolenoid = wpilib.DoubleSolenoid(0, 1)

    @classmethod
    def manualTurn(cls, angle):
        # turn robot to specified angle values using navx
        pass

    @classmethod
    def autoTurn(cls):
        # turn robot to angle values returned from Vision.getTargetAngle using navx
        pass

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
    def tankDrive(cls):
        # tank drive at set scaling
        cls.__fullDrive.tankDrive(LeftJoystick.getRawAxis(1) * DRIVESCALING, RightJoystick.getRawAxis(1) * DRIVESCALING)
        return

    @classmethod
    def arcadeDrive(cls):
        # arcade drive at set scaling
        cls.__fullDrive.arcadeDrive(LeftJoystick.getRawAxis(1) * DRIVESCALING, LeftJoystick.getRawAxis(2) * DRIVESCALING)
        return
