""" vision functions """
# importing packages
from robot.shared import *
from networktables import NetworkTables
import math

__all__ = ["Vision"]

TARGETHEIGHTSIZE = 0.2159
CAMANGLEMOUNT = 45
CAMHEIGHTMOUNT = 0  # Needs to change
CAMOFFSETMOUNT = 0  # Needs to change


class Vision:

    __limelight = None

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__limelight = NetworkTables.getTable("limelight")

    @classmethod
    def getTargetAngle(cls):
        cls.__limelight.putNumber('ledMode', 3)
        horizontalTargetAngle = cls.__limelight.getNumber('tx', -1)
        cls.__limelight.putNumber('ledMode', 1)
        if horizontalTargetAngle == -1: return -1

        return math.radians(horizontalTargetAngle)*0.99  # 0.99 is a coefficient to prevent overshoot.

    @classmethod
    def getTargetDistance(cls):
        cls.__limelight.putNumber('ledMode', 3)
        verticalTargetAngle = cls.__limelight.getNumber('ty', -1)  # finds vertical angle to target
        cls.__limelight.putNumber('ledMode', 1)
        if verticalTargetAngle == -1: return -1

        # finds distance to target using limelight
        return (TARGETHEIGHT - CAMHEIGHTMOUNT - TARGETHEIGHTSIZE) / math.tan(math.radians(CAMANGLEMOUNT + verticalTargetAngle)) + CAMOFFSETMOUNT
