#!/usr/bin/env python3
############## Task1.1 - ArUco Detection ##############

import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time
#corner[0][0] = topleft
#corner[0][1] = topright
#corner[0][2] = bottomright
#corner[0][3] = bottomleft
def get_corner_colour_dict(tr, tl, br, bl):
	d = {tr: (0,255,0), tl: (125,125,125), br: (180,105,255), bl: (255,255,255)}
	return d
	
def calculate_centroid(corner):
	print(corner[0][0][0])
	cX = int(((corner[0][0] + corner[0][2]) / 2.0))
	cY = int((corner[0][0] + corner[0][2]) / 2.0)
	return cX, cY
	
def calculate_midpoint(corner):
	mX, mY = (corner[0][1] + corner[0][2])//2 , (corner[0][1] + corner[0][2])//2
	return mX, mY

def draw_corner_dots(img, ccd):
	for i in ccd:
		cv2.circle(img, i, 2, ccd[i], 5)
		
def draw_borders(img, corner, colour):
	cv2.line(img, corner[0][0], corner[0][1], colour, 2)
	cv2.line(img, corner[0][1], corner[0][1], colour, 2)
	cv2.line(img, corner[0][1], corner[0][3], colour, 2)
	cv2.line(img, corner[0][3], corner[0][0], colour, 2)
	
def draw_centroid(img, corner, colour):
	cX = int((corner[0][0][0] + corner[0][2][0]) / 2.0)
	cY = int((corner[0][0][1] + corner[0][2][1]) / 2.0)
	cv2.circle(img, (cX, cY), 4, colour, -1)
	return cX, cY
	
def draw_center_to_midpt_line(img, cX, cY, corner, colour):
	mpX, mpY= (corner[0][1][0] + corner[0][2][0])//2 , (corner[0][1][1] + corner[0][2][1])//2
	cv2.line(img, (cX, cY), (mpX, mpY), colour, 2)
	print(f"(({mpX}, {mpY}), ({cX}, {cY}))")
	height = img.shape[0]
	width = img.shape[1]
	angle_finder(mpX, mpY, cX, cY)

def detect_ArUco(img):
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
	parameters = aruco.DetectorParameters_create()
	corners, ids, _ = aruco.detectMarkers(grey, aruco_dict, parameters=parameters)
	d = {}

	## function to detect ArUco markers in the image using ArUco library
	## argument: img is the test image
	## return: dictionary named Detected_ArUco_markers of the format {ArUco_id_no : corners}, where ArUco_id_no indicates ArUco id and corners indicates the four corner position of the aruco(numpy array)
	## 		   for instance, if there is an ArUco(0) in some orientation then, ArUco_list can be like
	## 				{0: array([[315, 163],
	#							[319, 263],
	#							[219, 267],
	#							[215,167]], dtype=float32)}
	ids = ids.flatten()
	#print(ids, corners)
	
	for i in range(len(ids)):
		d[ids[i]] = corners[i]
	


	return d


def Calculate_orientation_in_degree(Detected_ArUco_markers):
	## function to calculate orientation of ArUco with respective to the scale mentioned in problem statement
	## argument: Detected_ArUco_markers  is the dictionary returned by the function detect_ArUco(img)
	## return : Dictionary named ArUco_marker_angles in which keys are ArUco ids and the values are angles (angles have to be calculated as mentioned in the problem statement)
	##			for instance, if there are two ArUco markers with id 1 and 2 with angles 120 and 164 respectively, the 
	##			function should return: {1: 120 , 2: 164}
	#print(Detected_ArUco_markers)
	ArUco_marker_angles = {}
	d = Detected_ArUco_markers	
	for markerId in Detected_ArUco_markers:
		#markerId = markerId.flatten()
		#print(markerId, d[markerId])
		mpX, mpY = calculate_midpoint(d[markerId])
		cX, cY = calculate_centroid(d[markerId])
		if mpX > cX:
			if mpY > cY:
				angle = 270+math.degrees(math.atan(abs((mpY-cY)/(mpX-cX))))
			else:
				angle = (math.degrees(math.atan(abs((mpY-cY)/(mpX-cX)))))
		else:
			if mpY > cY:
				angle = (180+math.degrees(math.atan(abs((mpY-cY)/(mpX-cX)))))
			else:
				angle = (90+math.degrees(math.atan(abs((mpY-cY)/(mpX-cX)))))
		ArUco_marker_angles[markerId] = angle
	
	return ArUco_marker_angles	

def mark_ArUco(img, Detected_ArUco_markers, ArUco_marker_angles):
	## function to mark ArUco in the test image as per the instructions given in problem statement
	## arguments: img is the test image 
	##			  Detected_ArUco_markers is the dictionary returned by function detect_ArUco(img)
	##			  ArUco_marker_angles is the return value of Calculate_orientation_in_degree(Detected_ArUco_markers)
	## return: image namely img after marking the aruco as per the instruction given in problem statement

    ## enter your code here ##
    
	for (markerCorner, markerId) in Detected_ArUco_markers:
		vertices = markerCorner.reshape(4, 2)
		topLeft, topRight, bottomRight, bottomLeft = markerCorner
		topRight = (int(topRight[0]), int(topRight[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		print(topLeft, topRight, bottomLeft, bottomRight)
		draw_borders(img, markerCorner, (255, 0, 0))
		ccd = get_corner_colour_dict(markerCorner)
		draw_corner_dots(img, ccd)
		cX, cY = draw_centroid(img, markerCorner, (0, 255, 0))
		draw_center_to_midpt_line(img, cX, cY, markerCorner, (100, 200, 130)) 

	return img

