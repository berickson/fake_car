rosservice call /gazebo/apply_joint_effort "joint_name: 'back_left_wheel_joint'
effort: 0.01
start_time:
  secs: 0
  nsecs: 0
duration:
  secs: 2
  nsecs: 0"

  rosservice call /gazebo/apply_joint_effort "joint_name: 'front_left_wheel_steer_joint'
effort: 0.01
start_time:
  secs: 0
  nsecs: 0
duration:
  secs: 2
  nsecs: 0"
