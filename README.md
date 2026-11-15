# ROS-2-Turtlesim-Landscape-Artist

A Python-based ROS 2 project that uses **two turtles** in the `turtlesim` simulator to draw a complete landscape. 

The drawing features a sun with rays, fluffy clouds, a red house with a door and window, and four trees framing the scene. To ensure perfectly straight walls and clean shapes, this project uses a combination of `TeleportAbsolute` (for straight lines) and `Twist` (for curved sun/cloud arcs).

## ✨ Features
- **Multi-Turtle Support:** Dynamically spawns a second turtle to divide the drawing workload.
- **Precision Drawing:** Uses `TeleportAbsolute` to draw 100% straight lines, eliminating the PID-drift and slanted walls common with movement-based drawing.
- **Dynamic Pen Control:** Changes colors and lifts/lowers the pen using the `/set_pen` service.
- **Clean Layout:** Carefully calculated coordinates prevent shapes from overlapping.

## 📋 Prerequisites
- ROS 2 (Foxy, Humble, or Iron)
- `turtlesim` package installed (`sudo apt install ros-<distro>-turtlesim`)
- Python 3

## 🚀 Installation

1. **Create a ROS 2 Workspace** (if you don't have one):
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
Create the Package:

bash
ros2 pkg create --build-type ament_python turtle_drawer --dependencies rclpy geometry_msgs turtlesim
Add the Code:
Navigate to ~/ros2_ws/src/turtle_drawer/turtle_drawer/, create a file named draw_picture.py, and paste the Python script.

Configure setup.py:
Open ~/ros2_ws/src/turtle_drawer/setup.py and add the entry point:

python
entry_points={
    'console_scripts': [
        'draw_picture = turtle_drawer.draw_picture:main',
    ],
},
Build the Workspace:

bash
cd ~/ros2_ws
colcon build --packages-select turtle_drawer
source install/setup.bash
🎮 How to Run
You will need two separate terminals. Make sure to source the workspace in both.

Terminal 1: Start the Simulator

bash
source ~/ros2_ws/install/setup.bash
ros2 run turtlesim turtlesim_node
Terminal 2: Run the Drawing Script

bash
source ~/ros2_ws/install/setup.bash
ros2 run turtle_drawer draw_picture
🖼️ Preview
(Add a screenshot of your final landscape here!)

<!-- ![Turtlesim Landscape](link_to_your_image.png) -->
🧠 How It Works
Turtle 1 is tasked with drawing the house (walls, roof, door, and window).

Turtle 2 is spawned to draw the background (sun, clouds) and the foreground (trees).

The line() function lifts the pen, teleports to the start of the line, puts the pen down, and teleports to the end. This guarantees perfectly straight lines regardless of the simulator's physics update rate.

The draw_circle() function calculates the exact linear and angular velocities required to draw a perfect circle without stopping.

📜 License
This project is open-source and available under the MIT License.

text

### 💡 Tips for your GitHub Repo:
1. **Add a Picture:** Since you have a working screenshot of the sun, clouds, house, and trees, upload that image to your GitHub repository and add it to the `Preview` section so people can see what the code draws!
2. **The Code File:** Make sure your `draw_picture.py` (Version 9) is uploaded to the repository, and you edit the `setup.py` file exactly as shown in the README.
