#!/usr/bin/env python

"""
Author: David Valencia
Description: Code para genrara un referencia Lemniscata(signo de infinito) 

"""

import roslib
import rospy
import math
import numpy as np 

from geometry_msgs.msg import Vector3, Twist

def publish_velocities(x,y,z):

	tw = Twist(Vector3(x,y,z), Vector3(0,0,0))
	pub.publish(tw)


if __name__ == '__main__':

	pub = rospy.Publisher('position_referencia', Twist,queue_size=1)
	rospy.init_node('referencia')
	
	alfa = 5 #RADIO 	

	
	try:
		while not rospy.is_shutdown():

			for i in range (360):

				x=  alfa *  (math.cos(math.radians(i))) /  ((math.sin(math.radians(i)))**2 + 1)
				y=  alfa * (math.cos(math.radians(i)))* (math.sin(math.radians(i))) / ((math.sin(math.radians(i)))**2 + 1)
				z=2

				print x
				print y 

				rospy.sleep(0.1)
				publish_velocities(x, y, z)

	

	except rospy.ROSInterruptException:
		pass
	