import cv2 as cv
import numpy as np

MATH_MORPH_KERNEL_SIZE = 3
BLUR_KERNEL_SIZE = 11
DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/0c2n-3.jpg'
# DEFAULT_INPUT_IMG_PATH = './notas-e-moedas-exemplo/6c3n.jpg'

def calculate_area_of_rect(rect):
    return rect[1][0] * rect[1][1]

def calculate_rect_ratio(rect):
    width = rect[1][0]
    height = rect[1][1]
    if width > height:
        return width / height
    else:
        return height / width

def count_coins_and_bills_in_image(filename, show_steps=False):
    bgr_img = cv.imread(filename, 1)
    img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY)

	# Tratando tamanho da imagem para ser visualizável enquanto é feito o tuning dos parâmetros
    img = cv.resize(img,None,fx=0.25,fy=0.25)
    resized_img = img.copy()
    if show_steps:
        cv.imshow('Resized Original Image', img)

    # Utilizando blur para amenizar detalhes internos das notas e moedas como números de desenhos
    img = cv.GaussianBlur(img, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), cv.BORDER_DEFAULT)
    if show_steps:
        cv.imshow('0.0 - Gaussian Blur', img)

    # Aplicando transformada de hough para encontrar círculos na imagem
    all_circles_found = cv.HoughCircles(img, cv.HOUGH_GRADIENT, dp=0.9, minDist=120, param1=10, param2=40, minRadius=30, maxRadius=60)

    # Encontrando círculos que serão considerados como moedas
    coins_in_image = 0
    if all_circles_found is not None:
        all_circles_found_rounded = np.uint16(np.around(all_circles_found))
        for circle in all_circles_found_rounded[0, :]:
            # Desenhando círculo na imagem original
            cv.circle(resized_img, (circle[0], circle[1]), circle[2], (0, 255, 0), 5)
            # Cada círculo conta como uma moeda
            coins_in_image += 1
        if show_steps:
            cv.imshow('Drawn circles', resized_img)

	# Binarizando valores de intensidade
    img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
    if show_steps:
        cv.imshow('0.0 - Adaptive Gaussian Thresholding', img)

    # Definindo kernel que será utilizado nas operações de morfologia matemática
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (MATH_MORPH_KERNEL_SIZE, MATH_MORPH_KERNEL_SIZE))	

    # Realizando fechamento para fechar fendas que surgem principalmente nas notas,
    #  evitando que fiquem separadas e cause com que não consigamos transformar
    # essas partes no "blob" da nota
    img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel, iterations=5)
    if show_steps:
        cv.imshow('0.2 - Closing', img)
	
    # Dilatando as pequenas partes que compõe cada nota para que se juntem e eventualmente
    # seja possível identificar os retângulos das notas
    img = cv.dilate(img, kernel, iterations = 12)
    if show_steps:
        cv.imshow('0.5 - Dilation', img)
	
    bills_in_image = 0

	# Encontrando os contours (liga os pontos de mesma intensidade que estão próximos)
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)    

    for contour in contours:
        # Achando os retângulos que possivelmente são uma nota
        rect = cv.minAreaRect(contour)
        rect_area = calculate_area_of_rect(rect)
        rect_ratio = calculate_rect_ratio(rect)

        # Assumindo por critério de área e ratio do retângulo se ele é uma nota ou não
        if (rect_area > 90000) and 1.2 < rect_ratio < 2.0:
            # Criando bounding box correspondente para poder desenhar na imagem
            box = cv.boxPoints(rect)
            box = np.int0(box)
            resized_img = cv.drawContours(resized_img, [box], 0, (0, 255, 0), 3)
            bills_in_image += 1
    
    if show_steps:
        cv.imshow(f'Coins and bills: {filename}', resized_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    return coins_in_image, bills_in_image

if __name__ == "__main__":
	count_coins_and_bills_in_image(DEFAULT_INPUT_IMG_PATH, show_steps=True)