


import numpy as np 
import math



def eulerAnglesToRotationMatrix(theta) :

	theta[0]= math.radians(theta[0])
	theta[1]= math.radians(theta[1])
	theta[2]= math.radians(theta[2])
	
	 
	R_x = np.array([[1,         0,                  0                   ],
					[0,         math.cos(theta[0]), -math.sin(theta[0]) ],
					[0,         math.sin(theta[0]), math.cos(theta[0])  ]
					])
		 
		 
					 
	R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
					[0,                     1,      0                   ],
					[-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
					])
				 
	R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
					[math.sin(theta[2]),     math.cos(theta[2]),    0],
					[0,                     0,                      1]
					])
					 
					 
	R = np.dot(R_z, np.dot( R_y, R_x ))
 
	return R

def Homogenius (Rot, x, y , z):

	Th = np. array ([ [Rot[0,0] , Rot[0,1] , Rot [0,2], x],
					  [Rot[1,0] , Rot[1,1] , Rot [1,2], y],
					  [Rot[2,0] , Rot[2,1] , Rot [2,2], z],
					  [		0	,       0,      0,      1]
					]) 
	return Th


def Homogenius_Inversa(Rot, x, y , z):

	R_inversa = Rot.T

	R_p = np.matmul(- R_inversa, np. array ([[x],[y],[z]]))

	

	T_I = np. array ([[R_inversa[0,0] , R_inversa[0,1] , R_inversa [0,2], R_p[0]],
					  [R_inversa[1,0] , R_inversa[1,1] , R_inversa [1,2], R_p[1]],
					  [R_inversa[2,0] , R_inversa[2,1] , R_inversa [2,2], R_p[2]],
					  [		 	0	  ,               0,               0,      1]
					]) 

	return T_I


