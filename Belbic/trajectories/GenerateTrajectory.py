#!/usr/bin/env python

"""
Author: David Valencia
Description: Cubic polynomical functions for trajectory 

"""

import rospy 
import os
from   geometry_msgs.msg     import Twist,Vector3,PoseStamped, Pose
from   nav_msgs.msg import  Path 

def cubic_polynomial(c0, cf, t_fin, t):


	a0 = c0
	a1 = 0.0
	a2 = 3 * (cf - c0) / t_fin ** 2
	a3 =-2 * (cf - c0) / t_fin ** 3

	p = a0 + (a1*t)    + (a2 * (t**2)) + (a3 * (t**3))
	v = a1 + (2* a2*t) + (3  * a3*(t **2))

	return p,v


def cubic_polynomial_setVel(c0, cf, t_fin, t, Vo = 0, Vf = 0):


	a0 = c0
	a1 = Vo

	a2 = ((3 * (cf - c0))  - ((Vf + 2 * Vo) * t_fin) )/ t_fin ** 2
	a3 = ((-2 * (cf - c0)) + ((Vf  + Vo) * t_fin) )/ t_fin ** 3

	p = a0 + (a1*t)    + (a2 * (t**2)) + (a3 * (t**3))
	v = a1 + (2* a2*t) + (3  * a3*(t **2))

	return p,v

def rvizPpath(px,py,pz):

	pose = PoseStamped() 
	msg = Path()   

	#Set a atributes of the msg
	pose.header.frame_id = "nav"
	pose.pose.position.x = px
	pose.pose.position.y = py
	pose.pose.position.z = pz

	pose.pose.orientation.w = 1
	
	pose.header.seq     = msg.header.seq + 1
	msg.header.frame_id ="nav"
	msg.header.stamp    =rospy.Time.now()
	pose.header.stamp   = msg.header.stamp
	msg.poses.append(pose)

	return msg


if __name__ == '__main__':
	
	TimeStart = 0.0
	Time      = 0.0
	rospy.init_node("Trajectory_Generator")
	cmd_vel_publisher = rospy.Publisher('position_referencia', Twist,queue_size=1)
	markerPub         = rospy.Publisher('trajectory_marker',   Path, queue_size=1) # esto es para luego poder graficar en el rviz

	graph_data  = open("/home/david/Dropbox/tum_simulator_ws/src/Belbic/trajectories/waypoints.txt","r").read()
	#graph_data  = open("/drone_simulation_ws/src/Belbic/trajectories/waypoints.txt","r").read()
	lines       = graph_data.split ('\n')

	pos0       = [-12.0,-12.0,10.0] # initial position
	
	for line in lines:
 	
		if len (line) > 1:


			xf,yf,zf,tf = line.split(',')

			tf   = float (tf)
			posf = [float(xf), float(yf), float(zf)]  # goal   position

			# Define the duration:
			Tf = tf

			rate = rospy.Rate(55.0)

			while not rospy.is_shutdown() and Time < Tf:

				current_time = rospy.get_time()

				if TimeStart == 0:
				   TimeStart = current_time   
				Time = current_time - TimeStart

				px,vx = cubic_polynomial(pos0[0],posf[0],Tf,Time)
				py,vy = cubic_polynomial(pos0[1],posf[1],Tf,Time)
				pz,vz = cubic_polynomial(pos0[2],posf[2],Tf,Time)
				print px,py,pz

				tw = Twist(Vector3(px,py,pz), Vector3(0,0,0))
				#tw = Twist(Vector3(px,py,pz), Vector3(vx,vy,vz))
				cmd_vel_publisher.publish(tw)


				tra_rviz = rvizPpath(px, py,pz)
				markerPub.publish(tra_rviz)

				
				rate.sleep()

			pos0 = [posf[0],posf[1],posf[2]]
			Time = 0
			TimeStart = 0





