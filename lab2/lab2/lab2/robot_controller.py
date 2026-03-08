#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        # Створюємо паблішер для топіка /cmd_vel
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Створюємо таймер для публікації з частотою 10Hz (кожні 0.1 с)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.counter = 0
        self.get_logger().info('Robot Controller started - publishing to /cmd_vel')

    def timer_callback(self):
        """Викликається кожні 0.1 секунди для відправки команд швидкості"""
        msg = Twist()
        
        # Рух вперед із синусоїдальним поворотом
        msg.linear.x = 0.5  # 0.5 м/с вперед
        msg.angular.z = 0.3 * math.sin(self.counter * 0.1)  # Хвилеподібний рух
        
        self.publisher.publish(msg)
        self.counter += 1
        
        # Виводимо лог кожні 5 секунд
        if self.counter % 50 == 0:
            self.get_logger().info(
                f'Publishing: linear.x={msg.linear.x:.2f}, '
                f'angular.z={msg.angular.z:.2f}'
            )

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    
    try:
        rclpy.spin(node)  # Тримаємо ноду запущеною
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
