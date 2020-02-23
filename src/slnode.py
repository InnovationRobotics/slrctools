#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$


import rospy
from std_msgs.msg import Header
from std_msgs.msg import Int32, Bool
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped, TwistStamped

MAX_NUM_STONES = 10
#global stonePoseSub[]
#global stoneIsLoaded[MAX_NUM_STONES]
#global vehiclePositionSub, vehicleVelocitySub, heightSub, bladeImuSub, vehicleImuSub

world_state = {}
joyactions = {}

def VehiclePositionCB(stamped_pose):
    rospy.logdebug("I was called here")
    type(stamped_pose)
 #   pose = stamped_pose.pose
 #   position = pose.position
 #   rospy.loginfo("I was called...")
    world_state['VehiclePosition'] = stamped_pose
    rospy.logdebug('position is:' + str(stamped_pose))

def VehicleVelocityCB(stamped_twist):
    twist = stamped_twist.twist
    world_state['VehicleVelocity'] = stamped_twist
    rospy.logdebug('velocity is:' + str(twist))

def ArmHeightCB(data):
    height=data.data
    world_state['ArmHeight'] = height
    rospy.logdebug('arm height is:' + str(height))

def BladeImuCB(imu):
    orientation=imu.orientation
    angular_velocity = imu.angular_velocity
    linear_acceleration = imu.linear_acceleration
    world_state['BladeImu'] = imu
    rospy.logdebug('blade imu is:' + str(imu))

def VehicleImuCB(imu):
    orientation = imu.orientation
    angular_velocity = imu.angular_velocity
    linear_acceleration = imu.linear_acceleration
    world_state['VehicleImu'] = imu
    rospy.logdebug('vehicle imu is:' + str(imu))


def StonePositionCB(data, arg):
    position=data.pose
    stone=arg
    world_state['StonePosition'+str(stone)] = position
    rospy.logdebug('stone '+str(stone)+ ' position is:' + str(position))

def StoneIsLoadedCB(data, arg):
    question=data.data
    stone=arg
    world_state['StoneIsLoaded'+str(stone)] = question
    rospy.logdebug('Is stone '+str(stone)+ ' loaded? ' + str(question))

def actions():
    print(joyactions)
    joymessage = Joy()
    joymessage.header = Header
    joymessage.header.stamp = rospy.get_time()
 #   joymessage.axes =  [-0.0, -0.0, 0.0, 0.0, 0.0, 0.0]
    joymessage.axes =  [joyactions["0"], joyactions["1"], joyactions["2"], joyactions["3"], joyactions["4"], joyactions["5"]]
    joymessage.buttons= [0] * 12
    print(joymessage)

    while not rospy.is_shutdown():
        joymessage.axes[0] = "0.1"
        joymessage.buttons[2] = "1"
#        pubjoy.publish(joymessage)
        #rospy.loginfo(joymessage)
        rate.sleep()

def __init__():
    rospy.init_node('slagent', anonymous=False)
    #rospy.init_node('slagent', anonymous=False,log_level=rospy.DEBUG)

    #Define Subscribers
    vehiclePositionSub = rospy.Subscriber('mavros/local_position/pose', PoseStamped, VehiclePositionCB)
    vehicleVelocitySub = rospy.Subscriber('mavros/local_position/velocity', TwistStamped, VehicleVelocityCB)
    heightSub = rospy.Subscriber('arm/height', Int32, ArmHeightCB)
    bladeImuSub = rospy.Subscriber('arm/blade/Imu', Imu, BladeImuCB)
    vehicleImuSub = rospy.Subscriber('mavros/imu/data', Imu, VehicleImuCB)

    stoneIsLoadedSubList = []
    stonePoseSubList = []
    for i in range(MAX_NUM_STONES):
        topicName = 'stone/'+str(i)+'/Pose'
        stonePoseSubList.append(rospy.Subscriber(topicName, PoseStamped, StonePositionCB, i))
        #stonePoseSub[i] = rospy.Subscriber(topicName, PoseStamped, StonePositionCB, i)
        topicName = 'stone/'+ str(i)+'/IsLoaded'
        stoneIsLoadedSubList.append(rospy.Subscriber(topicName, Bool, StoneIsLoadedCB, i))
    rospy.spin()
    #Define Publishers
    joyactions["0"] = 0
    joyactions["1"] = joyactions["2"] = 0
    joyactions["3"] = joyactions["4"] = 0
    joyactions["5"] = 0

    pubjoy = rospy.Publisher("joy", Joy, queue_size=10 )
    rate = rospy.Rate(10) # 10hz

def run():
    try:
        actions()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    __init__()
    run()
