#!/usr/bin/env python3
############## Task1.1 - ArUco Detection ##############

import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time

def get_corner_colour_dict(tl, tr, br, bl):
	d = {tr: (0,255,0), tl: (125,125,125), br: (180,105,255), bl: (255,255,255)}
	return d
	
def calculate_centroid(topLeft, topRight, bottomRight, bottomLeft):
	cX = int((topLeft[0] + bottomRight[0]) / 2.0)
	cY = int((topLeft[1] + bottomRight[1]) / 2.0)
	return cX, cY
	
def calculate_midpoint(topLeft, topRight):
	mpX, mpY= (topRight[0] + topLeft[0])//2 , (topRight[1] + topLeft[1])//2
	return mpX, mpY

def draw_corner_dots(img, ccd):
	for i in ccd:
		cv2.circle(img, i, 2, ccd[i], 5)
	
def draw_centroid(img, topLeft, topRight, bottomRight, bottomLeft, colour):
	cX = int((topLeft[0] + bottomRight[0]) / 2.0)
	cY = int((topLeft[1] + bottomRight[1]) / 2.0)
	cv2.circle(img, (cX, cY), 4, colour, -1)
	return cX, cY
	
def draw_center_to_midpt_line(img, cX, cY, topRight, topLeft, colour):
	mpX, mpY= (topRight[0] + topLeft[0])//2 , (topRight[1] + topLeft[1])//2
	cv2.line(img, (cX, cY), (mpX, mpY), colour, 2)
	
def put_text(img, text, coordinates, color):

	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 1
	thickness = 2
	   
	cv2.putText(img, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)

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


def Calculate_orientation_in_degree(Detected_ArUco_markers):
	
	ArUco_marker_angles = {}
	for (markerId) in Detected_ArUco_markers:
		vertices = Detected_ArUco_markers[markerId].reshape(4, 2)
		topLeft, topRight, bottomRight, bottomLeft = vertices
		mpX, mpY = calculate_midpoint(topLeft, topRight)
		cX, cY = calculate_centroid(topLeft, topRight, bottomRight, bottomLeft)
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
		ArUco_marker_angles[markerId] = round(angle)
	
	return ArUco_marker_angles	

def mark_ArUco(img, Detected_ArUco_markers, ArUco_marker_angles):
    
	for (markerId) in Detected_ArUco_markers:
		vertices = Detected_ArUco_markers[markerId].reshape(4, 2)
		topLeft, topRight, bottomRight, bottomLeft = vertices
		topRight = (int(topRight[0]), int(topRight[1]))
		topLeft = (int(topLeft[0]), int(topLeft[1]))
		bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
		ccd = get_corner_colour_dict(topLeft, topRight, bottomRight, bottomLeft)
		draw_corner_dots(img, ccd)
		cX, cY = draw_centroid(img, topLeft, topRight, bottomRight, bottomLeft, (0, 0, 255))
		draw_center_to_midpt_line(img, cX, cY, topLeft, topRight, (255,0,0)) 
		
		put_text(img, str(ArUco_marker_angles[markerId]), (cX-130, cY-10), (0,255,0))
		put_text(img, str(markerId), (cX+20, cY-10), (0,0, 255))
	return img
