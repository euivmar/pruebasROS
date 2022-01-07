#! /usr/bin/env python

import rospy
from my_custom_srv_msg_pkg.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse # you import the service message python classes 
from geometry_msgs.msg import Twist 

def move_circle():
     move = Twist() 

     move.linear.x = 1 

     move.angular.z = 1 

     pub.publish(move) 

def stop():
     move = Twist() 

     move.linear.x = 0

     move.angular.z = 0 

     pub.publish(move) 

def my_callback(request):
    print("My_callback has been called")
    move_circle()
    print(f'Tiempo{request.duration} seg')
    rospy.sleep(request.duration)
    stop()
    my_response = MyCustomServiceMessageResponse()
    my_response.success = True
    return my_response # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('service_server') 
my_service = rospy.Service('/move_bb8_in_circle_custom', MyCustomServiceMessage , my_callback) # create the Service called my_service with the defined callback

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) 

# rate = rospy.Rate(2) 

move = Twist()

rospy.spin() # maintain the service open.