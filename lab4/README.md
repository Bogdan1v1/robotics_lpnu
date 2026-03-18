# Lab 4: Dead Reckoning

**Author:** Bohdan  
**Course:** Introduction to Robotics

## Overview
This repository contains the implementation of Lab 4. The main objective of this lab is to implement **dead reckoning** — a method of estimating the robot's pose by mathematically integrating its velocity commands (`/cmd_vel`) over time. This estimated trajectory is then visualized and compared against the Gazebo ground truth odometry (`/odom`) to observe and understand positional drift.

---

## How to Run (Launch Instructions)

All tasks are designed to be executed within the provided ROS2 Docker container. 

### 1. Build the Workspace
Before running the simulation, you must compile both the `lab3` (for the movement scripts) and `lab4` packages, then source the environment:

# Inside the Docker container:
cd /opt/ws
colcon build --packages-select lab3 lab4
source install/setup.bash
2. Launch the Simulation & RViz2 (Terminal 1)Open your first terminal, source the environment, 
and launch the TurtleBot3 simulation along with the pre-configured RViz2 environment: source /opt/ws/install/setup.bash
ros2 launch lab4 dead_reckoning_bringup.launch.py
(Note: Remember to press the Play (▶) button in Gazebo to start the physics engine).3. 
Run the Trajectory Node (Terminal 2)
Open a second terminal, enter the Docker container, source the environment, and execute the circle trajectory node from Lab 3 to set the robot in motion:
# Inside the Docker container:
source /opt/ws/install/setup.bash
ros2 run lab3 circle_path
4. Observe the ResultsOnce the robot starts moving, switch to the RViz2 window.
You will observe two distinct trajectory lines being drawn:Green Line: The ground truth path from Gazebo's odometry (/path).Red/Orange Line: 
The estimated path calculated by the custom dead reckoning script (/path_dr).
Look at Terminal 1 to see the real-time calculated drift error in meters.Tasks CompletedDead Reckoning Implementation: 
Developed the dead_reckoning.py node to calculate the robot's coordinates ($X$, $Y$, and $\theta$) over time using velocity commands and kinematic
equations.Simulation & Visualization: Successfully launched the TurtleBot3 in the room environment and used the circle_path
node to drive the robot in a continuous circle.Comparison: 
Visualized both the ground truth path and the dead reckoning path in RViz2 to observe the divergence (drift) between pure mathematical 
integration and the simulated physical reality.
Deliverables & Theoretical QuestionsWhy does dead reckoning drift?
Dead reckoning relies entirely on the open-loop mathematical integration of velocity commands over time 
(e.g., $X_{new} = X_{old} + v \cdot \cos(\theta) \cdot dt$). 
It assumes perfect, instantaneous execution of commands by the robot's hardware.However, in physical reality (and precise physics simulators like Gazebo), 
wheels slip, friction varies, and timing updates ($dt$) are never perfectly exact. Because each new position calculation builds upon the previous one, 
these microscopic errors accumulate continuously (unbounded error growth). 
Without external sensor feedback to correct it, the dead reckoning estimate will inevitably drift away from the actual ground truth position.
