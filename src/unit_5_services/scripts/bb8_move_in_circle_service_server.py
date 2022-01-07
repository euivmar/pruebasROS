#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse # you import the service message python classes generated from Empty.srv.
from geometry_msgs.msg import Twist 

def move_circle():
     move = Twist() 

     move.linear.x = 1 

     move.angular.z = 1 

     pub.publish(move) 

def my_callback(request):
    print("My_callback has been called")
    move_circle()
    return EmptyResponse() # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('service_server') 
my_service = rospy.Service('/move_bb8_in_circle', Empty , my_callback) # create the Service called my_service with the defined callback

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) 

# rate = rospy.Rate(2) 

move = Twist() 

rospy.spin() # maintain the service open.