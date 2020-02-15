""" dashboard functions """
# importing packages
from robot.drive import Drive
from networktables import NetworkTables, NetworkTable

__all__ = ["Dashboard"]

class Dashboard:

    __dashboard: NetworkTable = NetworkTables.getTable('SmartDashboard')

    @classmethod
    def setDashboardGearStatus(cls):
        # display high/low gear to dashboard
        if Drive._gearSolenoid.get() is 1:
            cls.__dashboard.putString("Gear Shift", "HIGH Gear")
        elif Drive._gearSolenoid.get() is 2:
            cls.__dashboard.putString("Gear Shift", "LOW Gear")
        else:
            cls.__dashboard.putString("Gear Shift", "Gear OFF")
        return
