#!/usr/bin/env python
import roslib; roslib.load_manifest('robot_goalkeeper')
import rospy
from std_msgs.msg import Int16
from ball_param_msg.msg import ball_param
def callback(data):
	pub_action = rospy.Publisher('forward_action', Int16, queue_size=10)
	pub_y_err = rospy.Publisher('forward_y_err',Int16, queue_size=10)
	action = Int16()
	rospy.loginfo(data.find_ball)
	if(data.find_ball):
		rospy.loginfo(data.x_centre)
		if (abs(data.x_centre)<20):
			action = 1
		if (data.x_centre > 20 and data.x_centre < 120):
			action = 3
		if (data.x_centre < -20 and data.x_centre > -120):
			action = 2
	if(not data.find_ball):
		rospy.loginfo(data.x_centre) 
		action = 10 
	pub_action.publish(action)
	pub_y_err.publish(data.y_centre)


def listener_publisher():
	rospy.init_node('goalkeeper_node', anonymous=True)
	rospy.Subscriber("ball_state", ball_param , callback)
	rospy.spin()

if __name__ == '__main__':
	listener_publisher()
