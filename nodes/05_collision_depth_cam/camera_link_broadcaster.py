#!/usr/bin/env python3

# http://wiki.ros.org/tf/Tutorials/Adding%20a%20frame%20%28Python%29
# usage:   $ rosrun tf tf_echo world object_8

import rospy
import tf
import numpy as np  # Scientific computing library for Python

if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        
        # Hier Abstand camera_link zum world_frame eintragen
        # vorher messen in Meter
        # x, y, z    67cm hohes Stativ
        # quaternion_from_euler( rool, pitch, yaw)
        
        # UR5e 13_06_22  
        br.sendTransform((1.65, -0.0205, 0.09),
                         (tf.transformations.quaternion_from_euler(-np.pi + 15.0*np.pi/180, np.pi * (0.575), 13.8*np.pi/180, 'sxyz')),  # rpy # (1.0, -0.90, 0.0) (-3.14 , 1.3, 0.0)
                         rospy.Time.now(),
                         "camera_link",
                         "world")
        print("sending transform /world => /camera_link")

        br.sendTransform((0, 0, 0),
                         (tf.transformations.quaternion_from_euler(0, 0, 0 , 'sxyz')),  # rpy
                         rospy.Time.now(),
                         "base_link",
                         "world")
        print("sending transform /world => /base_link")

        print(rospy.Time.now())
        rate.sleep()
