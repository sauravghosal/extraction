from operator import itemgetter
import cv2
import numpy as np
import pandas as pd
from pytesseract import pytesseract

def expand(bbox, marginX=15, marginY=10):
    # supose bbox is x, y, w, h
    return [
        bbox[0] - marginX,
        bbox[1] - marginY,
        bbox[2] + marginX,
        bbox[3] + marginY]

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
im = im[150:, :]
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
cols = im.shape[1]
rows = im.shape[0]
horizontal_size = cols // 40
vertical_size = rows // 45
ret, thresh = cv2.threshold(gray, 127, 255, 0)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, vertical_size))
# Applying dilation and erosion on the threshold image to find horizontal lines
# Erosion finds min value over kernel
horizontal = cv2.erode(thresh, rect_kernel)
# Dilation finds max value over kernet
horizontal = cv2.dilate(horizontal, rect_kernel, iterations = 1)
contours, hierarchy = cv2.findContours(horizontal, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
bounding_boxes = [cv2.boundingRect(c) for c in contours]
# Sort the contours by y value
bounding_boxes = sorted(bounding_boxes[:-1], key=itemgetter(1))
# TODO extract the number of columns (and rows if possible) from the image instead of hardcoding 

# 11 columns (dynamic based on cabin age), 14 rows
# sort each row according to x value 
for i in range(0, len(bounding_boxes), 11):
    bounding_boxes[i:i+11] = sorted(bounding_boxes[i:i+11], key=itemgetter(0))

data = []
for index, bounding_box in enumerate(bounding_boxes):     
	# Drawing a rectangle on image
	x, y, w, h = expand(bounding_box)
	rect = cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	# Cropping the text block for giving input to OCR
	cropped = im[y:y + h, x:x + w]
 
	# Apply OCR on the cropped image
	text = pytesseract.image_to_string(cropped)
 
	# Header row
	data.append(text)
 
data = [tuple(data[i:i+11]) for i in range(0, len(data), 11)]
df = pd.DataFrame.from_records(data[1:], columns=data[0])
df.to_excel('out.xlsx')
    
cv2.imshow('img', im)
cv2.waitKey(0)