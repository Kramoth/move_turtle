#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
import time

class SquareMover(Node):

    def __init__(self):
        super().__init__('square_mover')
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose = None
        self.timer = self.create_timer(0.1, self.move_square)
        self.state = 'forward'
        self.start_x = None
        self.start_y = None
        self.edge_count = 0

    def pose_callback(self, msg):
        self.pose = msg

    def move_square(self):
        if self.pose is None:
            return

        cmd = Twist()

        if self.state == 'forward':
            if self.start_x is None:
                self.start_x = self.pose.x
                self.start_y = self.pose.y

            # Avancer tout droit sur ~2 unités
            distance = math.sqrt((self.pose.x - self.start_x)**2 + (self.pose.y - self.start_y)**2)
            if distance < 2.0:
                cmd.linear.x = 1.0
                cmd.angular.z = 0.0
            else:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.state = 'turn'
                self.turn_start_angle = self.pose.theta

        elif self.state == 'turn':
            # Tourner jusqu'à 90°
            angle_diff = abs(self.normalize_angle(self.pose.theta - self.turn_start_angle))
            if angle_diff < math.pi / 2.0:
                cmd.angular.z = 1.0
                cmd.linear.x = 0.0
            else:
                cmd.angular.z = 0.0
                self.start_x = None
                self.start_y = None
                self.edge_count += 1
                if self.edge_count >= 4:
                    self.get_logger().info('Carré terminé !')
                    self.timer.cancel()
                    return
                self.state = 'forward'

        self.cmd_pub.publish(cmd)

    def normalize_angle(self, angle):
        """Ramène un angle entre -pi et pi"""
        while angle > math.pi:
            angle -= 2*math.pi
        while angle < -math.pi:
            angle += 2*math.pi
        return angle

def main(args=None):
    rclpy.init(args=args)
    node = SquareMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()