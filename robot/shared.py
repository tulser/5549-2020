import wpilib  # only for annotations
import networktables

# shared constants
TARGETHEIGHTBIAS = 0.01  # offset to compensate for undershoot and partly for air resistance
TARGETHEIGHT = 2.49555  # ground to target mid
TARGETMARGINS = 0.2921  # maximum vertical margins for ball to go into target.


# shared objects
class SharedJoysticks:
    RightJoystick: wpilib.Joystick = None
    LeftJoystick: wpilib.Joystick = None
    XBox: wpilib.Joystick = None

class SharedTable:
    NTinstance = networktables.NetworkTablesInstance.getDefault()