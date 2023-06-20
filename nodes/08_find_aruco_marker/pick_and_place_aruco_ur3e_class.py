#!/usr/bin/env python3
# pick_and_place_aruco.py
# ------------------------------------
# edited WHS, OJ & ME , 20.6.2023 #
# -------------------------------------
# Pick and Place
# in Python mit der move_group_api
# und Kollsionsverhütung
# FiXer Marker  ID5 => Position mit static_tf_broadcaster senden
# Ort des Arucco Merkers ID9
 # Mit Massband gemessen
 #       tr.transform.translation.x = 0.0
 #       tr.transform.translation.y = -0.65
 #       tr.transform.translation.z = 0.0
# -----------------------------------------
# -----------------------------------------
# usage
#  starte broadcaster: $ rosrun emr22 static_tf_broadcaster_aruco.py 
#  starte UR3e, Bringup, Moveit,...
# ----------------------------------------------------------------
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
# from math import pi
# import numpy as np  # für deg2rad
import tf


class Ur3_aruco:
    # Instantiate the MoveGroupCommander object.
    group_name = "ur3_arm"
    group = moveit_commander.MoveGroupCommander(group_name)
    # Instantiate the robot commander object,
    # which is used to control the whole robot
    robot = moveit_commander.RobotCommander()

    def Ur3_aruco():  # Konstruktor
        # First initialize moveit_ Command and rospy nodes:
        moveit_commander.roscpp_initialize(sys.argv)
       
        # Instantiate the robot commander object,
        # which is used to control the whole robot
        # robot = moveit_commander.RobotCommander()

        # Instantiate the MoveGroupCommander object.
        # group_name = "ur3_arm"
        # group = moveit_commander.MoveGroupCommander(group_name)
        # group_name_gripper = "gripper"
        # group_gripper = moveit_commander.MoveGroupCommander(group_name_gripper)

        # Create a Publisher.
        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                    moveit_msgs.msg.DisplayTrajectory,
                                                    queue_size=20)
        
    def wait_for_state_update(box_name, scene, box_is_known=False,
                            box_is_attached=False, timeout=4):
        start = rospy.get_time()
        seconds = rospy.get_time()
        while (seconds - start < timeout) and not rospy.is_shutdown():
            attached_objects = scene.get_attached_objects([box_name])
            is_attached = len(attached_objects.keys()) > 0
            is_known = box_name in scene.get_known_object_names()
            if (box_is_attached == is_attached) and (box_is_known == is_known):
                return True
            rospy.sleep(0.1)
            seconds = rospy.get_time()
        return False

    def get_aruco_tf_and_go(self):
        lst = tf.TransformListener()
        # if lst.frameExists("world") and lst.frameExists("marker_id9"):
        # Sicherstellen, das die Frames empfangen werden
        while not lst.frameExists("world"):
            print("Kein world frame")
        while not lst.frameExists("marker_id9"):
            print("Kein marker_id9 frame")
        
        (trans, rot) = lst.lookupTransform('world', 'marker_id9', rospy.Time(0))    
                 
        pose_goal = self.group.get_current_pose()  # Instanzierung
        # no worx pose_goal.pose.position = trans
        # => Daten einzeln übergeben
        print("translation is ", trans)
        xt = round(trans[0], 2)
        pose_goal.pose.position.x = xt 
        yt = round(trans[1], 2)
        pose_goal.pose.position.y = yt - 0.2
        zt = round(trans[2], 2)
        pose_goal.pose.position.z = zt - 0.2

        # Pose Aruco Marker id5 per Roboter gemessen
            #         pose: 
            #   position: 
            #     x: 0.278479154823257
            #     y: 0.31181788713775943
            #     z: 0.30379764389423247
            #   orientation: 
            #     x: -0.09277899476643865
            #     y: 0.6757922309004211
            #     z: 0.11867112386862275
            #     w: 0.7215359195109547

        #print("rotation is ", rot)        
        #xr = round(rot[0], 2)
        pose_goal.pose.orientation.x = 0.00
        #yr = round(rot[1], 2)
        pose_goal.pose.orientation.y = 0.70
        #zr = round(rot[2], 2)
        pose_goal.pose.orientation.z = 0.00
        #wr = round(rot[3], 2)
        pose_goal.pose.orientation.w = 0.70
      
        self.group.set_pose_target(pose_goal)
        plan = self.group.plan()
        sucess = self.group.go(wait=True)
        print("suc?", sucess)
        self.group.stop()
        self.group.clear_pose_targets()
         
    def goto_goal1(self):
        # Anfahren der einer gültigen Positiom
        print("===  Go to Goal 1 ==")
        pose_goal = self.group.get_current_pose()

        pose_goal.pose.position.x = 0.04
        pose_goal.pose.position.y = 0.33
        pose_goal.pose.position.z = 0.5
        pose_goal.pose.orientation.x = 0
        pose_goal.pose.orientation.y = 0.70
        pose_goal.pose.orientation.z = 0
        pose_goal.pose.orientation.w = 0.71

        # Diese Pose kann nicht angefahren werden
        # pose_goal.pose.position.x = -5.04
        # pose_goal.pose.position.y = 0.19
        # pose_goal.pose.position.z = 0.69
        # pose_goal.pose.orientation.x = 2.73
        # pose_goal.pose.orientation.y = 2.73
        # pose_goal.pose.orientation.z = 0.70
        # pose_goal.pose.orientation.w = 0.70

        print(" going to Goal 1", pose_goal.pose.position) 

        self.group.set_pose_target(pose_goal)
        plan = self.group.plan()
        sucess = self.group.go(wait=True)
        print("suc?", sucess)
        self.group.stop()
        self.group.clear_pose_targets()
  
    def goto_stored_position_home(self, pos_str="home"):
        # ---- 1. Move to home position (Vorgabe der Gelenkwinkel) ----
        print(self.group.get_named_target_values(pos_str))
        joint_goal = self.group.get_named_target_values(pos_str)
        self.group.go(joint_goal, wait=True)
        # print("Reached Joint Goal Home", joint_goal)
        print("Current Pose", self.group.get_current_pose())
#  ----- Ur3_aruco() -----------------------------------------


def main():
    rospy.init_node('move_group_python_interface_tutorial',
                    anonymous=True)
    rate = rospy.Rate(10.0)
    ua = Ur3_aruco()
    ua.goto_stored_position_home("home")
    ua.goto_goal1()
    ua.get_aruco_tf_and_go()
    input("Back to Home ? => Enter")
    ua.goto_stored_position_home("home")


if __name__ == "__main__":
    main()