# Lab 2: Introduction to ROS2 and Simulation Environment

## Overview
This repository contains the implementation of Lab 2 for the Robotics course. The project demonstrates the integration of the Gazebo simulation environment with ROS2, including creating a custom Python package, launching nodes via a launch file, bridging topics, and visualizing sensor data.

## Features Implemented
* **ROS2 Custom Package:** Created an `ament_python` package named `lab2` containing custom nodes, launch files, and configuration files.
* **Gazebo-ROS2 Bridge:** Utilized `ros_gz_bridge` to establish communication between Gazebo Transport and ROS2 DDS for `/cmd_vel` (commands) and `/lidar` (sensor data) topics.
* **Autonomous Robot Controller:** Implemented a Publisher node (`robot_controller.py`) that sends `Twist` messages at 10 Hz to drive the robot in a continuous sinusoidal (wave-like) trajectory.
* **LiDAR Data Processing:** Implemented a Subscriber node (`lidar_subscriber.py`) that processes `LaserScan` data in real-time, calculates minimum/maximum distances, and outputs warnings when obstacles are detected within 1.0 meter.
* **RViz2 Visualization:** Configured an `.rviz` profile to visualize the robot's environment, plotting real-time LiDAR point clouds (red rays) reflecting off simulated obstacles.
* **Unified Launch System:** Developed `gazebo_ros2.launch.py` to start the Gazebo simulator, the parameter bridge, and RViz2 simultaneously.

## Prerequisites
* Docker
* ROS2 (Jazzy/Humble)
* Gazebo Harmonic
* `ros_gz_bridge` and `ros_gz_sim`

## How to Run

1. **Launch the Docker Container:**
docker run -it --rm --net=host --env DISPLAY=$DISPLAY --volume /tmp/.X11-unix:/tmp/.X11-unix --volume ~/robotics_lpnu:/opt/ws/src --name robotics_intro robotics_intro bash

Build the Workspace:
Inside the container, compile the package and source the environment:

cd /opt/ws
colcon build --packages-select lab2
source install/setup.bash

Start the Simulation, Bridge, and RViz2 (Terminal 1):

ros2 launch lab2 gazebo_ros2.launch.py
(Press the Play button in Gazebo to start the physics engine).

Run the Robot Controller (Terminal 2):
Open a new terminal, enter the container, and start the publisher:

docker exec -it robotics_intro bash
source /opt/ws/install/setup.bash
ros2 run lab2 robot_controller

Run the LiDAR Subscriber (Terminal 3):
Open another terminal, enter the container, and start the subscriber:

docker exec -it robotics_intro bash
source /opt/ws/install/setup.bash
ros2 run lab2 lidar_subscriber
