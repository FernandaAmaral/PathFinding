from matplotlib import pyplot as plt
import numpy as np
import cv2
import sys
import os

# Macros
IMAGE = True
GRAPH = False
ORIGIN = [415, 260]
DESTINATION = [1000, 815]

# Methods
def img_plot(img_title, image, img_type):
	plt.figure()
	if (img_type):
		plt.imshow(image, cmap = 'gray')
		plt.title(img_title)
	else:
		plt.plot(image, 'go')
		plt.title(img_title)


def histogram_calc(image):
	img_height = np.shape(image)[0]
	img_width = np.shape(image)[1]
	prob_level = [0] * 256

	# Calculate the number of occurrence of each gray level
	for i in range(0, img_height):
		for j in range(0, img_width):
			prob_level[image[i][j]] += 1

	# Divide for the total number of pixels to normalize probability of occurrence 
	return np.true_divide(prob_level , img_height*img_width)


def transformation_function_calc(img_histogram):
	sk = [0] * 256
	for k in range (0,256):
		for j in range(0,k+1):
			sk[k] +=  img_histogram[j]
		sk[k]*=255
	return sk


def img_equalize(transform_function, original_img):
	img_height = np.shape(original_img)[1]
	img_width = np.shape(original_img)[0]
	equalized_img = [[0 for x in range(img_width)] for y in range(img_height)] 

	# Replace original_img pixels by transform function mapping values
	for i in range(0, img_height):
		for j in range(0, img_width):
			equalized_img[i][j] = int(round(transform_function[original_img[j][i]])) 
	return equalized_img


def euclidean_dist(pixel_x, pixel_y):
	return ((pixel_x - DESTINATION[1])**2 + (pixel_y-DESTINATION[0])**2) ** 0.5


def mapping(desired_index):
	i=0
	map_matrix = [[0 for x in range(2)] for y in range(10)] 

	for x in range(-1, 2):
		for y in range(-1, 2):
			map_matrix[i][1] = x
			map_matrix[i][0] = y
			i += 1
	return map_matrix[desired_index]


def look_4_path(image):
	current_pixel = ORIGIN
	distances = [0] * 9
	nearest_values = [0] * 3
	trajectory = []

	while(current_pixel != DESTINATION):
		i=0

		# Find euclidean distance from each neighbour to destination
		for x in range(-1, 2):
			for y in range(-1, 2):
				distances[i] = euclidean_dist(current_pixel[1]+x , current_pixel[0]+y)
				i+=1

		# Get the index order of the nearest ones 
		nearest = sorted(range(len(distances)), key=lambda k: distances[k])

		# Get the grayscale value of the 3 nearest neighbours (based on euclidean distance)
		for i in range(0,3):
		  	nearest_values[i] = image[np.add(current_pixel[1], mapping(nearest[i])[1])][np.add(current_pixel[0], mapping(nearest[i])[0])]

		# Find the index of the winner pixel (the one with smaller grayscale value)
		winner = nearest[sorted(range(len(nearest_values)), key=lambda k: nearest_values[k])[0]]

		# Update current pixel and append it to the trajectory array
		current_pixel = [np.add(current_pixel[0], mapping(winner)[0]), np.add(current_pixel[1], mapping(winner)[1])]
		trajectory.append(current_pixel)

	return trajectory


def draw_trajectory(image, trajectory):
	size = np.shape(trajectory)[0]
	i=0
	for i in range(0, size-1):
		cv2.line(image, (trajectory[i][0],trajectory[i][1]), (trajectory[i+1][0],trajectory[i+1][1]), (255,0,0), 5)
	return image
						
#####################  Assignment 1: In the search for supplies  #####################


#Load an color image 
fileDir = os.path.dirname(os.path.abspath(__file__))
Mrgb = cv2.imread(fileDir + '/Mars.bmp')
img_height = Mrgb.shape[0]
img_width = Mrgb.shape[1]
Mgray = [[0 for x in range(img_height)] for y in range(img_width)] 

# Convert to grayscale
for i in range(0, img_height):
	for j in range(0, img_width):
		Mgray[j][i]=int(round(Mrgb.item(i,j,0)*0.114 +  Mrgb.item(i,j,1)*0.587 + Mrgb.item(i,j,2)*0.299));

# Get histogram of Mgray and transformation function
grayscale_histogram = histogram_calc(Mgray)
transformation_function = transformation_function_calc(grayscale_histogram)
Mheq = img_equalize(transformation_function, Mgray)
equalized_histogram = histogram_calc(Mheq)
cumulative_prob = transformation_function_calc(equalized_histogram)
trajectory = look_4_path(Mheq)
Mrgb_trajectory = draw_trajectory(Mrgb, trajectory)

# Save

cv2.imwrite(fileDir + '/Mars_final.bmp',Mrgb_trajectory);

# Plots

# img_plot('Original Image', Mrgb, IMAGE)
# img_plot('Greyscale Image', zip(*Mgray), IMAGE)
# img_plot('Equalized Image', Mheq, IMAGE)

# img_plot('Grayscale Histogram', grayscale_histogram, GRAPH)
# img_plot('Transformation Function', transformation_function, GRAPH)
# img_plot('Equalized Histogram', equalized_histogram, GRAPH)
# img_plot('Cumulative Probability after equalization', cumulative_prob, GRAPH)

img_plot('Trajectory', Mrgb_trajectory, IMAGE)

plt.show()
