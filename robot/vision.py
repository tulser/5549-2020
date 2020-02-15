""" vision functions """
# importing packages
from robot.shared import *
from networktables import NetworkTables, NetworkTable
import math

__all__ = ["Vision"]

class Vision:

    __limelight: NetworkTable = None

    @classmethod
    def __call__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__limelight = NetworkTables.getTable("limelight")

    @classmethod
    def getTargetAngle(cls) -> float:
        horizontalTargetAngle = cls.__limelight.getNumber('tx', -1)

        return math.radians(horizontalTargetAngle)*0.95 #0.95 is a coefficient to prevent overshoot.

    @classmethod
    def getDistance(cls) -> float:
        verticalTargetAngle = cls.__limelight.getNumber('ty', -1)  # finds vertical angle to target
        if verticalTargetAngle is -1: return -1

        # finds distance to target using limelight
        return (TARGETHEIGHT - (CAMHEIGHTMOUNT)) / math.tan(math.radians(CAMANGLEMOUNT + verticalTargetAngle)) + CAMOFFSETMOUNT