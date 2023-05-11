#!/usr/bin/env python3
# =================================================
# edited WHS, OJ , 9.5.2023 #
#
# Ein Bild der Intel Realsense Camera vom ROS-node holen
#
# usage: starting driver for camera
# $1 roslaunch realsense2_camera rs_camera.launch
# $2 rqt 
#    Plugin image viewer starten, Topic /camera/color/image_raw
#    anzeigen lassen
#
#       $ rostopic info /camera/color/image_raw
#               Type: sensor_msgs/Image
#
#        Publishers: 
#        * /camera/realsense2_camera_manager (http://192.168.0.100:35785/)
#
# $3 rosrun emr22 openCV_01_get_pic_from_realsense_via_ros.py 
# -------------------------------------------------------
# Idea from 
# https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/


# Python libs
import sys, time
import numpy as np

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

VERBOSE = False  # for debuging

class image_receiver:

    def __init__(self):  
        # subscribed Topic
        self.subscriber = rospy.Subscriber("/camera/color/image_raw/compressed",
            CompressedImage, self.callback,  queue_size = 10)
        if VERBOSE :
            print ("subscribed to /camera/color/image_raw/compressed")

    def hsv2redmask(self):
        # Set range for red color and define mask
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        self.img_red_mask = cv2.inRange(self.img_hsv, red_lower, red_upper)
        cv2.imshow('Red Mask Img', self.img_red_mask)
        cv2.waitKey(2)

    def morph(self):
        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        kernel = np.ones((5, 5), "uint8")
        self.img_red_mask = cv2.dilate(self.img_red_mask, kernel)
        cv2.bitwise_and(self.img, self.img, mask = self.img_red_mask)


    def find_contours(self):
        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(self.img_red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
               
                self.img2 = cv2.rectangle(self.img2, (x, y), 
                                        (x + w, y + h), 
                                        (0, 0, 255), 2)
                
                cv2.putText(self.img2, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))    
        
        cv2.imshow("Red Color Detection in Real-TIme", self.img2)

    def convert2hsv(self):
        # Convert the imageFrame in BGR(RGB color space) to 
        # HSV(hue-saturation-value) color space
        self.img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        cv2.imshow('HSV-img', self.img_hsv)
        cv2.waitKey(2)
   
    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected'''
        if VERBOSE :
            print('received image of type: "%s"' % ros_data.format)

        #### direct conversion to CV2 ####
        np_arr = np.frombuffer(ros_data.data, np.uint8)
        self.img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.img2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        

def main(args):
    ir = image_receiver() # Instanzierung der Klasse
    rospy.init_node('image_receiver', anonymous=True)

    while (not rospy.is_shutdown()):
        try:
            # get img from callback
            cv2.imshow('cv_img', ir.img)
            cv2.waitKey(2)
            # convert 2 HSV
            ir.convert2hsv()
            # Maskiere Rot
            ir.hsv2redmask()
            # Erosion und Dilatation
            ir.morph()
            # Finde contouren
            ir.find_contours()
            cv2.waitKey(2)

        except KeyboardInterrupt:
            print("Shutting down ROS Image feature detector module")
            cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main(sys.argv)