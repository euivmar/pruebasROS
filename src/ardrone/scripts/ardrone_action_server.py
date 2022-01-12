#! /usr/bin/env python
import rospy
import time

import actionlib

from actionlib.msg import TestFeedback, TestResult, TestAction

from std_msgs.msg import Int32, Empty 

from geometry_msgs.msg import Twist

class ArdroneClass(object):
    
  # create messages that are used to publish feedback/result
  _feedback = TestFeedback()
  _result   = TestResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("ardrone_as", TestAction, self.goal_callback, False)
    self._as.start()
    self._pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
  def performSide(self,side,squareSize):
      # check that preempt (cancelation) has not been requested by the action client
    success = True
    if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        # the following line, sets the client in preempted state (goal cancelled)
        self._as.set_preempted()
        success = False

    else:
        # builds the next feedback msg to be sent
        self._feedback.feedback=side

        rospy.loginfo('Moving along square side %i', side)
        # publish the feedback
        self._as.publish_feedback(self._feedback)

        #first stop
        var = Twist()
        var.linear.x=0
        var.linear.y=0
        self._pub.publish(var)

        #change vel according square side
        if(side==1): 
            var.linear.x=0.5
        if(side==2): 
            var.linear.y=0.5
        if(side==3): 
            var.linear.x=-0.5
        if(side==4): 
            var.linear.y=-0.5

        self._pub.publish(var)
        
        rospy.sleep(squareSize)
        if(side==4): 
            var.linear.x=0
            var.linear.y=0
            self._pub.publish(var)
    return success
 

  def goal_callback(self, goal):
    # this callback is called when the action server is called.
    # this is the function that move the drone forming a square
    # and returns the total time
    
    # helper variables
    rate = rospy.Rate(1)
    success = True

    
    squareSize = goal.goal

    # publish info to the console for the user
    rospy.loginfo('"ardrone_as": Executing, moving drone with a square of size %i' %( squareSize))
    
    # starts perfoming the movement

    for side in range(1, 5):
        success=self.performSide(side,squareSize)
        if success==False:
            break
    
    # at this point, either the goal has been achieved (success==true)
    # or the client preempted the goal (success==false)
    # If success, then we publish the final result
    # If not success, we do not publish anything in the result
    if success:
      self._result = squareSize*4
      rospy.loginfo('Succeeded perfoming the square movement' )
      self._as.set_succeeded(self._result)
      
if __name__ == '__main__':
  rospy.init_node('ardrone_server')
  ArdroneClass()
  rospy.spin()
