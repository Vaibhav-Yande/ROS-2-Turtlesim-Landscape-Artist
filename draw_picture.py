#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, TeleportAbsolute, Spawn
import time, math

class Drawer(Node):
    def __init__(self):
        super().__init__('drawer')
        self.p1 = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pen1 = self.create_client(SetPen, '/turtle1/set_pen')
        self.tp1 = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        
        self.p2 = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.pen2 = self.create_client(SetPen, '/turtle2/set_pen')
        self.tp2 = self.create_client(TeleportAbsolute, '/turtle2/teleport_absolute')
        
        self.spawn_c = self.create_client(Spawn, '/spawn')

        self.pen1.wait_for_service()
        self.tp1.wait_for_service()
        self.spawn_c.wait_for_service()

        self.get_logger().info('Spawning Turtle 2...')
        req = Spawn.Request()
        req.x, req.y, req.theta = 2.0, 2.0, 0.0
        f = self.spawn_c.call_async(req)
        rclpy.spin_until_future_complete(self, f)
        time.sleep(1.0)

        self.pen2.wait_for_service()
        self.tp2.wait_for_service()
        self.get_logger().info('Both turtles are ready!')

    def ent(self, t):
        return (self.p1, self.pen1, self.tp1) if t == 'turtle1' else (self.p2, self.pen2, self.tp2)

    def pen(self, t, c, w, o):
        _, p, _ = self.ent(t)
        r = SetPen.Request()
        r.r, r.g, r.b, r.width, r.off = c[0], c[1], c[2], w, o
        f = p.call_async(r)
        rclpy.spin_until_future_complete(self, f)
        time.sleep(0.2) 

    def tp(self, t, x, y, a):
        _, _, tr = self.ent(t)
        r = TeleportAbsolute.Request()
        r.x, r.y, r.theta = float(x), float(y), float(a)
        f = tr.call_async(r)
        rclpy.spin_until_future_complete(self, f)
        time.sleep(0.2) 

    def mv(self, t, l, a, d):
        p, _, _ = self.ent(t)
        end = time.time() + d
        while time.time() < end:
            m = Twist()
            m.linear.x, m.angular.z = l, a
            p.publish(m)
            time.sleep(0.05)
        p.publish(Twist())
        time.sleep(0.1)

    def fwd(self, t, d, s=2.5): 
        self.mv(t, (1.0 if d > 0 else -1.0) * s, 0.0, abs(d)/s)

    # Draws a 100% mathematically perfect straight line using teleport
    def line(self, t, x1, y1, x2, y2):
        self.pen(t, (0,0,0), 1, 1) # Pen up
        self.tp(t, x1, y1, 0.0)    # Go to start
        self.pen(t, (255,0,0), 3, 0) # Pen down (Red)
        self.tp(t, x2, y2, 0.0)    # Go to end (Draws line)
        self.pen(t, (0,0,0), 1, 1) # Pen up

    def draw_circle(self, t, x, y, r, color):
        self.pen(t, (0,0,0), 1, 1)
        self.tp(t, x, y - r, 0.0)
        self.pen(t, color, 3, 0)
        self.mv(t, 2.5, 2.5/r, (2 * math.pi * r) / 2.5)
        self.pen(t, (0,0,0), 1, 1)

    def draw_sun(self, t, x, y, r):
        self.draw_circle(t, x, y, r, (255, 200, 0))
        for i in range(8):
            ang = i * math.pi / 4
            self.pen(t, (0,0,0), 1, 1)
            self.tp(t, x + (r + 0.2) * math.cos(ang), y + (r + 0.2) * math.sin(ang), ang)
            self.pen(t, (255, 200, 0), 3, 0)
            self.fwd(t, 0.6)
            self.pen(t, (0,0,0), 1, 1)

    def draw_cloud(self, t, x, y):
        self.draw_circle(t, x, y, 0.6, (255, 255, 255))
        self.draw_circle(t, x + 0.8, y + 0.2, 0.8, (255, 255, 255))
        self.draw_circle(t, x + 1.6, y, 0.6, (255, 255, 255))

    def draw_tree(self, t, cx, cy):
        # Trunk
        self.line(t, cx - 0.2, cy, cx + 0.2, cy)
        self.line(t, cx + 0.2, cy, cx + 0.2, cy + 1.0)
        self.line(t, cx + 0.2, cy + 1.0, cx - 0.2, cy + 1.0)
        self.line(t, cx - 0.2, cy + 1.0, cx - 0.2, cy)
        # Leaves
        self.line(t, cx - 1.0, cy + 1.0, cx + 1.0, cy + 1.0)
        self.line(t, cx + 1.0, cy + 1.0, cx, cy + 2.732)
        self.line(t, cx, cy + 2.732, cx - 1.0, cy + 1.0)

    def draw(self):
        self.get_logger().info('====================================')
        self.get_logger().info('   STARTING DRAWING VERSION 9 (FIXED)  ')
        self.get_logger().info('====================================')
        
        self.draw_sun('turtle2', 9.0, 8.5, 0.7)
        self.draw_cloud('turtle2', 1.5, 8.5)
        self.draw_cloud('turtle2', 5.5, 9.0)

        # House
        p_bl = (4.0, 2.5); p_br = (7.0, 2.5); p_tr = (7.0, 5.0)
        p_peak = (5.5, 6.5); p_tl = (4.0, 5.0)
        
        self.line('turtle1', *p_bl, *p_br)
        self.line('turtle1', *p_br, *p_tr)
        self.line('turtle1', *p_tr, *p_peak)
        self.line('turtle1', *p_peak, *p_tl)
        self.line('turtle1', *p_tl, *p_bl)
        
        # Door
        self.line('turtle1', 4.8, 2.5, 5.4, 2.5)
        self.line('turtle1', 5.4, 2.5, 5.4, 3.5)
        self.line('turtle1', 5.4, 3.5, 4.8, 3.5)
        self.line('turtle1', 4.8, 3.5, 4.8, 2.5)
        
        # Window
        self.line('turtle1', 6.0, 3.5, 6.5, 3.5)
        self.line('turtle1', 6.5, 3.5, 6.5, 4.0)
        self.line('turtle1', 6.5, 4.0, 6.0, 4.0)
        self.line('turtle1', 6.0, 4.0, 6.0, 3.5)

        self.draw_tree('turtle2', 1.5, 1.0)
        self.draw_tree('turtle2', 9.0, 1.0)
        self.draw_tree('turtle2', 1.0, 3.5)
        self.draw_tree('turtle2', 9.5, 3.5)

        self.get_logger().info('Drawing Complete!')

def main():
    rclpy.init()
    n = Drawer()
    try: n.draw()
    except KeyboardInterrupt: pass
    finally: n.destroy_node(); rclpy.shutdown()

if __name__ == '__main__': main()
