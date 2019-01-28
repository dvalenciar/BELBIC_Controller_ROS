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

1. Download and install the package in your personal workspace (e.g. ~/drone_simulation_ws)
```
$ cd ~/drone_simulation_ws/src
$ git clone https://github.com/dvalenciar/BELBIC_Controller_ROS.git
$ cd ..
$ catkin_make

```
