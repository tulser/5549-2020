""" dashboard functions """
# importing packages
from robot import *

__all__ = ["Dashboard"]


class Dashboard:

    __dashboard = None

    @classmethod
    def __init__(cls):
        cls.init()
        return

    @classmethod
    def init(cls):
        cls.__dashboard = SharedTable.NTinstance.getTable('SmartDashboard')
        return

    @classmethod
    def setDashboardGearStatus(cls, status):
        # display high/low gear to dashboard
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
    def setLiftStatus(cls, status):
        # display high/low gear to dashboard
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
    def setCompressorStatus(cls, status):
        # display high/low gear to dashboard
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
