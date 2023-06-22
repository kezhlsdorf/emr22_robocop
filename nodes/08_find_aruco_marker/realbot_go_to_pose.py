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
# usage
# ----------------------------------------------------------------
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
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

cur_pose = group.get_current_pose()
print("\n Current Pose is: ", cur_pose)

lst = tf.TransformListener()
# pose_goal = group.get_current_pose()
pose_goal = geometry_msgs.msg.Pose()

rate = rospy.Rate(10.0)

# pose_goal.header.seq = 1
pose_goal.pose.position.x = 0.06
pose_goal.pose.position.y = 0.33
pose_goal.pose.position.z = 0.5

pose_goal.pose.orientation.x = -0.003
pose_goal.pose.orientation.y = 0.704
pose_goal.pose.orientation.z = -0.003
pose_goal.pose.orientation.w = 0.710

print("new Goal", pose_goal)
# print("\n\nnew position \n", pose_goal.pose.position)
# print(" new orientation \n", pose_goal.pose.orientation)
input("\n  Should I go to this Pose?  => Enter \a \n")
group.set_pose_target(pose_goal)
plan = group.plan()
sucess = group.go(wait=True)
print("Reached new Pose?", sucess)
group.stop()

cur_pose2 = group.get_current_pose()
print("\n Now I reached this Pose: ", cur_pose2)

group.clear_pose_targets()
