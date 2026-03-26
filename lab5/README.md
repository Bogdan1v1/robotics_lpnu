# Lab 5: Obstacle Avoidance

**Author:** Bohdan Vasyliv  
**Course:** Introduction to Robotics

## Overview
This repository contains the implementation of Lab 5. The objective is to implement an obstacle avoidance system for a TurtleBot3 robot in a simulated Gazebo environment. The robot uses LiDAR (`/scan`) and odometry (`/odom`) to navigate from its starting position to a specific goal `(3.0, 3.0)` while dynamically avoiding static obstacles (a red box and a blue cylinder) placed in its path.

The navigation logic is based on the **Artificial Potential Fields** algorithm.

## How to Run (Launch Instructions)

All tasks are designed to be executed within a ROS 2 Docker container. The launch file automatically starts Gazebo, RViz2, and the obstacle avoidance node.

### 1. Build the Workspace
Before running the simulation, compile the necessary packages and source the environment:

# Inside the Docker container:
cd /opt/ws
colcon build --packages-select lab3 lab5
source install/setup.bash

2. Launch the Simulation
Open a terminal, source the environment, and launch the bringup file. You only need one terminal for this lab:

source /opt/ws/install/setup.bash
ros2 launch lab5 obstacle_avoidance_bringup.launch.py
(Note: Remember to press the Play (▶) button in Gazebo to start the physics engine).

3. Observe the Results
The robot will automatically calculate the attractive force toward the goal and the repulsive forces from the obstacles.

It will navigate around the red box and blue cylinder.

Check the terminal output to see the remaining distance to the goal.

Once the distance is less than 0.2m, the robot will stop and print 🎯 Ціль досягнута!.

Algorithm & Parameters Tuning
The Artificial Potential Fields algorithm was implemented with a custom 10 Hz control loop to avoid sensor delay issues.

Tuned Parameters:

k_att (Attractive gain): 1.2

k_rep (Repulsive gain): 0.01

safe_dist (Obstacle reaction distance): 0.5 m

max_v (Max linear velocity): 0.2 m/s

Issues Faced: The Local Minimum Problem
During testing, the robot initially got stuck oscillating in place when the attractive force toward the goal exactly canceled out the repulsive force from the obstacles (Local Minimum). To overcome this, the parameters were heavily tuned: the repulsive gain (k_rep) was significantly decreased, and the reaction distance (safe_dist) was reduced to 0.5 m. This made the robot "braver," allowing it to approach obstacles closer and slip past them without getting trapped. A filter was also added to ignore LiDAR readings below 0.2 meters so the robot wouldn't react to its own chassis.
