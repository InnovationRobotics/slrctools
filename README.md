# slrctools
The goal of this software package is to stupidely convert /joy topic to /mavros/rc/override topic.

The file joy2rc.py is the implementation of the ROS node called /joy2rc that corresponds to microsoft mouse.
The file ltech2rc.py is the implementation of the ROS node called /ltech2rc that corresponds to logitech mouse.
This two nodes monitor the following topic:
* /joy (http://docs.ros.org/api/sensor_msgs/html/msg/Joy.html)

and output the topic that corresponds to the mavros rc topic:
* /mavros/rc/override (mavros/OverrideRCIn)

The file adc2std.py contains the implementation of the node adc2std that converts the arduino topic:
 * /adc
 
to: 
 * /arm/height, /arm/shortHeight, /arm/blade/Imu

This node is needed only for the real car. For this last file, you need to install rosserial_arduino.







