""" vision functions """
# importing packages
import wpilib
from networktables import NetworkTables
import math


class Vision:
    def __init__(self):
        self.heightCamera = 0 # change later
        self.heightTarget = 0 # change later
        self.angleMount = 0 # change later
        self.limelight = NetworkTables.getTable("limelight")

    def getDistance(self):
        self.verticalAngleToTarget = self.limelight.getNumber('ty')  # finds vertical angle to target
        self.horizontalAngleToTarget = self.limelight.getNumber('tx')  # finds horizontal angle to target

        # finds distance to target using limelight
        self.distanceToTarget = (self.heightTarget - self.heightCamera) / math.tan(self.angleMount + self.angleToTarget)