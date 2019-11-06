import cv2 as cv
import numpy as np

KERNEL_SIZE = 3
DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/4c3n.jpg'

def count_coins_and_bills_in_image(filename):
    bgr_img = cv.imread(filename, 1)
    img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY)
	# cv.imshow('Original Image', img)

	# Tratando tamanho da imagem
    img = cv.resize(img,None,fx=0.25,fy=0.25)
    resized_img = img.copy()
    cv.imshow('Resized Original Image', img)

	# Achando moedas
    img = cv.GaussianBlur(img, (21, 21), cv.BORDER_DEFAULT)
    cv.imshow('0.0 - Gaussian Blur', img)

    all_circs = cv.HoughCircles(img, cv.HOUGH_GRADIENT, dp=0.9, minDist=120, param1=10, param2=40, minRadius=30, maxRadius=60)

    coins_in_image = 0
    if all_circs is not None:
        print('there are circles!')
        all_circs_rounded = np.uint16(np.around(all_circs))
        print(f'all_circs_rounded: {all_circs_rounded}')
        for i in all_circs_rounded[0, :]:
            cv.circle(resized_img, (i[0], i[1]), i[2], (50, 200, 200), 5)
            coins_in_image += 1
        cv.imshow('Drawn circles', resized_img)
        
    else:
        print('no circles')

    return coins_in_image, 0

	# Binarizando valores de intensidade
    # img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    # cv.imshow('0.0 - Adaptive Gaussian Thresholding', img)

	# Usando morfologia matemática para deixar os objetos mais bem definidos
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (KERNEL_SIZE, KERNEL_SIZE))	
	# kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

	# img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
	# cv.imshow('0.1 - Opening', img)

    # img = cv.erode(img, kernel, iterations = 1)
    # cv.imshow('TESTE - erode', img)

    # img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel, iterations=2)
    # cv.imshow('0.2 - Closing', img)
	
    # img = cv.medianBlur(img, 3)
    # cv.imshow('0.3 - Median Blur', img)
    # img = cv.medianBlur(img, 3)
    # cv.imshow('0.4 - Median Blur again', img)

	# img = cv.dilate(img, kernel, iterations = 1)
	# cv.imshow('0.5 - Dilation', img)
	# img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
	# cv.imshow('0.6 - Opening again', img)
	
	####
	# Extraindo bordas

	# img = cv.Canny(img, 100, 200)
	# cv.imshow('1.0 - Canny Edge Detection', img)

	####
	# findContours (liga os pontos de mesma intensidade que estão próximos)
	# contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
	# img = cv.drawContours(img, contours, -1, (0,255,0), 3)
	# cv.imshow('2.0 - Finding Contours', img)
	
	###
	# Diferindo por formato


    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
	count_coins_and_bills_in_image(DEFAULT_INPUT_IMG_PATH)