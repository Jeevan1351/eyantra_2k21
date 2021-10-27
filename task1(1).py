import numpy as np
import math
import cv2
import cv2.aruco as aruco

def get_corner_colour_dict(tr, tl, br, bl):
	d = {tr: (0,0,255), tl: (0,0,255), br: (0,0,255), bl: (0,0,255)}
	return d
def draw_corner_dots(img, ccd):
	for i in ccd:
		cv2.circle(img, i, 2, ccd[i], 5)

def draw_borders(img, topLeft, topRight, bottomRight, bottomLeft, colour):
	cv2.line(img, topLeft, topRight, colour, 2)
	cv2.line(img, topRight, bottomRight, colour, 2)
	cv2.line(img, bottomRight, bottomLeft, colour, 2)
	cv2.line(img, bottomLeft, topLeft, colour, 2)

def draw_centroid(img, topLeft, topRight, bottomRight, bottomLeft, colour):
	cX = int((topLeft[0] + bottomRight[0]) / 2.0)
	cY = int((topLeft[1] + bottomRight[1]) / 2.0)
	cv2.circle(img, (cX, cY), 4, colour, -1)
	return cX, cY

def draw_center_to_midpt_line(img, cX, cY, topRight, bottomRight, colour):
	mpX, mpY= (topRight[0] + bottomRight[0])//2 , (topRight[1] + bottomRight[1])//2
	cv2.line(img, (cX, cY), (mpX, mpY), colour, 2)


img = cv2.imread("test_image1.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
parameters = aruco.DetectorParameters_create()
corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
d = {}

if (len(corners) > 0):
	ids = ids.flatten()
	print(ids)

for (markerCorner, markerID) in zip(corners, ids):
	corners = markerCorner.reshape(4, 2)
	topLeft, topRight, bottomRight, bottomLeft = corners
	topRight = (int(topRight[0]), int(topRight[1]))
	bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
	bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	topLeft = (int(topLeft[0]), int(topLeft[1]))
	draw_borders(img, topLeft, topRight, bottomRight, bottomLeft, (255, 0, 0))
	ccd = get_corner_colour_dict(topRight, topLeft, bottomRight, bottomLeft)
	draw_corner_dots(img, ccd)
	cX, cY = draw_centroid(img, topLeft, topRight, bottomRight, bottomLeft, (0, 255, 0))
	draw_center_to_midpt_line(img, cX, cY, topLeft, topRight, (100, 200, 130)) 
	
cv2.imshow("image", img)
cv2.waitKey()
    
