#!/usr/bin/env python3


'''
This is a boiler plate script that contains an example on how to subscribe a rostopic containing camera frames 
and store it into an OpenCV image to use it further for image processing tasks.
Use this code snippet in your code or you can also continue adding your code in the same file


This python file runs a ROS-node of name marker_detection which detects a moving ArUco marker.
This node publishes and subsribes the following topics:

	Subsriptions					Publications
	/camera/camera/image_raw			/marker_info
'''
from sensor_msgs.msg import Image
from task_1.msg import Marker
from cv_bridge import CvBridge, CvBridgeError
import cv2
import cv2.aruco as aruco
import numpy as np
import rospy
import math

def calculate_centroid(topLeft, topRight, bottomRight, bottomLeft):
	cX = (topLeft[0] + bottomRight[0]) / 2.0
	cY = (topLeft[1] + bottomRight[1]) / 2.0
	return cX, cY

def detect_ArUco(img):
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
	parameters = aruco.DetectorParameters_create()
	corners, ids, _ = aruco.detectMarkers(grey, aruco_dict, parameters=parameters)
	d = {}

	ids = ids.flatten()

	
	for i in range(len(ids)):
		d[ids[i]] = corners[i]
	
	return d

def get_marker_orientation(topRight, bottomLeft):
    top_right_angle = (math.degrees(math.atan2(-topRight[1] + bottomLeft[1], topRight[0] - bottomLeft[0]))) % 360
    angle = (top_right_angle + 45) % 360
    return angle

def detect_pos_and_id(img):
	d = {}
	answer = {}
	Detected_ArUco_markers= detect_ArUco(img)
	for (markerId) in Detected_ArUco_markers:
		vertices = Detected_ArUco_markers[markerId].reshape(4, 2)
		topLeft, topRight, bottomRight, bottomLeft = vertices
		topRight = (int(topRight[0]), int(topRight[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		cX, cY = calculate_centroid(topLeft, topRight, bottomRight, bottomLeft)
		angle = get_marker_orientation(topRight, bottomLeft)
		answer[markerId] = [cX, cY, angle]
	return answer
		

class image_proc():

	# Initialise everything
	def __init__(self):
		rospy.init_node('marker_detection') #Initialise rosnode 
		
		# Making a publisher 
		
		self.marker_pub = rospy.Publisher('/marker_info', Marker, queue_size=1)
		
		# ------------------------Add other ROS Publishers here-----------------------------------------------------
	
        	# Subscribing to /camera/camera/image_raw

		self.image_sub = rospy.Subscriber("/camera/camera/image_raw", Image, self.image_callback) #Subscribing to the camera topic
		
	        # -------------------------Add other ROS Subscribers here----------------------------------------------------
        
		self.img = np.empty([]) # This will contain your image frame from camera
		self.bridge = CvBridge()
		
		self.marker_msg=Marker()  # This will contain the message structure of message type task_1/Marker
	# Callback function of camera topic
	def image_callback(self, data):
	# Note: Do not make this function lenghty, do all the processing outside this callback function
		try:
			self.img = self.bridge.imgmsg_to_cv2(data, "bgr8") # Converting the image to OpenCV standard image
			a = detect_pos_and_id(self.img)
			#print(a)
			for i in a:
				self.marker_msg.id = i
				self.marker_msg.x = a[i][0]
				self.marker_msg.y = a[i][1]
				self.marker_msg.yaw = a[i][2]
		except CvBridgeError as e:
			print(e)
			return
			
	def publish_data(self):
		#print(self.marker_msg)
		self.marker_pub.publish(self.marker_msg)

if __name__ == '__main__':
    image_proc_obj = image_proc()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
    	try:
    		image_proc_obj.publish_data()
    		rate.sleep()
    	except rospy.ROSInterruptException:
	    	pass
    		
    rospy.spin()
