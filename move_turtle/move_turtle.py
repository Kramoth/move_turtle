#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import sqrt, pi, atan, tan
    
class MoveSquareNode(Node):
    def __init__(self):
        super().__init__("move_square")
        self.turtle_pose=None
        self.start_x=None
        self.start_y=None
        self.start_orientation=None
        self.state="forward"
        self.square_length=2
        self.pose_sub=self.create_subscription(Pose, "turtle1/pose", self.update_pose, 10)
        self.cmd_pub=self.create_publisher(Twist, "turtle1/cmd_vel", 10) 
        self.create_timer(0.03, self.move_turtle)
    def update_pose(self, msg:Pose):
        self.turtle_pose=msg   
    
    def move_turtle(self):
        cmd_msg=Twist()
        # si la position de la tortue n'est pas encore connue alors on ne calcule pas la cmd vel 
        if self.turtle_pose is None: 
            return
        if self.start_x is None:
            self.start_x=self.turtle_pose.x
            self.start_y=self.turtle_pose.y
            self.start_orientation=self.turtle_pose.theta
        if self.state=="forward":
            distance=sqrt((self.turtle_pose.x-self.start_x)**2+(self.turtle_pose.y-self.start_y)**2)
            if distance<self.square_length:
                cmd_msg.linear.x=3.0
            else:
                self.state="turn"
                self.start_x=self.turtle_pose.x
                self.start_y=self.turtle_pose.y
                self.start_orientation=self.turtle_pose.theta
        if self.state=="turn":
            diff_theta=self.turtle_pose.theta-self.start_orientation
            heading_travel = (diff_theta + pi) % (2 * pi) - pi
            self.get_logger().info(str(heading_travel))
            if abs(heading_travel)<pi/2:
                cmd_msg.angular.z=2.0
            else:
                self.state="forward"
                self.start_x=self.turtle_pose.x
                self.start_y=self.turtle_pose.y
                self.start_orientation=self.turtle_pose.theta


            
        self.cmd_pub.publish(cmd_msg)
        
    
def main(args=None):
    rclpy.init(args=args)
    node = MoveSquareNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()