import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

#ps里面的线条0.035cm既可，太粗的话内部线条也会被识别。

no_test = "5"

file = cv.imread("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\test"+ no_test +".jpg")
gray = cv.cvtColor(file, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

contour_img = cv.drawContours(file, contours, 0, (0,255,0), 3)
cv.imshow("input",contour_img)
cv.imwrite("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\contour" + no_test + ".jpg", contour_img)
cv.waitKey(0)
cv.destroyAllWindows()
'''
x_list = []
y_list = []
x_y_list = []
for point in contours[0]:
    list_point = point[0].tolist()
    x_y_list.append(list_point)
    x_list.append(list_point[0])
    y_list.append(list_point[1])
print(x_list)
print(y_list)
print(x_y_list)
plt.scatter(x_list, y_list)
plt.title('Contour of Jar', fontsize=24)
plt.xlabel('X', fontsize=14)
plt.ylabel('Y', fontsize=14)
x_lim = ((max(x_list)/100) + 1) * 100
y_lim = ((max(y_list)/100) + 1) * 100
plt.xlim(0, x_lim)
plt.ylim(0, y_lim)
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\fig" + no_test + ".jpg")
plt.show()
'''
