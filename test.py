import cv2 as cv
import numpy as np

MATH_MORPH_KERNEL_SIZE = 3
BLUR_KERNEL_SIZE = 11
DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/0c2n-3.jpg'
# DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/6c3n.jpg'

def calculateAreaOfRect(rect):
    return rect[1][0] * rect[1][1]

def calculateRectRatio(rect):
    width = rect[1][0]
    height = rect[1][1]
    if width > height:
        return width / height
    else:
        return height / width

def count_coins_and_bills_in_image(filename, show_steps=False):
    bgr_img = cv.imread(filename, 1)
    img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY)

	# Tratando tamanho da imagem
    img = cv.resize(img,None,fx=0.25,fy=0.25)
    resized_img = img.copy()
    if show_steps:
        cv.imshow('Resized Original Image', img)

	# Achando moedas
    img = cv.GaussianBlur(img, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), cv.BORDER_DEFAULT)
    if show_steps:
        cv.imshow('0.0 - Gaussian Blur', img)

    all_circles_found = cv.HoughCircles(img, cv.HOUGH_GRADIENT, dp=0.9, minDist=120, param1=10, param2=40, minRadius=30, maxRadius=60)

    coins_in_image = 0
    if all_circles_found is not None:
        all_circles_found_rounded = np.uint16(np.around(all_circles_found))
        for i in all_circles_found_rounded[0, :]:
            cv.circle(resized_img, (i[0], i[1]), i[2], (50, 200, 200), 5)
            coins_in_image += 1
        if show_steps:
            cv.imshow('Drawn circles', resized_img)

	# Binarizando valores de intensidade
    # faz parte da estrutura final
    img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
    if show_steps:
        cv.imshow('0.0 - Adaptive Gaussian Thresholding', img)

	# Usando morfologia matemática para deixar os objetos mais bem definidos
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (MATH_MORPH_KERNEL_SIZE, MATH_MORPH_KERNEL_SIZE))	

    # img = cv.erode(img, kernel, iterations = 1)
    # cv.imshow('TESTE - erode', img)

    # faz parte da estrutura final
    img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel, iterations=5)
    if show_steps:
        cv.imshow('0.2 - Closing', img)
	
    # faz parte da estrutura final
    img = cv.dilate(img, kernel, iterations = 12)
    if show_steps:
        cv.imshow('0.5 - Dilation', img)
	
	####
    # Achando notas
    bills_in_image = 0
    # img = cv.Canny(img, 100, 200)
    # cv.imshow('1.0 - Canny Edge Detection', img)

	####
	# findContours (liga os pontos de mesma intensidade que estão próximos)
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)    

    for contour in contours:
        rect = cv.minAreaRect(contour)
        rect_area = calculateAreaOfRect(rect)
        rect_ratio = calculateRectRatio(rect)
        if (rect_area > 90000) and 1.2 < rect_ratio < 2.0:
            box = cv.boxPoints(rect)
            # transformando float para int
            box = np.int0(box)
            resized_img = cv.drawContours(resized_img, [box], 0, (0,255,0), 3)
            bills_in_image += 1
    
    if show_steps or False:
        cv.imshow(f'Drawn contours - {filename}', resized_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    return coins_in_image, bills_in_image

if __name__ == "__main__":
	count_coins_and_bills_in_image(DEFAULT_INPUT_IMG_PATH, show_steps=True)