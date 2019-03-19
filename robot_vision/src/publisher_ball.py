#!/usr/bin/env python
import roslib; roslib.load_manifest('robot_vision')

import rospy
import cv2
import numpy as np
from ball_param_msg.msg import ball_param

def read_param():
	camera_id = rospy.get_param("CameraID")
	maxb = rospy.get_param("Bmax")
	maxg = rospy.get_param("Gmax")
	maxr = rospy.get_param("Rmax")
	minb = rospy.get_param("Bmin")
	ming = rospy.get_param("Gmin")
	minr = rospy.get_param("Rmin")
	image_size_h = rospy.get_param("Width_image")
	image_size_w = rospy.get_param("Height_image")

	return camera_id, image_size_w, image_size_h, minb, ming, minr, maxb, maxg, maxr
	
            
def publish():
	try:
		pub = rospy.Publisher('ball_state', ball_param, queue_size=20)
		rospy.init_node('publisher_ball', anonymous=True)
		
		camera_id, image_size_w, image_size_h, minb, ming, minr, maxb, maxg, maxr = read_param()
		
		cam = cv2.VideoCapture(camera_id)

		print "Start" 
		param_ball_msg = ball_param()
		while not rospy.is_shutdown():
			error, image_ball = cam.read()
			image_ball = cv2.resize(image_ball, (image_size_h,image_size_w))

			y_size = np.size(image_ball, 0)
			x_size = np.size(image_ball, 1)
			
			x_offset = x_size/2
			y_offset = y_size/2

			image_ball = cv2.GaussianBlur(image_ball,(5,5),0)

			hsv_image_ball = cv2.cvtColor(image_ball, cv2.COLOR_BGR2HSV)

			bin_image_ball = cv2.inRange(hsv_image_ball, (minb, ming, minr), (maxb, maxg, maxr))

			bin_image_ball = cv2.erode(bin_image_ball,None,iterations=1)
			bin_image_ball = cv2.erode(bin_image_ball,None,iterations=2)

			contours = cv2.findContours(bin_image_ball, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
			
			contours = contours[1]
			
			x = 0
			y = 0
			radius = 0
			if len(contours):
				contours = sorted(contours, key=cv2.contourArea, reverse=True)
				#cv2.drawContours(image_ball, contours, 0, (255, 0, 255), 3)

				(x, y), radius = cv2.minEnclosingCircle(contours[0])
				center = (int(x), int(y))
				radius = int(radius)
				#cv2.circle(image_ball, center, radius, (0, 255, 0), 2)
				#cv2.imshow("Circle", image_ball)
				param_ball_msg.find_ball = True
				param_ball_msg.x_centre = x - x_offset
				param_ball_msg.y_centre = y_offset - y
				param_ball_msg.z_centre = radius
				pub.publish(param_ball_msg)
				print ("center x = " + str(x - x_offset) + " y = " + str(y_offset - y) + " radius= " + str(radius))
			else :
				param_ball_msg.find_ball = False
				pub.publish(param_ball_msg)
	except rospy.ROSInterruptException:
		return
	except KeyboardInterrupt:
		return

	cv2.destroyAllWindows()
if __name__ =='__main__':

		publish()

