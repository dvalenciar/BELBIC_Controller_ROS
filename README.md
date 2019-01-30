# BELBIC Controller AR. DRONE
This repository contains the simulation source-code for implementing a BELBIC (Brain Emotional Learning-Based Intelligent Controller) controller for autonomus navigation of AR.Drone. The control system presented is inspired by the working principle of the human brain, where a mathematical model of the limbic system (Thalamus, Sensory Cortex, Orbitofrontal Cortex, and Amygdala) is implemented; The computational modelis fundamentally an action generation mechanism based on sensory inputs (SI) and emotional signals (REW). This model, called BELBIC, has as main tasks the stabilization of the quadrotors as well as the autonomous tracking of trajectories. BELBIC and other biologically-inspired approaches have been extensively utilized for solving different types of problems, essentially because Emotional Learning is a powerful methodology, with low
computational complexity, fast training and simple to implement . An important characteristic of BELBIC is its single-layer architecture i.e. its computational complexity is in the order of O(n), which result in a better performance for real-time implementation 

## Pre-requisites
* Operation System
  * Ubuntu 16.04
* [ROS](http://wiki.ros.org/kinetic/Installation/Ubuntu) (Kinetic)
* [GAZEBO 7.0](http://gazebosim.org/)
  

## Getting started - 
Make sure ROS and GAZEBO are correctly installed. 

Also, please install [ardrone_autonmy](https://github.com/AutonomyLab/ardrone_autonomy) and [tum_simuator packages](https://github.com/eborghi10/AR.Drone-ROS). You can find the instructions here:
[AR Drone Gazebo Installation](https://github.com/dvalenciar/AR_Drone_ROS_GUI#getting-started)


## Installation 

Download and install the package in your personal workspace (e.g. ~/drone_simulation_ws)
  
  ```
  cd ~/drone_simulation_ws/src
  git clone https://github.com/dvalenciar/BELBIC_Controller_ROS.git
  cd ..
  catkin_make
  ```

## How to Run ##

1. **Source your workspace environment**

  ```
  cd ~/drone_simulation_ws/
  source devel/setup.bash
  ```
2. **Run a simulation by executing a launch file:**

  ```
  roslaunch Belbic empty_world.launch
  ```
3. **Take off the AR.Drone**

  ```
  rostopic pub -1 /ardrone/takeoff std_msgs/Empty
  ```

4. **Run the BELBIC controller node**

  ```
  rosrun Belbic Belbic_controller.py
  ```
The Drone will fly autonomously to the position X = 0, Y = 0 with an altitude Z = 2, and will maintain its position

![](https://github.com/dvalenciar/BELBIC_Controller_ROS/blob/master/Belbic_1.gif)


5. **Fly to a specific point**

You only have to publish the topic "*/position_referencia*"  with the point where you want to go. For example point x:7,y:7,z:3 The drone will fly autonomously to that point.

  ```
  rostopic pub /position_referencia geometry_msgs/Twist  '{linear:  {x: 7.0, y: 7.0, z: 3.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'
 ```
 
 ![](https://github.com/dvalenciar/BELBIC_Controller_ROS/blob/master/point.gif)

## Trajectory Tracking ##

To make it even easier, we programmed 3 nodes with different trajectories (circular, lemniscate, waypoints). The drone will fly autonomously through these trajectories.

The only thing you have to do is execute the following command in a terminal. (remember Source your workspace on the new terminal)


**Circular Trajectory (R = 5)**
  ```
  rosrun Belbic Trajectory_Circular.py 
```  
![](https://github.com/dvalenciar/BELBIC_Controller_ROS/blob/master/pic44.gif)


**Lemniscate  Trajectory (also known as 8 shape)**
 ```
 rosrun Belbic Trajectory_Lemniscata.py
 ```
 
 **Waypoints Trajectory**
 
Taking into account simplicity and efficiency, in this work, we created a ROS node that generated trajectories using a cubic polynomial function. The cubic polynomial function allows the generation of smooth trajectories. This “smoothness” means that velocity or acceleration has no discontinuities, therefore the stress on the motors is reduced considerably
 ```
 rosrun Belbic GenerateTrajectory.py 
 ```
 
 The controls points where the quadrotor shoul pass are: Point 1 (x=5, y=5, z=1), Point 2 (x=5, y= -5, z=3), Point 3 (x= -5,
y=-5, z=2), Point 4 (x= -5, y= 5, z=3), Point 5 (x=0, y=0, z=1)

You can modify or add  waypoints, you just have to modify the file **waypoints.txt** located in ~/Belbic/trajectories/
where the first column corresponds to X, the second column corresponds to Y, The third column corresponds to Z and the last column correspond to time.

 **rqt_multiplot**
 
You can also observe in real time the position of the drone and the reference send to the controller. You just have to run the following command
 
 ```
rosrun  rosrun rqt_multiplot rqt_multiplot
 ```
Open a configuration (right upper corner) and navigate to ~/Belbic/rqt/rqt_signal_plot.xml

![](https://github.com/dvalenciar/BELBIC_Controller_ROS/blob/master/Circular_Figure5.1.png)



