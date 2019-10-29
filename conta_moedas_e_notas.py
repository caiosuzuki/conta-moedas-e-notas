import cv2 as cv

KERNEL_SIZE = 3
INPUT_IMG_PATH = './notas-e-moedas-exemplo/5c2n.jpg'

img = cv.imread(INPUT_IMG_PATH, 0)
# cv.imshow('Original Image', img)

# Tratando tamanho da imagem
img = cv.resize(img,None,fx=0.25,fy=0.25)
cv.imshow('Resized Original Image', img)

# Binarizando valores de intensidade
adaptive_gaussian_thr = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

kernel = cv.getStructuringElement(cv.MORPH_CROSS, (KERNEL_SIZE, KERNEL_SIZE))

opening = cv.morphologyEx(adaptive_gaussian_thr, cv.MORPH_OPEN, kernel)
closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
median_blur = cv.medianBlur(closing, 5)
median_blur2 = cv.medianBlur(median_blur, 5)
# começou a dar ruim
dilation = cv.dilate(median_blur2, kernel, iterations = 1)
opening2 = cv.morphologyEx(dilation, cv.MORPH_OPEN, kernel)


cv.imshow('0.0 - Adaptive Gaussian Thresholding', adaptive_gaussian_thr)
cv.imshow('0.1 - Opening', opening)
cv.imshow('0.2 - Closing', closing)
cv.imshow('0.3 - Median Blur', median_blur)
cv.imshow('0.4 - Median Blur again', median_blur2)
cv.imshow('0.5 - Dilation', dilation)
cv.imshow('0.6 - Opening again', opening2)

###########
# Extraindo bordas

edges = cv.Canny(opening2, 100, 200)

cv.imshow('1.0 - Canny Edge Detection', edges)

####
# findContours (liga os pontos de mesma intensidade que estão próximos)
contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
img_with_drawn_contours = cv.drawContours(opening2, contours, -1, (0,255,0), 3)
cv.imshow('2.0 - Finding Contours', img_with_drawn_contours)

####
# Diferindo por formato

cv.waitKey(0)
cv.destroyAllWindows()