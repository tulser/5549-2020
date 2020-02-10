""" shooter functions """
# importing packages
import wpilib
from robot.shared import *
import math
from ctre import *

class Shooter:
    def __init__(self):
        # shooter motors and encoders
        self.topShooter1Encoder = WPI_TalonSRX(4)
        self.topShooter2 = WPI_TalonSRX(5)
        self.bottomShooter1Encoder = WPI_TalonSRX(6)
        self.bottomShooter2 = WPI_TalonSRX(7)

        # shooter motor groups
        self.topMotors = wpilib.SpeedControllerGroup(self.topShooter1Encoder, self.topShooter2)
        self.bottomMotors = wpilib.SpeedControllerGroup(self.bottomShooter1Encoder, self.bottomShooter2)

        # setting shooter rpm
        # need to move to always check
        self.topShooterRPM = self.topShooter1Encoder.getSelectedSensorPosition()    # this is not actually rpm
        self.bottomShooterRPM = self.bottomShooter1Encoder.getSelectedSensorPosition()  # this is not actually rpm

    def shootAuto(self, dist, force=False):
        if (dist < (TARGETHEIGHT-TARGETMARGINS) or dist > (TARGETHEIGHT-TARGETMARGINS)) and not force:
            # Recommended to setup networktables feedback
            return

        # automatically shoot balls given distance
        return math.sqrt(-9.81*math.pow(dist, 2)/(TARGETHEIGHT-dist))

    def initializeShooter(self, rpm):
        # initializes shooter and moves piston
        # only for shooter functions
        self.topMotors.set(rpm)
        self.bottomMotors.set(rpm)