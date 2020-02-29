# FRC Team 5549's 2019-2020 Robot Code 

This is the code for FRC Team 5549's robot 2020 Season: Infinite Recharge

# Deploying Code

1. Move to the folder with the code using `cd [directory name]`
2. Connect to the robot's WiFi
3. Deploy code to the robot using `py -3 robot.py deploy`. Add `--no-version-check` to the end you are deploying during the offseason.

Optional: Feel free to use the deploy scripts found [here](https://github.com/FRC5549Robotics/5549-Scripts).

# Todo
#### Critical
- Vision.CAMHEIGHTMOUNT & Vision.CAMOFFSETMOUNT need values.
  - Need camera height difference, in meters, for HEIGHTMOUNT (Lower than shooter is negative)
- Need to implement controls for drivers. (Drive team supervisors, talk with us.)
- Lift needs to have motor/compressor values set.
- Intake needs to implement UltraSonic once build and electrical finish.
- Preset shooter values need their RPMs checked, are these linear speeds or revolution speeds?

#### Semi-Critical
- Autonomous routes must be implemented.
  - Usage of curved/spline pathing?
  - Inline sequence of routes?
  - Awareness of team/other individuals' autonomous stratagem.