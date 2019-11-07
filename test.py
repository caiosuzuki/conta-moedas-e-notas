import cv2 as cv
import numpy as np

KERNEL_SIZE = 3
DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/4c3n.jpg'
# DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/0c3n.jpg'

def count_coins_and_bills_in_image(filename, show_steps=False):
    bgr_img = cv.imread(filename, 1)
    img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY)
	# cv.imshow('Original Image', img)

	# Tratando tamanho da imagem
    img = cv.resize(img,None,fx=0.25,fy=0.25)
    resized_img = img.copy()
    if show_steps:
        cv.imshow('Resized Original Image', img)

	# Achando moedas
    img = cv.GaussianBlur(img, (21, 21), cv.BORDER_DEFAULT)
    if show_steps:
        cv.imshow('0.0 - Gaussian Blur', img)

    all_circs = cv.HoughCircles(img, cv.HOUGH_GRADIENT, dp=0.9, minDist=120, param1=10, param2=40, minRadius=30, maxRadius=60)

    coins_in_image = 0
    if all_circs is not None:
        all_circs_rounded = np.uint16(np.around(all_circs))
        for i in all_circs_rounded[0, :]:
            cv.circle(resized_img, (i[0], i[1]), i[2], (50, 200, 200), 5)
            coins_in_image += 1
        if show_steps:
            cv.imshow('Drawn circles', resized_img)
        
    else:
        print('no circles')

    # return coins_in_image, 0

	# Binarizando valores de intensidade
    # faz parte da estrutura final
    img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
    if show_steps:
        cv.imshow('0.0 - Adaptive Gaussian Thresholding', img)

	# Usando morfologia matemática para deixar os objetos mais bem definidos
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (KERNEL_SIZE, KERNEL_SIZE))	

    # img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel, iterations=1)
    # cv.imshow('0.1 - Opening', img)

    # img = cv.erode(img, kernel, iterations = 1)
    # cv.imshow('TESTE - erode', img)

    # faz parte da estrutura final
    img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel, iterations=5)
    if show_steps:
        cv.imshow('0.2 - Closing', img)
	
    # img = cv.medianBlur(img, 3)
    # cv.imshow('0.3 - Median Blur', img)
    # img = cv.medianBlur(img, 3)
    # cv.imshow('0.4 - Median Blur again', img)

    # faz parte da estrutura final
    img = cv.dilate(img, kernel, iterations = 15)
    if show_steps:
        cv.imshow('0.5 - Dilation', img)
    # img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
    # cv.imshow('0.6 - Opening again', img)
	
	####
    # Achando notas
	# Extraindo bordas
    bills_in_image = 0
    # img = cv.Canny(img, 100, 200)
    # cv.imshow('1.0 - Canny Edge Detection', img)

	####
	# findContours (liga os pontos de mesma intensidade que estão próximos)
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)    
    print(f'qtde contours: {len(contours)}')
    
    for contour in contours:
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        resized_img = cv.drawContours(resized_img, [box], 0, (0,255,0), 3)
        print(type(box))
        # cv.drawContours(resized_img, contour, -1, (0, 255, 0), 3)
        # rectArea = ...
        # if rectArea > 85000 and rectArea < 110000:
        #     bills_in_image += 1
    
    print(f'bills in image: {bills_in_image}')
    if show_steps:
        cv.imshow('Drawn contours', resized_img)
	
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
	count_coins_and_bills_in_image(DEFAULT_INPUT_IMG_PATH, show_steps=True)