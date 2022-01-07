#! /usr/bin/env python

import rospy
# Import the service message used by the service /trajectory_by_name
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest # you import the service message python classes 
import sys

# Initialise a ROS node with the name service_client
rospy.init_node('move_bb8_service_client')
# Wait for the service client /move_bb8_in_circle to be running
rospy.wait_for_service('/move_bb8_in_square_custom')
# Create the connection to the service
move_bb8_con_service = rospy.ServiceProxy('/move_bb8_in_square_custom', BB8CustomServiceMessage)
# Create an object of type EmptyRequest
move_bb8_con_object= BB8CustomServiceMessageRequest()
move_bb8_con_object.side=2
move_bb8_con_object.repetitions=2
# Send the EmptyRequest
result = move_bb8_con_service(move_bb8_con_object)

# Create an object of type EmptyRequest
move_bb8_con_object= BB8CustomServiceMessageRequest()
move_bb8_con_object.side=4
move_bb8_con_object.repetitions=1
# Send the EmptyRequest
result = move_bb8_con_service(move_bb8_con_object)

# Print the result given by the service called
print(result)