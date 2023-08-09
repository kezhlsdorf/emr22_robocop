# Installing MoveIt Task Constructor on ROS Noetic for use with MoveIt!
# auf einem Rechner mit Ubuntu 20.04 Focal Fossa  
# geaendert am 09.08.2023
#------------------------------------------------------------------
#  usage demo example for RVIZ:
# $ roslaunch moveit_task_constructor_demo demo.launch
#------------------------------------------------------------------
#  usage demo example for a task:
# $ rosrun moveit_task_constructor_demo cartesian
# $ rosrun moveit_task_constructor_demo modular
# $ roslaunch moveit_task_constructor_demo pickplace.launch
#------------------------------------------------------------------
#!/bin/bash

echo -e "\033[34m ----- RoboCop -- MoveIt Task Constructor installieren ----- \033[0m"

cd ~/ws_moveit/src

git clone https://github.com/ros-planning/moveit_task_constructor.git

sudo rosdep install --from-paths . --ignore-src --rosdistro $ROS_DISTRO

cd ~/ws_moveit

echo -e "\033[34m ----- catkin build ----- \033[0m"

catkin build
