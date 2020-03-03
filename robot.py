"""
Infinite Recharge - Scorpio from FRC 5549: Gryphon Robotics
"""
# import packages
from robotpy_ext.control.toggle import Toggle
import wpilib
from robot import *

"""
Logitech Joysticks

Xbox 360 Controller

Axis Mapping

Button Mapping

Motor Mapping
1: driveLeftMotor1
2: driveLeftMotor2
3: driveRightMotor1
4: driveRightMotor2
5: shooterTopEncoder1
6: shooterTopMotor2
7: shooterBottomEncoder1
8: shooterBottomMotor2
9: intakeMotor1
10: indexerMotor1
11: indexerMotor2
12: indexerMotor3
13: indexerMotor4
14: indexerMotor4
15: liftMotor1
"""


class Manticore(wpilib.TimedRobot):
    gearButtonStatusPrev: bool = False  # variable for storing previous joystick states.
    driveButtonToggle: Toggle = None  # left joy, button 2 toggle.
    liftButtonToggle: Toggle = None

    def robotInit(self):
        """ function that is run at the beginning of the match """

        # init joysticks
        SharedJoysticks()

        # toggle buttons
        self.driveButtonToggle = Toggle(SharedJoysticks.LeftJoystick, 2)
        self.liftButtonToggle = Toggle(SharedJoysticks.XBox, 8)

        # init networktables
        SharedTables(server="10.55.49.2")

        # init networktables dependent modules
        Vision()
        Dashboard()

        # init pure motor modules
        Intake()
        Shooter()

        # init pneumatics
        SharedPneumatics()

        # init motor/pneumatics modules
        Drive()
        Lift()

    def autonomousInit(self):
        ''' function that is run at the beginning of the autonomous phase '''
        pass

    def autonomousPeriodic(self):
        ''' function that is run periodically during the autonomous phase '''
        pass

    def teleopInit(self):
        ''' function that is run at the beginning of the tele-operated phase '''
        pass

    def teleopPeriodic(self):
        ''' function that is run periodically during the tele-operated phase '''

        # get values at start of the loop
        gearButtonStatus = SharedJoysticks.RightJoystick.getRawButton(1)

        # Changing Between Arcade and Tank Drive
        if self.driveButtonToggle.get():
            Drive.changeDrive(0)
        else:
            Drive.changeDrive(1)
        Drive.drive()

        # Changing Drive Train Gears
        if self.gearButtonStatusPrev and not gearButtonStatus:
            Drive.alternateGear()

        if self.liftButtonToggle.get():
            Lift.liftUp()
        else:
            Lift.dropDown()

        # finalize the loop by applying the joystick state of this loop to be carried forward as the previous.
        self.gearButtonStatusPrev = gearButtonStatus


if __name__ == '__main__':
    ''' running the entire robot program '''
    wpilib.run(Manticore)
