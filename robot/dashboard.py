""" dashboard functions """
# importing packages
from networktables import NetworkTables

__all__ = ["Dashboard"]


class Dashboard:

    __dashboard = None

    @classmethod
    def __init__(cls):
        cls.init()

    @classmethod
    def init(cls):
        cls.__dashboard = NetworkTables.getTable('SmartDashboard')

    @classmethod
    def setDashboardGearStatus(cls, status):
        # display high/low gear to dashboard
        if status is 0:
            message = "Gear OFF"
        elif status is 1:
            message = "HIGH Gear"
        elif status is 2:
            message = "LOW Gear"
        else:
            message = "Unknown Gear"
        cls.__dashboard.putString("Gear Shift", message)
        return
