# 🐢 ROS 2 Turtlesim Landscape Artist

A Python-based ROS 2 project that uses **two turtles** in the `turtlesim` simulator to draw a complete landscape. 

The drawing features a sun with rays, fluffy clouds, a red house with a door and window, and four trees framing the scene. To ensure perfectly straight walls and clean shapes without PID-drift, this project uses a combination of `TeleportAbsolute` (for straight lines) and `Twist` (for curved sun/cloud arcs).

## 🎥 Demo

[![Watch Demo on LinkedIn](https://img.shields.io/badge/▶_Watch_Demo-LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://lnkd.in/p/dTgTM7vj)

## ✨ Features
- **Multi-Turtle Support:** Dynamically spawns a second turtle to divide the drawing workload.
- **Precision Drawing:** Uses `TeleportAbsolute` to draw 100% straight lines, eliminating slanted walls.
- **Dynamic Pen Control:** Changes colors and lifts/lowers the pen using the `/set_pen` service.
- **Clean Layout:** Carefully calculated coordinates prevent shapes from overlapping.

## 📋 Prerequisites
- ROS 2 (Foxy, Humble, Iron, or later)
- `turtlesim` package installed
- Python 3

## 🚀 Installation

Follow these steps to set up the workspace, build the package, and run the simulator.

### 1. Create the ROS 2 Workspace and Package
Open a terminal and run the following commands to create your workspace and generate the package:

```bash
# Create the workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create the python package with required dependencies
ros2 pkg create --build-type ament_python turtle_drawer --dependencies rclpy geometry_msgs turtlesim

2. Add the Code
Navigate to the inner package folder: ~/ros2_ws/src/turtle_drawer/turtle_drawer/

Create a file named draw_picture.py and paste the provided Python drawing script into it.

Open ~/ros2_ws/src/turtle_drawer/setup.py and add the executable entry point so ROS 2 can find your script:
entry_points={
    'console_scripts': [
        'draw_picture = turtle_drawer.draw_picture:main',
    ],
},


3. Build the Workspace
Once your files are saved, build the package and source the setup file:

cd ~/ros2_ws
colcon build --packages-select turtle_drawer
source install/setup.bash

🎮 How to Run
You will need two separate terminals open. Make sure to source the workspace in both terminals before running the commands.

Terminal 1: Start the Simulator

bash

source ~/ros2_ws/install/setup.bash
ros2 run turtlesim turtlesim_node

Terminal 2: Run the Drawing Script

bash
source ~/ros2_ws/install/setup.bash
ros2 run turtle_drawer draw_picture


🧠 How It Works
Turtle 1 draws the house (walls, roof, door, and window).

Turtle 2 is spawned to draw the background (sun, clouds) and the foreground (trees).

The line() function lifts the pen, teleports to the start of the line, puts the pen down, and teleports to the end. This guarantees perfectly straight lines regardless of the simulator's physics update rate.

The draw_circle() function calculates the exact linear (v) and angular (w) velocities required to draw a perfect circle without stopping.

📜 License
This project is open-source
