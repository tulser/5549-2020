from custom import ActiveBase
import wpilib  # only for annotations
from networktables import NetworkTablesInstance

# shared constants
TARGETHEIGHTBIAS = 0.01  # offset to compensate for undershoot and partly for air resistance
TARGETHEIGHT = 2.49555  # ground to target mid
TARGETMARGINS = 0.2921  # maximum vertical margins for ball to go into target.


# shared objects
class SharedJoysticks(ActiveBase):
    RightJoystick: wpilib.Joystick = None
    LeftJoystick: wpilib.Joystick = None
    XBox: wpilib.Joystick = None

    @classmethod
    def __init__(cls):
        if not cls.__active:
            cls.__startup()
            cls.__active = True
        return

    @classmethod
    def __startup(cls):
        cls.RightJoystick = wpilib.Joystick(0)
        cls.LeftJoystick = wpilib.Joystick(1)
        cls.XBox = wpilib.Joystick(2)
        return


class SharedTables(ActiveBase):
    __instance: NetworkTablesInstance = None

    @classmethod
    def __init__(cls, server: str):
        if not cls.__active:
            cls.__startup(server)
            cls.__active = True
        return

    @classmethod
    def __startup(cls, server: str):
        cls.__instance = NetworkTablesInstance.getDefault()
        cls.__instance.initialize(server)
        return

    @classmethod
    def getTable(cls, table: str):
        return cls.__instance.getTable(table)


class SharedPneumatics(ActiveBase):
    compressor: wpilib.Compressor = None
    __solenoids: list = None

    @classmethod
    def __init__(cls, doublesolenoids: [wpilib.DoubleSolenoid] = None):
        if not cls.__active:
            cls.__startup(doublesolenoids)
            cls.__active = True
        return

    @classmethod
    def __startup(cls, doublesolenoids: [wpilib.DoubleSolenoid] = None):
        cls.compressor = wpilib.Compressor(0)
        cls.compressor.setClosedLoopControl(True)
        if doublesolenoids is not None:
            cls.__solenoids = doublesolenoids
        cls.compressor.start()
        return

    @classmethod
    def registerNewDoubleSolenoid(cls, forwardChan: int, backwardChan: int) -> int:
        cls.__solenoids.append(wpilib.DoubleSolenoid(forwardChan, backwardChan))
        return len(cls.__solenoids) - 1

    @classmethod
    def setSolenoid(cls, index: int, state: wpilib.DoubleSolenoid.Value):
        cls.__solenoids[index].set(state)
        return
