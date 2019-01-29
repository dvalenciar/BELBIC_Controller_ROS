#!/usr/bin/env python

"""
Author     : David Valencia
Description: BELBIC controller for autonomous navigation 
Date       : 28/01/2019	
"""

import rospy 
import math
import numpy
import time 

from   nav_msgs.msg            import Odometry
from   ardrone_autonomy.msg    import Navdata
from   geometry_msgs.msg       import Twist
from   Rotation_Transformacion import *



class LecturePosicion:

	def __init__(self):

		rospy.Subscriber("ground_truth/state",       Odometry,  self.pose_callback)
		rospy.Subscriber("navdata",                  Navdata,   self.ang_callback)
		rospy.Subscriber("position_referencia",      Twist,     self.droneReferencia)
		
		self.movePub = rospy.Publisher ("cmd_vel", Twist, queue_size=10)


		#Initial Values

		self.posx_dron = 0.0
		self.posy_dron = 0.0
		self.posz_dron = 0.0
		
		self.roll_dron = 0.0 
		self.pich_dron = 0.0 
		self.yaw_dron  = 0.0

		self.X_d       = 0.0   
		self.Y_d       = 0.0
		self.Z_d       = 2.0
		self.yaw_d     = 0.0

		self.Vth       = 0.0
		self.w         = 0.0
		self.v         = 0.0

		self.alfa      = 0.00002
		self.beta      = 0.00009


	def pose_callback(self, pose_data):
	
		self.posx_dron = pose_data.pose.pose.position.x
		self.posy_dron = pose_data.pose.pose.position.y
		self.posz_dron = pose_data.pose.pose.position.z

	def ang_callback(self, ang_data):

		self.roll_dron  = ang_data.rotX  # angle of the drone in gradients
		self.pich_dron  = ang_data.rotY  # angle of the drone in gradients
		self.yaw_dron   = ang_data.rotZ  # angle of the drone in gradients

	def droneReferencia(self, data):

		self.X_d   = data.linear.x  # References points
		self.Y_d   = data.linear.y
		self.Z_d   = data.linear.z
		self.yaw_d = data.angular.z


	def calculos(self):

		rate = rospy.Rate(10) # 10hz

		Cnt_Z_REW   = pd_controller(5.4  ,  0.5) 
		Cnt_X_REW   = pd_controller(4.0  ,  7.5) 
		Cnt_Y_REW   = pd_controller(4.0  ,  7.5)
		Cnt_Yaw_REW = pd_controller(0.02 , 0.00)

		Cnt_Z_SI   = pid_controller(0.5  ,  0.04 , 0.00) 
		Cnt_X_SI   = pid_controller(1.3  ,  1.8  , 0.0001) 
		Cnt_Y_SI   = pid_controller(1.3  ,  1.8  , 0.0001)
		Cnt_Yaw_SI = pid_controller(0.02 , 0.00  , 0.00)


		while not rospy.is_shutdown():

				teta 	  = [ 0, 0, self.yaw_dron]
				R    	  = eulerAnglesToRotationMatrix(teta)
				T_inversa = Homogenius_Inversa(R, 0,0,0)
				position  = np.array ([[self.posx_dron], [self.posy_dron],[self.posz_dron], [1] ])
				dron      = np.dot   (T_inversa , position) 
				
				x_dron = dron[0]
				y_dron = dron[1]
				z_dron = dron[2]

				position_deseada    = np. array ([[self.X_d],[self.Y_d],[self.Z_d],[1]])
				positionDesada_dron = np.dot(T_inversa , position_deseada) 


				xd_dron = positionDesada_dron[0]
				yd_dron = positionDesada_dron[1]
				zd_dron = positionDesada_dron[2]
				
				error_x   = xd_dron  - x_dron
				error_y   = yd_dron  - y_dron  
				error_z   = self.Z_d    - self.posz_dron
				error_yaw = self.yaw_d  - self.yaw_dron


				#  REW signal for BELBIC

				REW_Z   = Cnt_Z_REW.set_REW(error_z) 
				REW_X   = Cnt_X_REW.set_REW(error_x) 
				REW_Y   = Cnt_Y_REW.set_REW(error_y) 
				REW_YAW = Cnt_Yaw_REW.set_REW(error_yaw) 

				#  SI signal for BELBIC
				SI_Z   =  Cnt_Z_SI.set_SI(error_z)
				SI_X   =  Cnt_X_SI.set_SI(error_x) 
				SI_Y   =  Cnt_Y_SI.set_SI(error_y)
				SI_YAW =  Cnt_Yaw_SI.set_SI(error_yaw)


				U1 = self.Belbic(SI_Z,   REW_Z,    0.7)
				U4 = self.Belbic(SI_YAW, REW_YAW,  0.2) 
				U2 = self.Belbic(SI_X,   REW_X,    1.0) 
				U3 = self.Belbic(SI_Y,   REW_Y,    1.0) 


				self.Action(U1,U2,U3,U4)

				rate.sleep()

	def Belbic (self, SI, REW, limite):

		_limit_out = limite

		A   = (self.v   * SI)
		O   = (self.w   * SI)
		MO  = (A - O) 

		#Ath = (self.Vth * SI)
		#MO  = ((Ath + A) - O) 

		rest = REW - A

		if rest < 0 :
		   rest = 0
		else:
		   pass

		dv   = self.alfa * (rest)     * SI
		dw   = self.beta * (MO - REW) * SI
		#dvth = self.alfa * (rest)     * SI
		print dv 

		self.v   = self.v + dv  
		self.w   = self.w + dw  
		#self.Vth = self.Vth + dvth 

		U = MO

		if   U  >   _limit_out:
			 U  =   _limit_out
		elif U  <  -_limit_out:
			 U  =  -_limit_out
		
		return U



	def Action (self, U1, U2, U3, U4):

		twist = Twist()
		
		twist.linear.z  = U1
		twist.linear.x  = U2
		twist.linear.y  = U3
		twist.angular.z = U4

		self.movePub.publish(twist)

