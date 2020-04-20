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
        rospy.logdebug("Got message:"+str(msg))
        self.msgHeightShort = msg.adc1
        self.pubShortHeight.publish(self.msgHeightShort)
        self.msgHeightLong = msg.adc0
        self.pubLongHeight.publish(self.msgHeightLong)
        # 1 degree = 0.0174532925 radian
        # We are getting adc2, adc3, adc4 in 0.01 degree
        rollRad = 1.74532925*msg.adc2
        pitchRad = 1.74532925*msg.adc3
        yawRad = 1.74532925*msg.adc4
        quat = toRW.euler_to_quaternion(rollRad, pitchRad, yawRad)
        self.bladeImuMsg.orientation.x = quat[0]
        self.bladeImuMsg.orientation.y = quat[1]
        self.bladeImuMsg.orientation.z = quat[2]
        self.bladeImuMsg.orientation.w = quat[3]

        self.pubBladeImu.publish(self.bladeImuMsg)


    def __init__(self, deblevel=rospy.INFO):

        if (len(sys.argv)>1):
            deblevel = int(sys.argv[1])
        print("ZZZZZZZZZ "+deblevel.__str__())
        print("xxxxxxxxxxxx"+ sys.argv.__str__())
        rospy.init_node('adc2std', anonymous=False,log_level=deblevel)
        # rospy.init_node('adc2std', anonymous=False,log_level=rospy.DEBUG)
        rospy.loginfo(rospy.get_name() + " initialized with Log Level:"+deblevel.__str__())
        rospy.get_name()

        # Define Subscriber
        self.adcSub = rospy.Subscriber('/adc', Adc, self.AdcSubCB)

        # Define Publisher /mavros/rc/override (mavros/OverrideRCIn)
        self.pubLongHeight = rospy.Publisher("/arm/height", Int32, queue_size=10)
        self.pubShortHeight = rospy.Publisher("/arm/shortHeight", Int32, queue_size=10)
        self.pubBladeImu = rospy.Publisher("/arm/blade/Imu", Imu, queue_size=10)

        # Init sequence:
        # publish pump om 1000 then on 2000

        rospy.spin()

if __name__ == '__main__':
    sys.path
    node = Adc2Std()
