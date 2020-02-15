import wpilib  # only for annotations

# shared constants
CAMANGLEMOUNT = 45
CAMHEIGHTMOUNT = 0  # Needs to change
CAMOFFSETMOUNT = 0  # Needs to change

SHOOTERHEIGHT = 0.5461  # ground to shooter

TARGETHEIGHTBIAS = 0.01  # offset to compensate for air resistance
TARGETHEIGHT = 2.49555  # ground to target mid
TARGETMARGINS = 0.2921  # maximum vertical margins for ball to go into target.


# shared objects
RightJoystick: wpilib.Joystick = None
LeftJoystick: wpilib.Joystick = None
Joystick: wpilib.Joystick = None
