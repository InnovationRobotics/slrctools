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

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
#import sensor_msgs.msg
from sensor_msgs.msg import Joy
from std_msgs.msg import Header


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', heightsub.data)

def actions():
    pubteststring = rospy.Publisher('testjoy', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    heightsub = rospy.Subscriber('arm/height', Int32, callback)
  #  testsub = rospy.Subscriber('joy', Joy, callback)
    pubjoy = rospy.Publisher("joy", Joy, queue_size=10 )
    joymessage = Joy()
    joymessage.header = Header
    joymessage.header.stamp = rospy.get_time()
    joymessage.axes =  [-0.0, -0.0, 0.0, 0.0, 0.0, 0.0]
    joymessage.buttons= [0] * 12
    #print(joymessage)
    for i in range(8):
    #    joymessage.axes[i] = 0.0
        joymessage.buttons[i] = 0

    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
#        rospy.loginfo(hello_str)
        pubteststring.publish(hello_str)
        #joymessage.axes[0] = "0.1"
        #joymessage.buttons[2] = "0.2"
        pubjoy.publish(joymessage)
        #rospy.loginfo(joymessage)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('slagent', anonymous=True)
    try:
        actions()
    except rospy.ROSInterruptException:
        pass
