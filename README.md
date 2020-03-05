# oprecorder - Operator Recorder
The goal of this software package is to record the world state and the actions performed by an operator.

It starts a ROS node called /oprecorder that monitors the following topics:
* /mavros/local_position/pose (PoseStamped)
* /mavros/local_position/velocity (TwistStamped)
* /arm/height (Int32)
* /arm/blade/Imu (Imu)
* /mavros/imu/data (Imu)
* /stone/1/Pose (PoseStamped)
* /stone/2/Pose (PoseStamped)
* /joy (Joy)

Each time the callback of the action (joystick) is called, it changes the world state accordingly and saves the:
Date&Time, world_state, grade (N/A) by adding a row in the csv file: oprecorder.csv



