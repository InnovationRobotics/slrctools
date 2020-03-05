import rospy
from sensor_msgs.msg import Joy
import csv
from datetime import datetime

actions = {}

def JoyActionSubCB(data):
    joydata = data.axes
    actions['Date&Time'] = datetime.now().strftime("%d-%m,%H:%M:%S")
    actions['Buttons'] = joydata
    rospy.logdebug("joydata"+joydata.__str__())
    rospy.logdebug("actions"+actions.__str__())
    with open('oprecorder.csv', 'a', newline='') as csvfile:
        fieldnames = ['Date&Time', 'Buttons']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(actions)


rospy.init_node('oprecorder', anonymous=False, log_level=rospy.DEBUG)

joyActionSub = rospy.Subscriber('/joy', Joy, JoyActionSubCB)

with open('oprecorder.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date&Time', 'Buttons']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

rospy.spin()