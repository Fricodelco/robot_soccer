#!/usr/bin/env python
import roslib; roslib.load_manifest('robot_goalkeeper')
import rospy
from std_msgs.msg import Int32
from ball_param_msg.msg import ball_param
def callback(data):
	rospy.loginfo(data.find_ball)
	pubMove = rospy.Publisher('goalkeeper_action', Int32, queue_size=20)
	pubErrY = rospy.Publisher('errY', Int32, queue_size=20)
	value = Int32()
	limit_close_distance = rospy.get_param("Limit_close_distance")
	limit_mid_distance = rospy.get_param("Limit_mid_distance")
	value = -1 
	pubMove.publish(value)
	if data.find_ball is True:
		pubErrY.publish(data.x_centre)
	else:
		pubErrY.publish(555)


def listener_publisher():
	try:
		while not rospy.is_shutdown():
			rospy.init_node('goalkeeper_node', anonymous=True)
			rospy.Subscriber("ball_state", ball_param , callback)
			rospy.spin()
	except rospy.ROSInterruptException:
		return
	except KeyboardInterrupt:
		return
if __name__ == '__main__':
	listener_publisher()
