#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class distance_sensor(Node):
    
    def __init__(self):
        super().__init__('distance_sensor')
        
        # Текущее расстояние до препятствия
        self.distance = 3.0
        
        # Таймер для публикации на частоте 5 Hz
        self.timer_period = 0.2  # 5 Hz = 0.2 секунды
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        # Publisher для данных расстояния
        self.distance_publisher = self.create_publisher(
            Float32,
            '/distance',
            10
        )
        
        # Subscriber для команд движения - ИСПРАВЛЕНО
        self.cmd_subscriber = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        # Хранение последней полученной команды
        self.last_cmd_vel = Twist()
        
    
    def cmd_vel_callback(self, msg):
        """Получаем и сохраняем команды движения."""
        self.last_cmd_vel = msg
        # Добавим логирование для отладки
    
    def timer_callback(self):
        """Периодически обновляем расстояние и публикуем данные."""
        # Обновляем расстояние на основе текущей команды
        self.update_distance()
        
        # Публикуем текущее расстояние
        msg = Float32()
        msg.data = self.distance
        self.distance_publisher.publish(msg)
        
    
    def update_distance(self):
        """Обновляет значение расстояния в зависимости от команды движения."""
        if abs(self.last_cmd_vel.linear.x) < 0.01:  # Используем допуск для учета погрешностей
            # Если стоим - расстояние возвращается к 3.0 м
            if self.distance < 3.0:
                self.distance = min(3.0, self.distance + 0.05)
        
        elif self.last_cmd_vel.linear.x > 0:
            # Если едем вперед - расстояние уменьшается
            self.distance = max(0.5, self.distance - 0.05)
        
        elif self.last_cmd_vel.linear.x < 0:
            # Если едем назад - расстояние увеличивается
            self.distance = min(3.0, self.distance + 0.05)


def main(args=None):
    rclpy.init(args=args)
    node = distance_sensor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Distance Sensor stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()