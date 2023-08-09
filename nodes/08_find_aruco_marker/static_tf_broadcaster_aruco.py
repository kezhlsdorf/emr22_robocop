#!/usr/bin/env python3

# -----------------------------------------------------------------
# Version vom 21.6.22

# http://wiki.ros.org/tf/Tutorials/Adding%20a%20frame%20%28Python%29
# usage:   $ rosrun tf tf_echo world object_8

import rospy
import tf
import tf2_ros
import geometry_msgs.msg
# import numpy as np  # Scientific computing library for Python


if __name__ == '__main__':
    rospy.init_node('static_tf_broadcaster')
    br = tf2_ros.StaticTransformBroadcaster()
    tr = geometry_msgs.msg.TransformStamped()
    
    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        # Hier Abstand camera_link zum world_frame eintragen
        # vorher messen in Meter
        # x, y, z    67cm hohes Stativ
        # quaternion( rool, picth, yaw)

        tr.header.stamp = rospy.Time.now()
        #  Richtung des Pfeils:  marker_id5 ----> world
        tr.header.frame_id = "marker_id5"      
        tr.child_frame_id = "world"      
       
        # Mit Massband gemessen
        tr.transform.translation.x = 0.0
        tr.transform.translation.y = -0.65
        tr.transform.translation.z = 0.0

        quat = tf.transformations.quaternion_from_euler(0.0, 0.0, 0.0)
        tr.transform.rotation.x = quat[0]
        tr.transform.rotation.y = quat[1]
        tr.transform.rotation.z = quat[2]
        tr.transform.rotation.w = quat[3]

        br.sendTransform(tr)
        print("sending transform /marker_id5 => /world")
        print(rospy.Time.now())
        rate.sleep()
