from operator import itemgetter
from cv2 import boundingRect, exp
import numpy as np
from pytesseract import pytesseract
import cv2
import pandas as pd

def expand(bbox, margin=10):
    # supose bbox is x1, y1, x2, y2
    return [
        bbox[0] - margin,
        bbox[1] - margin,
        bbox[2] + margin,
        bbox[3] + margin]

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

file = r'./2022-04-03/Grandview Theater Lodge.png'
im = cv2.imread(file)
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
cols = im.shape[1]
horizontal_size = cols // 45
ret, thresh = cv2.threshold(gray, 127, 255, 0)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
# Applying dilation and erosion on the threshold image to find horizontal lines
# Erosion finds min value over kernel
horizontal = cv2.erode(thresh, rect_kernel)
# Dilation finds max value over kernet
horizontal = cv2.dilate(horizontal, rect_kernel, iterations = 1)
contours, hierarchy = cv2.findContours(horizontal, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
bounding_boxes = [cv2.boundingRect(c) for c in contours]
bounding_boxes = sorted(bounding_boxes, key=itemgetter(1,0))
bounding_boxes = bounding_boxes[1:]
for bounding_box in bounding_boxes:     
    # Drawing a rectangle on copied image
    x, y, w, h = expand(bounding_box)
    rect = cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    # Cropping the text block for giving input to OCR
    cropped = im[y:y + h, x:x + w]
    # Apply OCR on the cropped image
    # text = pytesseract.image_to_string(cropped)
# Sort the contours by y-value
cv2.imshow('img', im)
cv2.waitKey(0)