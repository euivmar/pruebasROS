#! /usr/bin/env python
import rospy
import actionlib

from actions_quiz.msg import  CustomActionMsgFeedback, CustomActionMsgAction
from std_msgs.msg import Empty

class actionQuizClass(object):
    
  # create messages that are used to publish feedback/result
  _feedback = CustomActionMsgFeedback()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("action_custom_msg_as", CustomActionMsgAction, self.goal_callback, False)
    self._as.start()
    rospy.loginfo("ActionQuiz Server started")
    
  def goal_callback(self, goal):
    r = rospy.Rate(1)
    success = True

    if goal.goal.upper() == 'TAKEOFF':
        self._feedback.feedback = "TAKEOFF"
        self._as.publish_feedback(self._feedback)
        self.publish_once_in_takeoff()
        if self._as.is_preempt_requested():
            rospy.loginfo('The goal has been cancelled/preempted')
            self._as.set_preempted()
            success = False
    
    elif goal.goal.upper() == 'LAND':
        self._feedback.feedback = "LAND"
        self._as.publish_feedback(self._feedback)
        self.publish_once_in_land()
        if self._as.is_preempt_requested():
            rospy.loginfo('The goal has been cancelled/preempted')
            self._as.set_preempted()
            success = False
    
    else:
        rospy.loginfo('Bad input %s',goal.goal)
        success = False
    
    r.sleep()
    if success:
        rospy.loginfo('Succeeded')
        self._as.set_succeeded()
    else:
        self._as.set_aborted(result=None,text="Bad Input")

       
  def publish_once_in_takeoff(self):
        pubTakeOff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
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

  def publish_once_in_land(self):
    pubLand = rospy.Publisher('/drone/land', Empty, queue_size=1)
    rate = rospy.Rate(1)
    success=False
    while not success:
        connections = pubLand.get_num_connections()
        if connections > 0:
            pubLand.publish(Empty())
            rospy.loginfo("Land Published")
            success=True
            rate.sleep()


if __name__ == '__main__':
  rospy.init_node('action_custom_msg_as')
  actionQuizClass()
  rospy.spin()