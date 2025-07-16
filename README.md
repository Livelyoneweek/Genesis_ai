# Robot Arm Motion Planning and Control Project

reference https://github.com/Genesis-Embodied-AI/Genesis/blob/main/README_KR.md  

This project is a collection of Python scripts for studying and implementing robot arm motion planning and control. Based on the file names, it appears to focus on the Franka Emika robot arm and utilizes the OMPL library for motion planning.

## Project Overview

The primary goal of this project is to explore various aspects of robotics, including:

-   **Kinematics and Dynamics:** Controlling the robot arm's joints and end-effector.
-   **Motion Planning:** Generating collision-free paths for the robot arm using OMPL.
-   **Robot Control:** Implementing different control schemes for precise movements.
-   **Web Interface:** Potentially providing a web-based interface for robot interaction via Flask.

## File Descriptions

-   `frank_arm.py` / `frank_arm2.py`: Main scripts for controlling the Franka robot arm.
-   `motion_planing.py`: Contains the implementation of motion planning algorithms, likely using the OMPL library.
-   `robot_control_1.py` / `robot_control_2.py`: Scripts demonstrating different robot control strategies.
-   `parallel_robot_arm_1.py`: An experiment or implementation related to parallel robot arms.
-   `flask_app.py`: A Flask web application, possibly for visualizing or controlling the robot arm remotely.
-   `ompl-1.6.0-cp311-cp311-macosx_13_0_arm64.whl`: The OMPL wheel package for installation on macOS ARM64.
-   `mygenesis/`: A Python virtual environment containing the necessary dependencies for this project.

## Getting Started

### Prerequisites

-   Python 3.11
-   A virtual environment tool (like `venv`)

### Setup

1.  **Activate the virtual environment:**
    ```bash
    source mygenesis/bin/activate
    ```

2.  **Install dependencies:**
    The required packages are located within the `mygenesis` virtual environment. If you need to set up the environment from scratch, you would typically install packages from a `requirements.txt` file. Make sure to install the provided OMPL wheel file:
    ```bash
    pip install ompl-1.6.0-cp311-cp311-macosx_13_0_arm64.whl
    ```

### Running the Scripts

Once the environment is activated, you can run the individual Python scripts.

**Example:**
```bash
# Activate the virtual environment
source mygenesis/bin/activate

# Run one of the main control scripts
python frank_arm.py
```

To start the web interface (if configured):
```bash
# Activate the virtual environment
source mygenesis/bin/activate

# Run the Flask application
flask --app flask_app run
```
