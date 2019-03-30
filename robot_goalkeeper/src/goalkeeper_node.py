#!/usr/bin/env python
import roslib; roslib.load_manifest('robot_goalkeeper')
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Byte
from ball_param_msg.msg import ball_param
from time import sleep

Is_Ball = False
is_fall = False
y = 0
x = 0
x_ball = 0
x_old = 0
y_ball = 0
y_old = 0
radius = 0
count_find_shoot = 0
pub_action = rospy.Publisher('forward_action', Int16, queue_size=10)
pub_y_err = rospy.Publisher('forward_y_err',Int16, queue_size=10)
pub_x_err = rospy.Publisher('forward_x_err',Int16, queue_size=10)
def Go_To_Ball():
        action = Int16()
        global x,y, x_ball, y_ball, x_old, y_old
        if (abs(x)<=20):
                action = 1
 	if (x < -20  and x_ball <= 160):
                action = 5
                x=-11
        if (x > 20 and x_ball >= -160):
                action = 4
                x=11
        pub_x_err.publish(x)
        pub_action.publish(action)
def Shoot_Ball():
        global y,x,x_ball
        #y=-10
        #pub_y_err.publish(y)
        if (x <= 0):
                action = 7
        else :
                action = 6
        #pub_y_err.publish(y)
        pub_action.publish(action)
        #pub_action.publish(0)

def callback(data):
        global x,y,radius, Is_Ball, x_ball, y_ball, x_old, y_old
        Is_Ball = data.find_ball
        x_ball = data.x_centre
        y_ball = data.y_centre
        radius = data.z_centre
        if (Is_Ball):
                if (abs(y_ball)>20):
                        y_old = y_old+y_ball
                        y = y + 0.03*y_ball
                        #y = y - 0.4*(y_old-y)
                        if y>15:
                                y=15
                        elif(y<-60):
                                y=-60
                if (abs(x_ball)>20):
                        x_old = x_old+x_ball
                        x = x - 0.035*x_ball
                        #x = x + 0.2*(x_old-x)
                        if(x>40):
                                x=40
                        elif(x<-40):
                                x=-40
                pub_y_err.publish(y)
                pub_x_err.publish(x)
        else :
                x=0
                pub_y_err.publish(555)
                pub_x_err.publish(555)

        #rospy.loginfo(data.find_ball)


def Main_Forward(state):
        global x,y,radius,Is_Ball, x_ball, y_ball, count_find_shoot, is_fall
        rospy.loginfo(Is_Ball)
	if(not is_fall):
        	if(Is_Ball):
                	rospy.loginfo(x_ball)
                	err = y + 0.4 * y_ball
             		if(err > -40):
               	        	Go_To_Ball()
                        	count_find_shoot = 0
                	elif (abs(x) < 20):
                        	if(count_find_shoot < 1):
                                	Shoot_Ball()
                                	count_find_shoot = count_find_shoot+1
                        	else :
                                	count_find_shoot = 0
                	elif (x>=20):
                        	action = 4
                        	x = x - 11
                        	pub_action.publish(action)
                        	pub_x_err.publish(x)
                	elif (x<=-20):
                        	action = 5
                        	x = x + 11
                        	pub_action.publish(action)
                        	pub_x_err.publish(x)
        	else:
                	#rospy.loginfo(data.x_centre)
                	action = 10
                	count_find_shoot=0
                	pub_action.publish(action)
                	pub_y_err.publish(555)
                	pub_x_err.publish(555)
def fall_action(fall_number):
	global is_fall
	rospy.loginfo(fall_number.data)
	if(fall_number.data == 0):
		is_fall = False
	if(fall_number.data == 1):
		is_fall = True
		action = 12
		pub_action.publish(action)
	if(fall_number.data == -1):
		is_fall = True
		action = 11
		pub_action.publish(action)
		
def listener_publisher():
        rospy.init_node('goalkeeper_node', anonymous=True)
	rospy.Subscriber("Orientation", Int16, fall_action)
        rospy.Subscriber("ball_state", ball_param , callback)
        rospy.Subscriber("motion_ready", Byte, Main_Forward)
        rospy.spin()

if __name__ == '__main__':
        listener_publisher()
