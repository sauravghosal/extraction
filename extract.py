import argparse
from operator import itemgetter
import cv2
import numpy as np
import pandas as pd
from pytesseract import pytesseract

def expand(bbox, marginX=15, marginY=10):
    # suppose bbox is x, y, w, h
    return [
        bbox[0] - marginX,
        bbox[1] - marginY,
        bbox[2] + marginX,
        bbox[3] + marginY]

def extract_data(in_file=r'./2022-04-03/Grandview Theater Lodge.png', out_file=r"./out.xlsx", show_bounding_boxes=True, columns=11):
	im = cv2.imread(in_file)
	im = im[150:, :]
	gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	horizontal_size = im.shape[1] // 40
	vertical_size = im.shape[0] // 45
	_, thresh = cv2.threshold(gray, 127, 255, 0)
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, vertical_size))
	
 	# Applying dilation and erosion on the threshold image to find horizontal lines
	# Erosion finds min value over kernel
	horizontal = cv2.erode(thresh, rect_kernel)
	# Dilation finds max value over kernel
	horizontal = cv2.dilate(horizontal, rect_kernel, iterations = 1)
 
	# Finding boxes around text
	contours, _ = cv2.findContours(horizontal, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	bounding_boxes = [cv2.boundingRect(c) for c in contours]
 
	# Sort the bounding boxes by y value
	bounding_boxes = sorted(bounding_boxes[:-1], key=itemgetter(1))
	
 	# TODO extract the number of columns (and rows if possible) from the image instead of hardcoding 
	# 11 columns (dynamic based on cabin age), 14 rows for default GrandView Theatre Lodge
	# sort each row according to x value 
	for i in range(0, len(bounding_boxes), columns):
		bounding_boxes[i:i+columns] = sorted(bounding_boxes[i:i+columns], key=itemgetter(0))

	data = []
	for bounding_box in bounding_boxes:     
		# Drawing a rectangle on image
		x, y, w, h = expand(bounding_box)
		cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		# Cropping the text block for giving input to OCR
		cropped = im[y:y + h, x:x + w]
	
		# Apply OCR on the cropped image
		text = pytesseract.image_to_string(cropped)
	
		data.append(text)
	
	data = [tuple(data[i:i+columns]) for i in range(0, len(data), columns)]
	df = pd.DataFrame.from_records(data[1:], columns=data[0])
	df.to_excel(out_file)
 
	if show_bounding_boxes:
		cv2.imshow('img', im)
		cv2.waitKey(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use OCR to convert extract data from cabin performance report.")
    parser.add_argument('inFile', help="path to the report png", type=str)
    parser.add_argument('columns', help="number of columns in report table", type=int)
    parser.add_argument('outFile', help='path of the excel file to write to', type=str)
    parser.add_argument('-s', '--show-bounding-boxes', help='flag to show the report png with bounding boxes around text', action='store_true')
    args = parser.parse_args()
    extract_data(args.inFile, args.outFile, args.show_bounding_boxes, args.columns)