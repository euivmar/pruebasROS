#! /usr/bin/env python

import rospy
# Import the service message used by the service /trajectory_by_name
from std_srvs.srv import Empty, EmptyRequest # you import the service message python classes generated from Empty.srv.
import sys

# Initialise a ROS node with the name service_client
rospy.init_node('move_bb8_service_client')
# Wait for the service client /move_bb8_in_circle to be running
rospy.wait_for_service('/move_bb8_in_circle')
# Create the connection to the service
move_bb8_con_service = rospy.ServiceProxy('/move_bb8_in_circle', Empty)
# Create an object of type EmptyRequest
move_bb8_con_object= EmptyRequest()
# Send the EmptyRequest
result = move_bb8_con_service(move_bb8_con_object)
# Print the result given by the service called
print(result)