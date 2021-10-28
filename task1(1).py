import numpy as np
import cv2
import cv2.aruco as aruco
import math


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

def angle_finder(mpX, mpY, cX, cY):
	if mpX > cX:
		if mpY > cY:
			print(270+math.degrees(math.atan(abs((mpY-cY)/(mpX-cX)))))
		else:
			print(math.degrees(math.atan(abs((mpY-cY)/(mpX-cX)))))
	else:
		if mpY > cY:
			print(180+math.degrees(math.atan(abs((mpY-cY)/(mpX-cX)))))
		else:
			print(90+math.degrees(math.atan(abs((mpY-cY)/(mpX-cX)))))

def draw_center_to_midpt_line(img, cX, cY, topRight, bottomRight, colour):
	mpX, mpY= (topRight[0] + bottomRight[0])//2 , (topRight[1] + bottomRight[1])//2
	cv2.line(img, (cX, cY), (mpX, mpY), colour, 2)
	print(f"(({mpX}, {mpY}), ({cX}, {cY}))")
	height = img.shape[0]
	width = img.shape[1]
	angle_finder(mpX, mpY, cX, cY)

img_path = "./test_image2.png"

img = cv2.imread(img_path)
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
parameters = aruco.DetectorParameters_create()
corners, ids, _ = aruco.detectMarkers(grey, aruco_dict, parameters=parameters)
d = {}


if (len(corners) > 0):
	ids = ids.flatten()
	print("ids: ", ids)

for (markerCorner, markerId) in zip(corners, ids):
	vertices = markerCorner.reshape(4, 2)
	topLeft, topRight, bottomRight, bottomLeft = vertices
	topRight = (int(topRight[0]), int(topRight[1]))
	topLeft = (int(topLeft[0]), int(topLeft[1]))
	bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
	print(topLeft, topRight, bottomLeft, bottomRight)
	draw_borders(img, topLeft, topRight, bottomRight, bottomLeft, (255, 0, 0))
	ccd = get_corner_colour_dict(topRight, topLeft, bottomRight, bottomLeft)
	draw_corner_dots(img, ccd)
	cX, cY = draw_centroid(img, topLeft, topRight, bottomRight, bottomLeft, (0, 255, 0))
	draw_center_to_midpt_line(img, cX, cY, topLeft, topRight, (100, 200, 130)) 



cv2.imshow("image", img)
cv2.waitKey()
