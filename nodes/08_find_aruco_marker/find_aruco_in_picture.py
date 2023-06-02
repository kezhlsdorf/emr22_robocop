#!/usr/bin/env python3
# =================================================
# edited WHS, OJ , 2.6.2023 #
#
# Einen ArUco Marker in einem Bild detektieren
# Vgl. https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
#
# usage: not done yet
# $1
#

# Python libs
# import numpy as np

# OpenCV
import cv2
# Aruco Error
# AttributeError: module 'cv2' has no attribute 'aruco'
# Lösung:
# pip3 uninstall opencv-python
# pip3 uninstall opencv-contrib-python
# pip3 install opencv-python
# pip3 install opencv-contrib-python

# Ros libraries
# import roslib
# import rospy

# Ros Messages
# from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

image = cv2.imread('/home/oj/ws_moveit/src/emr22/nodes/08_find_aruco_marker/image.png')
cv2.imshow("Aruco Bild", image)
print(' Hit Any Key after klicking with mouse in Image Window')
cv2.waitKey(0)

# holt die passende Dictionary zu den Markern 
# (Bits NxN, Anzhal der verschienden Marker die dann möglich sind ) 
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image,
                                                   arucoDict,
                                                   parameters=arucoParams)
print(ids, corners)
