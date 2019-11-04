import cv2 as cv
import numpy as np

KERNEL_SIZE = 3
DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/4c3n.jpg'

def count_coins_and_bills_in_image(filename):
	bgr_img = cv.imread(filename)
	img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY)
	# cv.imshow('Original Image', img)

	# Tratando tamanho da imagem
	img = cv.resize(img,None,fx=0.25,fy=0.25)
	cv.imshow('Resized Original Image', img)

	# Binarizando valores de intensidade
	adaptive_gaussian_thr = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

	# Usando morfologia matemática para deixar os objetos mais bem definidos
	kernel = cv.getStructuringElement(cv.MORPH_CROSS, (KERNEL_SIZE, KERNEL_SIZE))

	opening = cv.morphologyEx(adaptive_gaussian_thr, cv.MORPH_OPEN, kernel)
	closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
	median_blur = cv.medianBlur(closing, 5)
	median_blur2 = cv.medianBlur(median_blur, 5)

	dilation = cv.dilate(median_blur2, kernel, iterations = 1)
	opening2 = cv.morphologyEx(dilation, cv.MORPH_OPEN, kernel)


	cv.imshow('0.0 - Adaptive Gaussian Thresholding', adaptive_gaussian_thr)
	cv.imshow('0.1 - Opening', opening)
	cv.imshow('0.2 - Closing', closing)
	cv.imshow('0.3 - Median Blur', median_blur)
	cv.imshow('0.4 - Median Blur again', median_blur2)
	cv.imshow('0.5 - Dilation', dilation)
	cv.imshow('0.6 - Opening again', opening2)

	####
	# Extraindo bordas

	edges = cv.Canny(median_blur, 100, 200)

	cv.imshow('1.0 - Canny Edge Detection', edges)

	####
	# findContours (liga os pontos de mesma intensidade que estão próximos)
	contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	img_with_drawn_contours = cv.drawContours(opening2, contours, -1, (0,255,0), 3)
	cv.imshow('2.0 - Finding Contours', img_with_drawn_contours)
	
	####
	# Diferindo por formato
	circles = cv.HoughCircles(img_with_drawn_contours, cv.HOUGH_GRADIENT, 0.9, 120, param1=50, param2=30, minRadius=60, maxRadius=0)
	
	if circles is not None:
		print('Circles isnt none!')
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		
		# Antes de desenhar os círculos, voltando imagem para BGR
		img_with_drawn_contours = cv.cvtColor(img_with_drawn_contours, cv.COLOR_GRAY2BGR)

		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv.circle(img_with_drawn_contours, (x, y), r, (0, 255, 0), 5)
	
	cv.imshow('3.0 - Drawn circles', img_with_drawn_contours)
	# print(f'{len(circles)} moedas foram encontradas na imagem.')

	cv.waitKey(0)
	cv.destroyAllWindows()

if __name__ == "__main__":
	count_coins_and_bills_in_image(DEFAULT_INPUT_IMG_PATH)