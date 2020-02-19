"""
Infinite Recharge - Scorpio from FRC 5549: Gryphon Robotics
"""
# import packages
from networktables import NetworkTables
from robotpy_ext.control.toggle import Toggle
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

    # I can't remember how python handles variable initialization or optimizes variables in general but I'm putting vars
    # for periodics here in case it handles variables like C/++ so I can prevent redeclaration and optimize the code.
    gearButtonStatus: bool = None
    driveButtonToggle: Toggle = None  # left joy, button 2 toggle.

    def robotInit(self):
        """ function that is run at the beginning of the match """

        global LeftJoystick, RightJoystick, Joystick

        LeftJoystick = wpilib.Joystick(1)
        RightJoystick = wpilib.Joystick(2)
        Joystick = wpilib.Joystick(3)  # xbox

        # Button for Switching Between Arcade and Tank Drive
        self.driveButtonToggle = Toggle(LeftJoystick, 2)

        # init networktables
        NetworkTables.initialize(server="10.55.49.2")

        # init networktables dependent modules
        Vision.init()
        Dashboard.init()

        # init motor modules
        Drive.init()
        Indexer.init()
        Intake.init()
        Lift.init()
        Shooter.init()

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
        self.gearButtonStatus = Joystick.getRawButton(1)

        # Changing Between Arcade and Tank Drive
        if self.driveButtonToggle.get():
            Drive.tankDrive()
        else:
            Drive.arcadeDrive()

        # Changing Drive Train Gears
        if self.gearButtonStatusPrev and not self.gearButtonStatus:
            Drive.alternateGear()

        # finalize the loop by applying the joystick state of this loop to be carried forward as the previous.
        self.gearButtonStatusPrev = self.gearButtonStatus


if __name__ == '__main__':
    ''' running the entire robot program '''
    wpilib.run(Manticore)
