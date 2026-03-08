# Lab 1: Building Your Robot in Gazebo

## Overview
This repository contains the implementation of Lab 1 for the Robotics course. The project demonstrates the creation of a 4-wheeled mobile robot in the Gazebo simulation environment using the SDF (Simulation Description Format).

## Features Implemented
* **4-Wheel Drive Robot:** A custom robot model featuring a main chassis and four independently simulated wheels connected via revolute joints. Complete with proper physical and inertial properties.
* **Differential Drive Controller:** Integrated `gz-sim-diff-drive-system` plugin configured to drive all four wheels simultaneously, responding to `/cmd_vel` Twist messages.
* **LiDAR Sensor:** A GPU-based LiDAR sensor is mounted on the robot to scan the environment. It publishes distance data to the `/lidar` topic with visualization enabled.
* **Test Environment:** A custom world containing three distinct obstacles (a box, a cylinder, and a sphere) to test the LiDAR's scanning capabilities and the robot's maneuverability.
* **Keyboard Teleoperation:** The robot can be directly controlled using the Gazebo Key Publisher plugin via keyboard arrows mapping directly to the `/cmd_vel` topic.

## Prerequisites
* Docker
* Gazebo Harmonic / ROS 2 (Jazzy/Humble)

## How to Run

1. **Launch the Docker Container:**
Ensure your X-server allows local connections, then run:
docker run -it --rm --net=host --env DISPLAY=$DISPLAY --volume /tmp/.X11-unix:/tmp/.X11-unix --volume ~/robotics_lpnu:/opt/ws/src --name robotics_intro robotics_intro bash
2. **Start the Simulation:**
Inside the container, run the world file:
gz sim /opt/ws/src/lab1/worlds/robot.sdf
3. **Control the Robot (Terminal):**
In a separate terminal connected to the container, source your ROS environment and publish a movement command:
docker exec -it robotics_intro bash
source /opt/ros/jazzy/setup.bash
4. **Control the Robot (Keyboard):**
You can use this to move robot:

gz topic -t "/cmd_vel" -m gz.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.0}"

Add the Key Publisher plugin from the Gazebo GUI.

Use the Up, Down, Left, and Right arrow keys to drive the robot. Use Space to stop.

Structure
worlds/robot.sdf: The main simulation file containing the world, physics plugins, test obstacles, and the complete robot model.
