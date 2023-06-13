#!/usr/bin/env python3

# -----------------------------------------------------------------
# Version vom 21.6.22

# http://wiki.ros.org/tf/Tutorials/Adding%20a%20frame%20%28Python%29
# usage:   $ rosrun tf tf_echo world object_8

import rospy
import tf
import numpy as np  # Scientific computing library for Python


if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(1.0)
    while not rospy.is_shutdown():
        # Hier Abstand camera_link zum world_frame eintragen
        # vorher messen in Meter
        # x, y, z    67cm hohes Stativ
        # quaternion( rool, picth, yaw)

        # original transform
        # # was br.sendTransform((-0.255, -0.47, 0.6),
        # br.sendTransform((-0.233, -0.43, 0.62),
        #                  (tf.transformations.quaternion_from_euler(0, 0.80, 0.88, axes='sxyz')),
        #                  #(tf.transformations.quaternion_from_euler(0, 0.88, 0.785, axes='sxyz')),
        #                  rospy.Time.now(),
        #                  "camera_link",
        #                  "world")

        # new transform
        # (tf.transformations.quaternion_from_euler(-np.pi + 15.0*np.pi/180, np.pi * (0.575), 13.8*np.pi/180, 'sxyz')),  # rpy # (1.0, -0.90, 0.0) (-3.14 , 1.3, 0.0)
                         
        br.sendTransform((0.45, 0.45, 0.0),
                         (tf.transformations.quaternion_from_euler(0.0, 0.0, 2.25)),  # rpy
                         rospy.Time.now(),
                         "world",
                         "marker_id5")  # Reference Frame for transformation  
        print("sending transform /marker_id5 => /world")
        print(rospy.Time.now())
        rate.sleep()

