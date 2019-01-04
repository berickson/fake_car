#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

pub_str = rospy.Publisher('str', Int16, queue_size=1)
pub_esc = rospy.Publisher('esc', Int16, queue_size=1)
esc_us = 1500
str_us = 1500


def esc_callback(data):
    esc_us = data
    pub_esc.publish(esc_us)

def str_callback(data):
    j = SetJointProperties();
    
    str_us = data
    pub_str.publish(str_us)

def main():
    rospy.init_node('fake_car_controller', anonymous=True)
    rospy.Subscriber('/cmd_str', Int16, str_callback)
    rospy.Subscriber('/cmd_esc', Int16, esc_callback)
    rate = rospy.Rate(10) # 10hz
    pub_str.publish(str_us)
    pub_esc.publish(esc_us)
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass