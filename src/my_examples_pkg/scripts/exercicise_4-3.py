#! /usr/bin/env python

import rospy

from my_examples_pkg.msg import Age

rospy.init_node('topic_publisher')
pub = rospy.Publisher('/Age', Age, queue_size=1)
rate = rospy.Rate(2)
var = Age()

var.years=2021
var.months=11
var.days=13

while not rospy.is_shutdown(): 
  pub.publish(var)
  rate.sleep()