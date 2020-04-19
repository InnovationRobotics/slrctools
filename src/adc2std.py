#!/usr/bin/env python

import sys
sys.path
import rospy
from std_msgs.msg import Header
from std_msgs.msg import Int32, Bool
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs import msg
from datetime import datetime
import math
from geometry_msgs.msg import Pose, Point, Quaternion, Vector3
import Unity2RealWorld27 as toRW
from rosserial_arduino.msg import Adc
#from slrctools.msg import IntAdc
from rospy_tutorials.msg import Floats

class Adc2Std(object):
    bladeImuMsg = Imu()
    msgHeightShort = Int32()
    msgHeightLong = Int32()
#    thismsg = IntAdc()

    def AdcSubCB(self, msg):
        rospy.logdebug("Got message:"+msg)
        self.msgHeightShort = msg.adc0
        self.pubShortHeight.publish(self.msgHeightShort)
        self.msgHeightLong = msg.adc1
        self.pubLongHeight.publish(self.msgHeightLong)

        rollPitchYaw = Vector3(msg.adc2, msg.adc3, msg.adc4)
        self.bladeImuMsg.orientation = toRW.rotationROS2RW(rollPitchYaw)
        self.pubBladeImu.publish(self.bladeImuMsg)


    def __init__(self):
        rospy.init_node('adc2std', anonymous=False, log_level=rospy.DEBUG)
        # rospy.init_node('slagent', anonymous=False,log_level=rospy.DEBUG)

        # Define Subscriber
        self.adcSub = rospy.Subscriber('/adc', Adc, self.AdcSubCB)

        # Define Publisher /mavros/rc/override (mavros/OverrideRCIn)
        self.pubShortHeight = rospy.Publisher("/arm/height", Int32, queue_size=10)
        self.pubLongHeight = rospy.Publisher("/arm/longHeight", Int32, queue_size=10)
        self.pubBladeImu = rospy.Publisher("/arm/blade/Imu", Imu, queue_size=10)

        # Init sequence:
        # publish pump om 1000 then on 2000

        rospy.spin()

if __name__ == '__main__':
    sys.path
    node = Adc2Std()
