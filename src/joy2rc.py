#!/usr/bin/env python3



import rospy
from std_msgs.msg import Header
from std_msgs.msg import Int32, Bool
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs import msg
from datetime import datetime


class Joy2RC(object):
    rcmsg = msg.OverrideRCIn()


    def JoyActionSubCB(self, data):
        joydata = data.axes
        buchna = data.buttons

        if buchna[6]==1:
            self.rcmsg.channels[4]=1000
        if buchna[7]==1:
            self.rcmsg.channels[4]=2000
        # print("joydata" + joydata.__str__())
        #
        rospy.logdebug("actions" + joydata.__str__())

        #compute throttle:
        #   button 5: 1=1500 -1=1900
        #   button 2: 1=1500 -1=1100
        #print("%.2f" % joydata[5])
        x = round(joydata[5],2)
        val = int(1700 - 200*x)
        if val == 1500:
            #print("forget val="+val.__str__())
            y = round(joydata[2], 2)
            other_val = int(1300 + y * 200)
            self.rcmsg.channels[0] = other_val
        else:
            self.rcmsg.channels[0] = val

        #print(other_val.__str__()+"|"+val.__str__()+"|"+((other_val+val)/2).__str__())

        #compute steering:
        # button 0: 0 = 1500
        # [0,1] = 1800-2000
        # [-1,0] = 1000-1200
        x = round(joydata[0],2)
        if x==0:
            val = 1500
        elif x > 0:
            val = int(1800+x*200)
        else:
            val = int(1200+x*200)
        self.rcmsg.channels[2] = val

        #compute arm height:
        # button 4: 0 = 1500
        # [0,-1] =[1900, 2100] - lower the arm
        # [0,1] = [900, 1100] -  raise the arm
        x = round(joydata[4],2)
        if x==0:
            val = 1500
        elif x > 0:
            val = int(900 + x*200)
        else:
            val = int(1900 -x*200)
        self.rcmsg.channels[1] = val

        #compute blade angle:
        # button 3: 0 = 1500
        # [0,1] = 1800-2000 left
        # [-1,0] = 1000-1200 right
        # Not sure
        x = round(joydata[3], 2)
        if x == 0:
            val = 1500
        elif x > 0:
            val = int(1800 + x * 200)
        else:
            val = int(1200 + x * 200)
        self.rcmsg.channels[3] = val

        rospy.logdebug("Publishing:"+self.rcmsg.__str__())
        self.pubRC.publish(self.rcmsg)


    def __init__(self):
        rospy.init_node('joy2rc', anonymous=False, log_level=rospy.DEBUG)
        # rospy.init_node('slagent', anonymous=False,log_level=rospy.DEBUG)

        # Define Subscriber
        self.joyActionSub = rospy.Subscriber('/joy', Joy, self.JoyActionSubCB)

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

        # Define Publisher /mavros/rc/override (mavros/OverrideRCIn)
        self.pubRC = rospy.Publisher("/mavros/rc/override", msg.OverrideRCIn, queue_size=10)
        # Init sequence:
        # publish pump om 1000 then on 2000
        self.pubRC.publish(self.rcmsg)
        self.rcmsg.channels[4] = 1000
        self.pubRC.publish(self.rcmsg)
        self.rcmsg.channels[4] = 2000
        self.pubRC.publish(self.rcmsg)

        print("Init sequence complete...")

        rospy.spin()

if __name__ == '__main__':
    node = Joy2RC()
