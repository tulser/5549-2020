""" vision functions """
# importing packages
from robot.shared import *
from networktables import NetworkTables
import math

__all__ = ["Vision"]


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
        horizontalTargetAngle = cls.__limelight.getNumber('tx', -1)
        if horizontalTargetAngle is -1: return -1

        return math.radians(horizontalTargetAngle)*0.99  # 0.99 is a coefficient to prevent overshoot.

    @classmethod
    def getDistance(cls):
        verticalTargetAngle = cls.__limelight.getNumber('ty', -1)  # finds vertical angle to target
        if verticalTargetAngle is -1: return -1

        # finds distance to target using limelight
        return (TARGETHEIGHT - CAMHEIGHTMOUNT) / math.tan(math.radians(CAMANGLEMOUNT + verticalTargetAngle)) + CAMOFFSETMOUNT
