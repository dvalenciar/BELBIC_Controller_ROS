#!/usr/bin/env python

"""
Author: David Valencia
Description: Code para genrara un referencia circular de radio r 

"""

import roslib
import rospy
import math

from geometry_msgs.msg import Vector3, Twist

def publish_velocities(x,y,z):

	tw = Twist(Vector3(x,y,z), Vector3(0,0,0))
	pub.publish(tw)


if __name__ == '__main__':

	pub = rospy.Publisher('position_referencia', Twist,queue_size=10)
	rospy.init_node('referencia')
	r=5 #RADIO 	
	
	#outfile = open('/home/david/Dropbox/tum_simulator_ws/src/controladores/scripts/datos.txt', 'w')
	
	try:
		while not rospy.is_shutdown():

			for i in range (360):

				x= r *  (math.cos(math.radians(i)))
				y= r *  (math.sin(math.radians(i)))
				z=2



				print x
				print y 
				

				rospy.sleep(0.1)
				
				#outfile.write(str(x))
				#outfile.write(',')
				#outfile.write(str(y))

				#outfile.write('\n')

				publish_velocities(x, y, z)

				#outfile.close()

	except rospy.ROSInterruptException:
		pass
	