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



class SlRosNode(object):
    MAX_NUM_STONES = 10
#global stonePoseSub[]
#global stoneIsLoaded[MAX_NUM_STONES]
#global vehiclePositionSub, vehicleVelocitySub, heightSub, bladeImuSub, vehicleImuSub

    world_state = {}
    joyactions = {}

    def SetActionValues(self, values):
        self.joyactions["0"] = values["0"]
        self.joyactions["1"] = values["1"]
        self.joyactions["2"] = values["2"]
        self.joyactions["3"] = values["3"]
        self.joyactions["4"] = values["4"]
        self.joyactions["5"] = values["5"]

    def VehiclePositionCB(self,stamped_pose):
        rospy.logdebug("I was called here")
        type(stamped_pose)
        #   pose = stamped_pose.pose
        #   position = pose.position
        #   rospy.loginfo("I was called...")
        self.world_state['VehiclePosition'] = stamped_pose

        self.computeActions()
 #       self.actions()
        rospy.loginfo('position is:' + str(stamped_pose))

    def VehicleVelocityCB(self, stamped_twist):
        twist = stamped_twist.twist
        self.world_state['VehicleVelocity'] = stamped_twist
        rospy.logdebug('velocity is:' + str(twist))

    def ArmHeightCB(self, data):
        height = data.data
        self.world_state['ArmHeight'] = height
        rospy.logdebug('arm height is:' + str(height))

    def BladeImuCB(self, imu):
        orientation = imu.orientation
        angular_velocity = imu.angular_velocity
        linear_acceleration = imu.linear_acceleration
        self.world_state['BladeImu'] = imu
        rospy.logdebug('blade imu is:' + str(imu))

    def VehicleImuCB(self, imu):
        orientation = imu.orientation
        angular_velocity = imu.angular_velocity
        linear_acceleration = imu.linear_acceleration
        self.world_state['VehicleImu'] = imu
        rospy.logdebug('vehicle imu is:' + str(imu))

    def StonePositionCB(self, data, arg):
        position = data.pose
        stone = arg
        self.world_state['StonePosition' + str(stone)] = position
        rospy.logdebug('stone ' + str(stone) + ' position is:' + str(position))

    def StoneIsLoadedCB(self, data, arg):
        question = data.data
        stone = arg
        self.world_state['StoneIsLoaded' + str(stone)] = question
        rospy.logdebug('Is stone ' + str(stone) + ' loaded? ' + str(question))

    def computeActions(self):
        actionValues = {"0": 0.0, "1": 0.1, "2": 0.2, "3": 0.3, "4": 0.4, "5": 0.5}
        self.SetActionValues(actionValues)

    def __init__(self):
        rospy.init_node('slagent', anonymous=False)
        # rospy.init_node('slagent', anonymous=False,log_level=rospy.DEBUG)

        # Define Subscribers
        self.vehiclePositionSub = rospy.Subscriber('mavros/local_position/pose', PoseStamped, self.VehiclePositionCB)
        self.vehicleVelocitySub = rospy.Subscriber('mavros/local_position/velocity', TwistStamped, self.VehicleVelocityCB)
        self.heightSub = rospy.Subscriber('arm/height', Int32, self.ArmHeightCB)
        self.bladeImuSub = rospy.Subscriber('arm/blade/Imu', Imu, self.BladeImuCB)
        self.vehicleImuSub = rospy.Subscriber('mavros/imu/data', Imu, self.VehicleImuCB)

        self.stoneIsLoadedSubList = []
        self.stonePoseSubList = []
        for i in range(self.MAX_NUM_STONES):
            topicName = 'stone/' + str(i) + '/Pose'
            self.stonePoseSubList.append(rospy.Subscriber(topicName, PoseStamped, self.StonePositionCB, i))
            # stonePoseSub[i] = rospy.Subscriber(topicName, PoseStamped, StonePositionCB, i)
            topicName = 'stone/' + str(i) + '/IsLoaded'
            self.stoneIsLoadedSubList.append(rospy.Subscriber(topicName, Bool, self.StoneIsLoadedCB, i))
       # rospy.spin()
        # Define Publishers
        self.joyactions["0"] = 0
        self.joyactions["1"] = self.joyactions["2"] = 0
        self.joyactions["3"] = self.joyactions["4"] = 0
        self.joyactions["5"] = 0

        self.pubjoy = rospy.Publisher("joy", Joy, queue_size=10)
        self.rate = rospy.Rate(10)  # 10hz
#        self.actions()
#        rospy.spin()
       # self.actions()


    def actions(self):
            rospy.logdebug(self.joyactions)
            joymessage = Joy()
            #joymessage.header = Header
           # joymessage.header.stamp = rospy.get_time()
            #   joymessage.axes =  [-0.0, -0.0, 0.0, 0.0, 0.0, 0.0]
            joymessage.axes = [self.joyactions["0"], self.joyactions["1"], self.joyactions["2"], self.joyactions["3"], self.joyactions["4"],
                               self.joyactions["5"]]
            joymessage.buttons = [0] * 12
            rospy.logdebug("Here also I am: ")
            rospy.logdebug(joymessage)

            while not rospy.is_shutdown():
                joymessage.axes = [self.joyactions["0"], self.joyactions["1"], self.joyactions["2"], self.joyactions["3"], self.joyactions["4"], self.joyactions["5"]]
                self.pubjoy.publish(joymessage)
                rospy.logdebug(joymessage)
                self.rate.sleep()

    def run(self):
           try:
               #rospy.spin()
               self.actions()
           except rospy.ROSInterruptException:
                pass

if __name__ == '__main__':
    node = SlRosNode()
    node.run()
