import wpilib
#constants
ROBOTRADIUS = 0 # Needs to change, should be the radius from the center of the robot to the wheels/drivetrain.

CAMANGLEMOUNT = 45
CAMHEIGHTMOUNT = 0 # Needs to change
CAMOFFSETMOUNT = 0 # Needs to change

TARGETHEIGHTBIAS = 0.01
TARGETHEIGHT = 0  # Needs to change
TARGETMARGINS = 0.2921

#shared objects
RightJoystick: wpilib.Joystick = None
LeftJoystick: wpilib.Joystick = None
Joystick: wpilib.Joystick = None
