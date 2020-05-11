#!/usr/bin/env python3

#
#   Correct for Logitech RumblePad
#
#   Mapping:
#      Truck navigation fw/bw steering left/right with the left mushroom
#      Blade Up/Down, Loader Oper/Close    with the right mushroom
#      Pump Off - Button 9
#      Pump On  - Button 10
#      The range of the axes is [-32767, 32767]
#




import sys
import rospy
from std_msgs.msg import Header
from std_msgs.msg import Int32, Bool
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs import msg
from datetime import datetime
from time import sleep


class Ltech22RC(object):
    rcmsg = msg.OverrideRCIn()


    def JoyActionSubCB(self, data):
        joydata = data.axes
        buchna = data.buttons

        if buchna[8]==1:
            self.rcmsg.channels[4]=1000
        if buchna[9]==1:
            self.rcmsg.channels[4]=2000
        # print("joydata" + joydata.__str__())
        #
        rospy.logdebug("actions" + joydata.__str__())

        #compute throttle:
        #   axe 5: <0 1=1500 -1=1900
        #   axe 5: >0 1=1500 -1=1100
        #print("%.2f" % joydata[5])
        #x = round(joydata[5],2)
        x=joydata[1]
        if x == 0:
            self.rcmsg.channels[0] = 1500
        else:
            temp_val = 400 * x / 1
            rounded_temp_val = round(temp_val, 0)
            val = int(1500 + rounded_temp_val)
            self.rcmsg.channels[0] = val

        #print(other_val.__str__()+"|"+val.__str__()+"|"+((other_val+val)/2).__str__())

        #compute steering:
        # axes[4] 0: 0 = 1500
        # [0,-32767] = 1800-2000
        # [0, 32767] = 1000-1200
        x = joydata[0]
        if x==0:
            val = 1500
        else:
            temp_val = 200 * x / 1
            rounded_temp_val = round(temp_val, 0)

            if x > 0:
                val = int(1200-rounded_temp_val)
            else:
                val = int(1800-rounded_temp_val)

        self.rcmsg.channels[2] = val

        #compute arm height:
        # axes[3] : 0 = 1500
        # [0,-32767] =[1900, 2100] - lower the arm
        # [0,32767] = [900, 1100] -  raise the arm
        x = joydata[3]
        if x==0:
            val = 1500
        else:
            temp_val = 200 * x / 1
            rounded_temp_val = round(temp_val, 0)
            if x > 0:
                val = int(1900+rounded_temp_val)
            else:
                val = int(1100+rounded_temp_val)

        self.rcmsg.channels[1] = val

        #compute blade angle:
        # axes[2]: 0 = 1500
        # [0,32767] = 1800-2000 left
        # [0,-32767] = 1000-1200 right
        # Not sure
        x = round(joydata[2], 2)
        if x == 0:
            val = 1500
        else:
            temp_val = 200 * x / 1
            rounded_temp_val = round(temp_val, 0)
            if x > 0:
                val = int(1200 - rounded_temp_val)
            else:
                val = int(1800 - rounded_temp_val)

        self.rcmsg.channels[3] = val

        rospy.logdebug("Publishing:"+self.rcmsg.__str__())
        self.pubRC.publish(self.rcmsg)


    def __init__(self, deblevel = rospy.INFO):

        if (len(sys.argv)>1):
            deblevel = int(sys.argv[1])

        rospy.init_node('ltech2rc', anonymous=False, log_level=deblevel)
        rospy.loginfo("ltech2rc initialized with Log Level:"+deblevel.__str__())
        # rospy.init_node('drag2rc', anonymous=False,log_level=rospy.DEBUG)

        # Define Subscriber
        self.joyActionSub = rospy.Subscriber('/joy', Joy, self.JoyActionSubCB)

        # Define Publisher /mavros/rc/override (mavros/OverrideRCIn)
        self.pubRC = rospy.Publisher("mavros/rc/override", msg.OverrideRCIn, queue_size=10)
#        self.pubRC = rospy.Publisher("mavros/rc/override", msg.OverrideRCIn, queue_size=10, latch=True)


        # Define Default Values RC Topic
        self.rcmsg.channels = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.rcmsg.channels[0] = 1500  # throttle
        self.rcmsg.channels[1] = 1500  # arm
        self.rcmsg.channels[2] = 1500  # steering
        self.rcmsg.channels[3] = 1500  # BladeArm
        self.rcmsg.channels[4] = 1500  # Oil Pump
        self.rcmsg.channels[5] = 1500  # Gear - NA
        self.rcmsg.channels[6] = 1500  # NA
        self.rcmsg.channels[7] = 1500  # NA

        # The publisher needs a bit of time before starting publishing
        sleep(0.5)
        # Init sequence:
        # publish pump om 1000 then on 2000
        rospy.logdebug("Publishing:"+self.rcmsg.__str__())
        self.pubRC.publish(self.rcmsg)

        self.rcmsg.channels[4] = 1000
        rospy.logdebug("Publishing:"+self.rcmsg.__str__())
        self.pubRC.publish(self.rcmsg)

        self.rcmsg.channels[4] = 2000
        rospy.logdebug("Publishing:"+self.rcmsg.__str__())
        self.pubRC.publish(self.rcmsg)

        rospy.loginfo("Init sequence complete...")

        rospy.spin()

if __name__ == '__main__':
    try:
        node = Ltech22RC()
    except rospy.ROSInterruptException:
        print("rospy.ROSInterruptException: " + node.__module__ )
        pass



