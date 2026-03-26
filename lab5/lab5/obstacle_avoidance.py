"""Obstacle avoidance - Potential Fields"""
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy

def euler_from_quaternion(q):
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__("obstacle_avoidance")

        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("goal_x", 3.0)
        self.declare_parameter("goal_y", 3.0)

        self.goal_x = self.get_parameter("goal_x").value
        self.goal_y = self.get_parameter("goal_y").value

        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

        self.sub_scan = self.create_subscription(LaserScan, self.get_parameter("scan_topic").value, self.scan_callback, qos)
        self.sub_odom = self.create_subscription(Odometry, self.get_parameter("odom_topic").value, self.odom_callback, 10)
        
        # ВИПРАВЛЕНО: Використовуємо TwistStamped
        self.pub_cmd = self.create_publisher(TwistStamped, self.get_parameter("cmd_vel_topic").value, 10)

        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_yaw = 0.0
        self.odom_ready = False
        self.latest_scan = None

        self.k_att = 1.2       # Зробимо притягання до цілі трохи сильнішим (було 1.0)
        self.k_rep = 0.01      # Зробимо відштовхування набагато слабшим (було 0.1)
        self.safe_dist = 0.5   # Робот почне "боятися" лише за півметра до перешкоди (було 0.8)
        self.max_v = 0.2
        self.max_w = 0.5
        self.create_timer(0.1, self.control_loop)
        self.create_timer(2.0, self.log_status)

    def odom_callback(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        self.robot_yaw = euler_from_quaternion(msg.pose.pose.orientation)
        self.odom_ready = True

    def scan_callback(self, msg):
        self.latest_scan = msg

    def log_status(self):
        if not self.odom_ready:
            self.get_logger().info("⏳ Чекаю на одометрію...")
        elif self.latest_scan is None:
            self.get_logger().info("📡 Одометрія є, чекаю на лідар...")
        else:
            dist = math.hypot(self.goal_x - self.robot_x, self.goal_y - self.robot_y)
            self.get_logger().info(f"🚀 Їду до цілі... Залишилось: {dist:.2f} м")

    def control_loop(self):
        if not self.odom_ready:
            return

        dx = self.goal_x - self.robot_x
        dy = self.goal_y - self.robot_y
        dist_to_goal = math.hypot(dx, dy)

        # Створюємо повідомлення з міткою часу
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = "base_link"

        if dist_to_goal < 0.2:
            self.get_logger().info("🎯 Ціль досягнута!")
            self.pub_cmd.publish(cmd)
            return

        fx = self.k_att * dx
        fy = self.k_att * dy

        if self.latest_scan is not None:
            for i, r in enumerate(self.latest_scan.ranges):
                if math.isinf(r) or math.isnan(r) or r < 0.2:
                    continue
                
                if r < self.safe_dist:
                    angle = self.latest_scan.angle_min + i * self.latest_scan.angle_increment
                    global_angle = self.robot_yaw + angle
                    
                    rep_force = self.k_rep * (1.0 / r - 1.0 / self.safe_dist) / (r**2)
                    fx -= rep_force * math.cos(global_angle)
                    fy -= rep_force * math.sin(global_angle)

        target_yaw = math.atan2(fy, fx)
        err_yaw = target_yaw - self.robot_yaw

        while err_yaw > math.pi: err_yaw -= 2.0 * math.pi
        while err_yaw < -math.pi: err_yaw += 2.0 * math.pi

        # Записуємо швидкості у структуру TwistStamped
        cmd.twist.angular.z = max(min(err_yaw * 1.5, self.max_w), -self.max_w)

        if abs(err_yaw) < math.pi / 4:
            cmd.twist.linear.x = self.max_v
        else:
            cmd.twist.linear.x = 0.02 

        self.pub_cmd.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