class pd_controller:

	def __init__(self, p_coef, d_coef):
		
		self.kp 				   = p_coef
		self.kd                    = d_coef
		self._previous_error	   = 0.0
		self._is_error_initialized = False

	def set_REW (self, error):

		output   = error * self.kp

		if self._is_error_initialized:

			error_diff           =  error   - self._previous_error
			output               += self.kd * error_diff
			self._previous_error = error

		else:

			self._previous_error       = error
			self._is_error_initialized = True
		
		return output


class pid_controller:

	def __init__(self, p_coef, d_coef, i_coef):
		
		self.kp = p_coef
		self.kd = d_coef
		self.ki = i_coef

		self._last_time      = 0.0
		self.error_integ     = 0.0
		self._previous_error = 0.0

		self._i_max =  5.0  # The integral upper limit.
		self._i_min = -5.0  # The integral lower limit.
		

		self._is_error_initialized_PID = False


	def set_SI (self, error):

		cur_time = time.time()
		output   = self.kp * error

		if self._is_error_initialized_PID:

			dt                   = cur_time - self._last_time
			self._last_time      = cur_time
			self.error_integ     += error * dt


			#error_diff           = (error - self._previous_error) / dt
			error_diff           = error - self._previous_error 
			self._previous_error = error

			derivativa           = self.kd *  error_diff
			integral             = self.ki *  self.error_integ
			
			if  integral  > self._i_max:
				integral  = self._i_max
			elif integral < self._i_min:
				integral  = self._i_min

			output +=  derivativa + integral 

		else:
			
			self._previous_error           = error
			self._last_time                = cur_time
			self._is_error_initialized_PID = True
		
		return output


def shutdown_callback():
	print "Shutting down position controller."


if __name__ == "__main__":

	rospy.init_node('belbic_controller',anonymous=True)
	a = LecturePosicion()
	a.calculos()
	rospy.on_shutdown(shutdown_callback)
	rospy.spin()
	


