# BELBIC Controller AR. DRONE
This repository contains the simulation source-code for implementing a BELBIC (Brain Emotional Learning-Based Intelligent Controller) controller for autonomus navigation of AR.Drone 

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

## How to Run

1. **Source your workspace environment**

  ```
  cd ~/drone_simulation_ws/
  source devel/setup.bash
  ```
2. Run a simulation by executing a launch file:

  ```
  roslaunch Belbic empty_world.launch
  ```
3. Take off the AR.Drone

  ```
  rostopic pub -1 /ardrone/takeoff std_msgs/Empty
  ```

4. Run the BELBIC controller node

  ```
  rosrun Belbic Belbic_controller.py
  ```
The Drone will fly autonomously to the position X = 0, Y = 0 with an altitude Z = 2, and will maintain its position

![](https://github.com/dvalenciar/BELBIC_Controller_ROS/blob/master/Belbic_1.gif)


5. Fly to a specific point

You only have to publish the topic "/position_referencia" with the point where you want to go. For example point x:7,y:7,z:3 The drone will fly autonomously to that point.

  ```
  rostopic pub /position_referencia geometry_msgs/Twist  '{linear:  {x: 7.0, y: 7.0, z: 3.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'
 ```
 
 ![](https://github.com/dvalenciar/BELBIC_Controller_ROS/blob/master/point.gif)
