#!/usr/bin/env python
# license removed for brevity
import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, Float32
from sensor_msgs.msg import Joy
from bicycle_model import BicycleModel, AckermannModel

steer = 0
velocity = 0

wheelbase_length = 0.3429 
front_wheelbase_width = 0.25
rear_wheelbase_width = 0.25
car_model = AckermannModel(wheelbase_length, front_wheelbase_width)

front_right_steer_pub = rospy.Publisher('/fake_car/fr_str', Float32, queue_size=10)
front_left_steer_pub = rospy.Publisher('/fake_car/fl_str', Float32, queue_size=10)

back_left_speed_pub = rospy.Publisher('/fake_car/back_left_wheel_velocity_controller/command', Float64, queue_size=10)
back_right_speed_pub = rospy.Publisher('/fake_car/back_right_wheel_velocity_controller/command', Float64, queue_size=10)



def joy_callback(msg):
    ad = AckermannDriveStamped()
    ad.drive.steering_angle = msg.axes[3]
    ad.drive.speed = msg.axes[1] * 100
    pub.publish(ad)


def ackermann_callback(msg):
    #rospy.loginfo(rospy.get_caller_id() + "Steering angle %s", msg.drive.steering_angle)
    #rospy.loginfo(rospy.get_caller_id() + "Speed: %s", msg.drive.speed)

    car_model.set_steer_angle(msg.drive.steering_angle)

    front_right_steer_pub.publish(car_model.get_right_bicycle().get_steer_angle())
    front_left_steer_pub.publish(car_model.get_left_bicycle().get_steer_angle())

    
    curvature = car_model.get_rear_curvature()
    if(curvature == 0):
        back_left_speed_pub.publish(msg.drive.speed)
        back_right_speed_pub.publish(msg.drive.speed)
    else:
        radius = 1/curvature
        left_radius = radius - rear_wheelbase_width / 2
        right_radius = radius + rear_wheelbase_width / 2
        back_left_speed_pub.publish(msg.drive.speed*left_radius/radius)
        back_right_speed_pub.publish(msg.drive.speed*right_radius/radius)

def twist_callback(msg):
    ad = AckermannDriveStamped()
    ad.drive.speed = msg.linear.x
   
    if msg.linear.x == 0:
        ad.drive.steering_angle = 0
    else:
        car_model.set_rear_curvature(msg.angular.z / msg.linear.x)
        ad.drive.steering_angle = car_model.get_steer_angle()
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