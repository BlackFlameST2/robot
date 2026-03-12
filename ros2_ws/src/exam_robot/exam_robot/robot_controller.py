#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class robot_controller(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        # --- Subscriber ---
        self.robot_status_sub = self.create_subscription(
            String, '/robot_status', self.robot_callback, 10)
        
        # --- Publisher ---
        self.cmd_vel_pub = self.create_publisher( 
            Twist, '/cmd_vel', 10)
        
        # --- Таймер для публикации ---
        self.timer = self.create_timer(0.1, self.publish_cmd_vel) 
        
        self.current_status = ""
        self.last_status = ""

    def robot_callback(self, msg):
        self.current_status = msg.data
    
    def publish_cmd_vel(self):
        cmd = Twist()
        
        if self.current_status == "ALL OK":
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
        elif self.current_status == "WARNING: Low battery":
            cmd.linear.x = 0.1
            cmd.angular.z = 0.0
        elif self.current_status == "WARNING: Obstacle close":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
        elif self.current_status == "CRITICAL":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
        
        self.cmd_vel_pub.publish(cmd)
        
        if self.current_status != self.last_status:
            self.get_logger().info(f'Режим изменен на: {self.current_status}')
            self.last_status = self.current_status


def main(args=None):
    rclpy.init(args=args)
    node = robot_controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()