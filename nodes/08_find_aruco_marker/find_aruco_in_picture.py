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
import numpy as np

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

# Getting Distance
# https://stackoverflow.com/questions/68019526/how-can-i-get-the-distance-from-my-camera-to-an-opencv-aruco-marker
markerSizeInCM = 0.2  # m
imsize = [640, 480]  # Bildeigenschaften
print(imsize)
cameraMatrixInit = np.array([[2000.,    0., imsize[0]/2.],
                             [   0., 2000., imsize[1]/2.],
                             [   0.,    0.,           1.]])
distortion_coefficients = 0
rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInCM,
                                                    cameraMatrixInit,
                                                    distortion_coefficients)
print("rvec", rvec)  # Output vector of rotation vectors (see Rodrigues ) estimated for each board view
print("tvec", tvec)  # Output vector of translation vectors estimated for each pattern view.
