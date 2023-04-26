#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://answers.ros.org/question/276176/print-message-from-launch-file/

'''
# Name: print_to_screen.py
# Author: Joseph Coombe


In your *.launch script, if you set the node's output attribute to "screen", the message will be printed to the terminal window.

<node name="PrintToScreenNode_1" pkg="my_package" type="print_info_from_launch.py" output="screen"/>

'''

# Uncomment lines 10, 13, 15 if you're running this node in its own separate
# terminal window. Otherwise the script will immediately exit and its terminal window will close.
# import rospy


def main():
    # rospy.init_node('print_to_screen', anonymous=True)
    print("Please keep this running in a separate tab.")
    # rospy.spin()


if __name__ == '__main__':
    main()
