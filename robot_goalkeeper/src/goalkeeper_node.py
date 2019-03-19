#!/usr/bin/env python
import roslib; roslib.load_manifest('robot_goalkeeper')
import rospy
from std_msgs.msg import Int32
from ball_param_msg.msg import ball_param
def callback(data):
	rospy.loginfo(data.find_ball)
	pub = rospy.Publisher('goalkeeper_action', Int32, queue_size=20)
	value = Int32()
	limit_close_distance = rospy.get_param("Limit_close_distance")
	limit_mid_distance = rospy.get_param("Limit_mid_distance")
	while not rospy.is_shutdown():
		value = -1 
		pub.publish(value)


def listener_publisher():
	rospy.init_node('goalkeeper_node', anonymous=True)
	rospy.Subscriber("ball_state", ball_param , callback)
	rospy.spin()

if __name__ == '__main__':
	listener_publisher()
