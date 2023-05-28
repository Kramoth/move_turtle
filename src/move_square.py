#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math
from turtlesim.msg import Pose




def move_square():
	rospy.init_node("move_square_node")
	pub=rospy.Publisher("cmd_vel",Twist,queue_size=1)
	rate=rospy.Rate(30)
	rospy.Subscriber("pose",Pose, getPose)
	linear_speed=rospy.get_param("~linear_speed",3)
	angular_speed=rospy.get_param("~angular_speed",2)
	rospy.loginfo("starting square with linear_speed: %f and angular_speed: %f"%(linear_speed, angular_speed))
	while not rospy.is_shutdown():
		move_line(pub,rate,linear_speed)
		rotate(pub,rate,angular_speed)
		print("turtle is a coordinate (%f,%f) heading to %f"%(turtlePose.x,turtlePose.y,turtlePose.theta))
def move_line(pub,rate,linear_speed):
	cmd=Twist()
	cmd.linear.x=linear_speed
	t0=rospy.Time.now().to_sec()
	distance_travelled=0
	while(distance_travelled<4):
		pub.publish(cmd)
		t1=rospy.Time.now().to_sec()
		distance_travelled=linear_speed*(t1-t0)
		rate.sleep()

def rotate(pub,rate,angular_speed):
	cmd=Twist()
	cmd.angular.z=angular_speed
	t0=rospy.Time.now().to_sec()
	angle_travelled=0
	while(angle_travelled<=math.pi/2.0):
		pub.publish(cmd)
		t1=rospy.Time.now().to_sec()
		angle_travelled=angular_speed*(t1-t0)
		rate.sleep()
def getPose(pose):
	global turtlePose
	turtlePose=pose

if __name__=="__main__":
	try:
		move_square()
	except ROSInterruptException:
		pass
