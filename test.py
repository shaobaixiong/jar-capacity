import cv2 as cv
import numpy as np

def get_image_info(image):
    print(type(image))
    print(image.shape)
    print(image.size)
    print(image.dtype)
    pixel_data = np.array(image)
    print(pixel_data)

file = cv.imread("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\test.jpg")
cv.imshow("input image", file)
get_image_info(file)
gray = cv.cvtColor(file, cv.COLOR_BGR2GRAY)
cv.imwrite("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\gray.jpg", gray)
cv.waitKey(0)

cv.destroyAllWindows()
