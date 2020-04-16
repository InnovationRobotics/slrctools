# joy2rc -
The goal of this software package is to stupidely convert /joy topic to /mavros/rc/override topic.

It starts a ROS node called /joy2rc that monitors the following topic:
* /joy (http://docs.ros.org/api/sensor_msgs/html/msg/Joy.html)

It outputs:
* /mavros/rc/override (mavros/OverrideRCIn)







