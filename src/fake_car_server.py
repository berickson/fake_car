#!/usr/bin/env python
# license removed for brevity
import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy

steer = 0
velocity = 0


front_right_steer_pub = rospy.Publisher('/fake_car/front_left_wheel_steer_position_controller/command', Float64, queue_size=10)
front_left_steer_pub = rospy.Publisher('/fake_car/front_right_wheel_steer_position_controller/command', Float64, queue_size=10)

back_left_speed_pub = rospy.Publisher('/fake_car/back_left_wheel_velocity_controller/command', Float64, queue_size=10)
back_right_speed_pub = rospy.Publisher('/fake_car/back_right_wheel_velocity_controller/command', Float64, queue_size=10)



def joy_callback(msg):
    ad = AckermannDriveStamped()
    ad.drive.steering_angle = msg.axes[3]
    ad.drive.speed = msg.axes[1] * 100
    pub.publish(ad)


def ackermann_callback(msg):
    rospy.loginfo(rospy.get_caller_id() + "Steering angle %s", msg.drive.steering_angle)
    rospy.loginfo(rospy.get_caller_id() + "Speed: %s", msg.drive.speed)

    front_right_steer_pub.publish(msg.drive.steering_angle)
    front_left_steer_pub.publish(msg.drive.steering_angle)

    back_left_speed_pub.publish(msg.drive.speed)
    back_right_speed_pub.publish(msg.drive.speed)

def twist_callback(msg):
    ad = AckermannDriveStamped()
    ad.drive.speed = msg.linear.x
    # hack, need real formula
    ad.drive.steering_angle = 0 if msg.linear.x == 0 else msg.angular.z / msg.linear.x
    pub.publish(ad)



def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    # rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("joy", Joy, joy_callback)
    rospy.Subscriber("cmd_vel", Twist, twist_callback)
    rospy.Subscriber("cmd_ackermann", AckermannDriveStamped, ackermann_callback)

def talker():
    rospy.init_node('fake_car_server', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg = AckermannDriveStamped()
    
        #rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        #rate = rospy.Rate(10)
        rospy.init_node('fake_car_server', anonymous=True)
        pub = rospy.Publisher('cmd_ackermann', AckermannDriveStamped, queue_size=10)
        listener()
        #talker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass