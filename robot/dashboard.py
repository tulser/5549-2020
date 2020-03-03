""" dashboard functions """
# importing packages
from custom import ActiveBase
from robot import *

__all__ = ["Dashboard"]


class Dashboard(ActiveBase):

    __dashboard = None

    @classmethod
    def __init__(cls):
        if not cls.__active:
            cls.__startup()
            cls.__active = True
        return

    @classmethod
    def __startup(cls):
        cls.__dashboard = SharedTables.dashboard
        return

    @classmethod
    def setDashboardGearStatus(cls, status: int):
        if status is 0:
            message = "OFF"
        elif status is 1:
            message = "HIGH"
        elif status is 2:
            message = "LOW"
        else:
            message = "UNKNOWN"
        cls.__dashboard.putString("Gear Shift", message)
        return

    @classmethod
    def setLiftStatus(cls, status: int):
        if status is 0:
            message = "INACTIVE"
        elif status is 1:
            message = "ACTIVE"
        elif status is 2:
            message = "YOUR CONTROL"
        else:
            message = "UNKNOWN"
        cls.__dashboard.putString("Lift Status", message)
        return

    @classmethod
    def setCompressorStatus(cls, status: int):
        if status is 0:
            message = "OFF"
        elif status is 1:
            message = "INACTIVE"
        elif status is 2:
            message = "ACTIVE"
        else:
            message = "UNKNOWN"
        cls.__dashboard.putString("Compressor Status", message)
        return

    @classmethod
    def setDriveStatus(cls, status: int):
        if status is 0:
            message = "TANK"
        elif status is 1:
            message = "ARCADE"
        else:
            message = "UNKNOWN/UNSUPPORTED"
        cls.__dashboard.putString("Drive Status", message)

    @classmethod
    def setBallsStatus(cls, quantity: int):
        cls.__dashboard.putNumber("Balls Obtained", quantity)

    @classmethod
    def setAHRSstatus(cls, angle: float):
        cls.__dashboard.putNumber("AHRS Yaw", angle)
