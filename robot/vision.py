""" vision functions """
# importing packages
from time import sleep
from robot.shared import *
import math
from networktables import NetworkTable

__all__ = ["Vision"]

TARGETHEIGHTSIZE = 0.2159
CAMANGLEMOUNT = 45
CAMHEIGHTMOUNT = 0  # Needs to change
CAMOFFSETMOUNT = 0  # Needs to change


class Vision:

    __limelight: NetworkTable = None

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__limelight = SharedTables.getTable("limelight")

    @classmethod
    def getTargetVisible(cls):  # Recommended to call this before calling getTargetDistance or getTargetAngle
        return True if cls.__limelight.getNumber('tv', -1) == 1 else False

    @classmethod
    def getTargetAngle(cls):
        cls.__limelight.putNumber('ledMode', 3)
        sleep(2)
        horizontalTargetAngle = cls.__limelight.getNumber('tx', 0)
        cls.__limelight.putNumber('ledMode', 1)

        return math.radians(horizontalTargetAngle)*0.99  # 0.99 is a coefficient to prevent overshoot.

    @classmethod
    def getTargetDistance(cls):
        cls.__limelight.putNumber('ledMode', 3)
        sleep(2)
        verticalTargetAngle = cls.__limelight.getNumber('ty', 0)  # finds vertical angle to target
        cls.__limelight.putNumber('ledMode', 1)

        # finds distance to target using limelight
        return (TARGETHEIGHT - CAMHEIGHTMOUNT - TARGETHEIGHTSIZE) / math.tan(math.radians(CAMANGLEMOUNT + verticalTargetAngle)) + CAMOFFSETMOUNT
