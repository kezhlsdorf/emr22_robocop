#!/usr/bin/env python3
# pick_and_place_aruco.py
# ------------------------------------
# edited WHS, OJ , 13.6.2023 #
# -------------------------------------
# Pick and Place
# in Python mit der move_group_api
# und Kollsionsverhütung
# 
# MoveIt: Plane und verfahre an eine vorgegebene Pose
# -----------------------------------------
# -----------------------------------------
# usage: 
# rosrun emr22 static_tf_broadcaster_aruco.py 
# rosrun <this file>
# Tested 19.6.23, 
# by ME and OJ => WORKX with UR3e an Aruco Detection 
# and realsense camera running
# ----------------------------------------------------------------
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
# import geometry_msgs.msg
# from math import pi
# import numpy as np  # für deg2rad
import tf


# First initialize moveit_ Command and rospy nodes:
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)
# Instantiate the robot commander object,
# which is used to control the whole robot
robot = moveit_commander.RobotCommander()

# Instantiate the MoveGroupCommander object.
group_name = "ur3_arm"
group = moveit_commander.MoveGroupCommander(group_name)
# group_name_gripper = "gripper"
# group_gripper = moveit_commander.MoveGroupCommander(group_name_gripper)

# Create a Publisher.
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)

# ---- 1. Move to home position (Vorgabe der Gelenkwinkel) ----
print(group.get_named_target_values("home"))
joint_goal = group.get_named_target_values("home")
group.go(joint_goal, wait=True)
# print("Reached Joint Goal Home", joint_goal)
print("Current Pose", group.get_current_pose())


# --- 2. Place the TCP above the blue box
print("===  Go to Pose  ==")
lst = tf.TransformListener()
pose_goal = group.get_current_pose()

rate = rospy.Rate(10.0)

pose_goal.pose.position.x = 0.04
pose_goal.pose.position.y = 0.33
pose_goal.pose.position.z = 0.5

# !!!!XXXXXXXX Maximal 2 Nachkommstellen !%$§$%&%!/("Z()")
pose_goal.pose.orientation.x = 0
pose_goal.pose.orientation.y = 0.70
pose_goal.pose.orientation.z = 0
pose_goal.pose.orientation.w = 0.71

# ===> SO NICHT !!!!
# pose_goal.pose.orientation.x = -0.0030587479732231237
# pose_goal.pose.orientation.y = 0.7040579296634328
# pose_goal.pose.orientation.z = -0.0030948106841058682
# pose_goal.pose.orientation.w = 0.7101292121055903

print(" going to position", pose_goal.pose.position)

group.set_pose_target(pose_goal)
plan = group.plan()
sucess = group.go(wait=True)
print("suc?", sucess)
group.stop()
group.clear_pose_targets()
