#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry 
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist



def callback(msg): 
    
    laserRanges=msg.ranges
    varVel = Twist()
    #No front obstacle <1 -> Move forward
    if(laserRanges[360]>1 and laserRanges[280]>1 and  laserRanges[420]>1):
        varVel.linear.x=0.5
        print ("Move Forward")
    else:
        #Turn left
        varVel.angular.z=0.8
        
        #if right obstacle <1 -> just rotate
        if(laserRanges[0]<1 or laserRanges[10]<1 or laserRanges[75]<1 or laserRanges[100]<1):
            varVel.linear.x=0
            print ("Rotate Left")
        else:
            print ("Move forward and rotate")
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    pub.publish(varVel)
  
    


rospy.init_node('topics_quiz_node')

sub = rospy.Subscriber('//kobuki/laser/scan', LaserScan, callback)
rospy.spin()