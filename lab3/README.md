# Lab 3: Moving Mobile Robots in Simulation

**Author:** Bohdan  
**Course:** Introduction to Robotics

## Overview
This repository contains the implementation of Lab 3. The main goals were to understand differential drive kinematics, use odometry feedback for path following, and visualize trajectories using RViz2. The tasks were tested on both a custom 4-wheel robot and the TurtleBot3 in a simulated room environment.

---

## How to Run (Launch Instructions)

All tasks are designed to be executed within the provided ROS2 Docker container. 

### 1. Build the Workspace
Before running any nodes, compile the `lab3` package and source the environment:
# Inside the Docker container:
sudo apt update && sudo apt install -y ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-simulations
cd /opt/ws
colcon build --packages-select lab3
source install/setup.bash
2. Launch the Simulation Environment (Terminal 1)
You can choose between two simulated robots. Run ONE of the following commands in your first terminal:

Option A: Custom 4-Wheel Robot

ros2 launch lab3 bringup.launch.py
Option B: TurtleBot3 in a Room

ros2 launch lab3 turtlebot3_room_bringup.launch.py
(Note: Remember to press the Play (▶) button in Gazebo to start the physics engine. RViz2 will open automatically).

3. Run the Path Controllers (Terminal 2)
Open a second terminal, enter the Docker container, source the environment (source /opt/ws/install/setup.bash), and run ONE of the desired path nodes:

To run the Figure-8 Path (Task 2):

ros2 run lab3 figure_8_path
To run the Circle Path:

ros2 run lab3 circle_path
To run the Square Path (with optimized parameters):

ros2 run lab3 square_path --ros-args -p side_length:=2.0 -p linear_speed:=0.2 -p angular_speed:=0.4
### Tasks Completed
1. Task 1 & 2: Path Implementations
Successfully ran the provided square_path and circle_path nodes.

Implemented the figure_8_path.py node, which executes a figure-8 trajectory by performing two consecutive timed circles (a left turn with w > 0 followed by a right turn with w < 0).

Tested the code on both the custom robot and the TurtleBot3 model.

2. Task 3: RViz2 Trajectory Visualization
The path of the robot was successfully tracked and visualized in RViz2 using the /path topic and the odom_path_publisher node. The Fixed Frame was correctly set to odom to display the green trajectory line.
