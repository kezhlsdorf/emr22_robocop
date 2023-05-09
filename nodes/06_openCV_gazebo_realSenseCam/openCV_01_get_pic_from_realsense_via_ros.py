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
# http://wiki.ros.org/rospy_tutorials/Tutorials/WritingImagePublisherSubscriber
# OpenCV feature detectors with ros CompressedImage Topics in python.
# This example subscribes to a ros topic containing sensor_msgs 
# CompressedImage. It converts the CompressedImage into a numpy.ndarray, 
# then detects and marks features in that image. It finally displays 
# and publishes the new image - again as CompressedImage topic.


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

VERBOSE = True  # for debugging

class image_receiver:

    def __init__(self):  
        # subscribed Topic
        self.subscriber = rospy.Subscriber("/camera/color/image_raw/compressed",
            CompressedImage, self.callback,  queue_size = 1)
        if VERBOSE :
            print ("subscribed to /camera/color/image_raw/compressed")

    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected'''
        if VERBOSE :
            print('received image of type: "%s"' % ros_data.format)

        #### direct conversion to CV2 ####
        np_arr = np.frombuffer(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        cv2.imshow('cv_img', image_np)
        cv2.waitKey(2)

        

def main(args):
    ir = image_receiver() # Instanzierung der Klasse
    rospy.init_node('image_receiver', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS Image feature detector module")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)