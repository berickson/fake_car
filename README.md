Getting started:


```
################
# initial setup
################
apt-get install ros-melodic-ackermann-msgs
source /opt/ros/melodic/setup.bash
mkdir -p ros_ws/src
cd ros_ws/src
git clone git@github.com:berickson/fake_car.git
git clone git@github.com:berickson/fake_car_plugin.git
cd ..
catkin_make

################
# every time
################

#in one terminal
cd ~/ros_ws
source devel/setup.bash
roscore

# in another terminal
cd ~/ros_ws
source devel/setup.bash
roslaunch fake_car fake_car.launch
```
