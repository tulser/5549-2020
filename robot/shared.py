import wpilib  # only for annotations

# shared constants
TARGETHEIGHTBIAS = 0.01  # offset to compensate for air resistance
TARGETHEIGHT = 2.49555  # ground to target mid
TARGETMARGINS = 0.2921  # maximum vertical margins for ball to go into target.

# shared objects
RightJoystick: wpilib.Joystick = None
LeftJoystick: wpilib.Joystick = None
XBox: wpilib.Joystick = None
