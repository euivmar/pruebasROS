#! /usr/bin/env python

import rospy
from bb8_move_circle_class import MoveBB8
from my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse # you import the service message python classes 

def my_callback(request):
    rospy.loginfo("The Service move_bb8_in_circle has been called with a duration of "+str(request.duration))
    movebb8_object = MoveBB8()
    movebb8_object.move_bb8(0.2,0.2,request.duration)
    rospy.loginfo("Finished service move_bb8_in_circle")

    my_response=MyCustomServiceMessageResponse()
    my_response.success=True
    return my_response

rospy.init_node('service_move_bb8_in_circle_server') 
my_service = rospy.Service('/move_bb8_in_circle', MyCustomServiceMessage , my_callback)
rospy.loginfo("Service /move_bb8_in_circle Ready")
rospy.spin() # keep the service open.
