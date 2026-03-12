#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool


class BatteryNode(Node):
    """
    Симулятор батареи робота.
    Разряжается со временем, быстрее при движении.
    """
    
    def __init__(self):
        super().__init__('battery_node')
        
        # Начальные параметры
        self.battery_level = 100.0  # процент заряда
        
        # Publisher для уровня батареи
        self.battery_publisher = self.create_publisher(
            Float32,
            '/battery_level',
            10
        )
        
        # Таймер для разрядки батареи (каждую 1 секунду - 1 Гц)
        self.timer = self.create_timer(1.0, self.update_battery)
        
        self.get_logger().info('Battery node started, publishing at 1 Hz')
    
    
    def update_battery(self):
        # Проверка на минимальный уровень
        if self.battery_level <= 0.0:
            self.battery_level = 0.0
        else:
            self.battery_level -= 1 
        
        if self.battery_level % 10 == 0:
            self.get_logger().warn(f'Battery: {self.battery_level:.1f}%')
        
        msg = Float32()
        msg.data = max(0.0, self.battery_level)
        self.battery_publisher.publish(msg)
        


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
