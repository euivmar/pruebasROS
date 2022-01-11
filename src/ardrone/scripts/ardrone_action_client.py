#! /usr/bin/env python
import rospy
import time
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from std_msgs.msg import Int32, Empty 

from geometry_msgs.msg import Twist

"""
class SimpleGoalState:
    PENDING = 0
    ACTIVE = 1
    DONE = 2
    WARN = 3
    ERROR = 4

"""
# We create some constants with the corresponing vaules from the SimpleGoalState class
PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

nImage = 1

#Configure to take off and land drone
pubTakeOff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
pubLand = rospy.Publisher('/drone/land', Empty, queue_size=1)

def publish_once_in_takeoff():
        rate = rospy.Rate(1)
        success=False
        while not success:
            connections = pubTakeOff.get_num_connections()
            if connections > 0:
                pubTakeOff.publish(Empty())
                rospy.loginfo("TakeOff Published")
                success=True
            else:
                rate.sleep()

def publish_once_in_land():
    rate = rospy.Rate(1)
    success=False
    while not success:
        connections = pubLand.get_num_connections()
        if connections > 0:
            pubLand.publish(Empty())
            rospy.loginfo("Land Published")
            success=True
            rate.sleep()

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def feedback_callback(feedback):
    global nImage
    print('[Feedback] image n.%d received'%nImage)
    nImage += 1

# initializes the action client node
rospy.init_node('drone_action_client')

# create the connection to the action server
client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
# waits until the action server is up and running
client.wait_for_server()

# creates a goal to send to the action server
goal = ArdroneGoal()
goal.nseconds = 10 # indicates, take pictures along 10 seconds

# sends the goal to the action server, specifying which feedback function
# to call when feedback received
client.send_goal(goal, feedback_cb=feedback_callback)

# Uncomment these lines to test goal preemption:
#time.sleep(3.0)
#client.cancel_goal()  # would cancel the goal 3 seconds after starting

# wait until the result is obtained
# you can do other stuff here instead of waiting
# and check for status from time to time 
# status = client.get_state()
# check the client API link below for more info

#Configure publication topics to move the drone
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

var = Twist()
var.linear.x=0.5
var.angular.z=0.1

state_result = client.get_state()

rate = rospy.Rate(1)


rospy.loginfo("state_result: "+str(state_result))
publish_once_in_takeoff()
while state_result < DONE:
    rospy.loginfo("Doing Stuff while waiting for the Server to give a result....")
    pub.publish(var)
    rate.sleep()
    state_result = client.get_state()
    rospy.loginfo("state_result: "+str(state_result))

#Stop the drone
var.linear.x=0.5
var.angular.z=0.1    
pub.publish(var)
publish_once_in_land()

rospy.loginfo("[Result] State: "+str(state_result))
if state_result == ERROR:
    rospy.logerr("Something went wrong in the Server Side")
if state_result == WARN:
    rospy.logwarn("There is a warning in the Server Side")

print('[Result] State: %d'%(client.get_state()))
