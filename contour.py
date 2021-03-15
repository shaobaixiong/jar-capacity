import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from operator import itemgetter
import math
import statistics

#ps里面的线条0.035cm既可，太粗的话内部线条也会被识别。

no_test = "5"

file_path = cv.imread("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\test"+ no_test +".jpg")

def contour_detection(file_path):
    gray = cv.cvtColor(file_path, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    no_contours_detected = len(contours)
    if no_contours_detected == 2:
        return contours
    elif no_contours_detected < 2:
        print("Less than two contours detected; check this error.")
        return "error"
    else:
        print("More than two contours detected; check this error")
        return "error"

def contour_area(contours):
        area1 = cv.contourArea(contours[0])
        area2 = cv.contourArea(contours[1])
        if area1 > area2:
            return area1, area2, 0, 1
        else:
            return area2, area1, 1, 0

def contour_display(file_path, contours, contour_index):
    contour_img = cv.drawContours(file_path, contours, contour_index, (0,255,0), 3)
    cv.imshow("input",contour_img)
    cv.imwrite("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\contour" + no_test + ".jpg", contour_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def generate_coordinates_lists(contours, contour_index):
    x_list = []
    y_list = []
    x_y_list = []
    for point in contours[contour_index]:
        list_point = point[0].tolist()
        x_y_list.append(list_point)
        x_list.append(list_point[0])
        y_list.append(list_point[1])
    return x_list, y_list, x_y_list
    #print(x_list)
    #print(y_list)
    #print(x_y_list)

def draw_scatter_plot(x_list, y_list):
    plt.scatter(x_list, y_list, s=1)
    plt.title('Contour of Jar', fontsize=24)
    plt.xlabel('X', fontsize=14)
    plt.ylabel('Y', fontsize=14)
    x_lim = ((max(x_list)/100) + 1) * 100
    y_lim = ((max(y_list)/100) + 1) * 100
    plt.xlim(0, x_lim)
    plt.ylim(0, y_lim)
    plt.gca().set_aspect('equal', adjustable='box')
    #plt.savefig("C:\\Users\\16130\\Desktop\\jar capacity\\cv_test\\fig" + no_test + ".jpg")
    plt.show()

def length(x_list):
    pixel_length = max(x_list) - min(x_list)
    return pixel_length

def remove_redundant(value):
    point_list = []
    for point in j_x_y_list:
        if point[1] == value:
            point_list.append(point)
            j_x_y_list.remove(point)
    x_list = []
    for point in point_list:
        x_list.append(point[0])
    x_list.sort()
    j_x_y_list.append([x_list[0], value])
    return j_x_y_list

def manual_remove(x,y):
    j_x_y_list.remove([x,y])
    return j_x_y_list

def measuring_radius(cleaned_x, middle_line, scale_exact_length, ratio):
    list = []
    for x_value in cleaned_x:
        diameter = ratio * (middle_line - x_value)
        list.append(diameter)
    return list

scale_exact_length = 18

contours = contour_detection(file_path)
area_jar, area_scale, j_contour_index, s_contour_index = contour_area(contours)
if contours != "error":
    contour_display(file_path, contours, j_contour_index)
    j_x_list, j_y_list, j_x_y_list = generate_coordinates_lists(contours, j_contour_index)
    s_x_list, s_y_list, s_x_y_list = generate_coordinates_lists(contours, s_contour_index)
    draw_scatter_plot(j_x_list, j_y_list)
    scale_pixel_length = length(s_x_list)
    ratio = scale_exact_length/scale_pixel_length
    middle_line = max(j_x_list)

    for y_value in j_y_list:
        j_x_y_list = remove_redundant(y_value)
    manual_remove(261, 20)
    manual_remove(170, 527)
    cleaned_x = []
    cleaned_y = []
    for point in j_x_y_list:
        cleaned_x.append(point[0])
        cleaned_y.append(point[1])
    draw_scatter_plot(cleaned_x, cleaned_y)

    r_list = measuring_radius(cleaned_x, middle_line, scale_exact_length, ratio)
    volume = (math.pi * ((sum(r_list)/len(r_list))**2) * 46) / 1000
    print("The volume of the jar is,", volume, "L")




    #cleaned_y.sort()
    #j_x_y_list.sort(key=itemgetter(1))


    #sorted_x = []
    #for point in j_x_y_list:
    #    sorted_x.append(point[0])
    #print(sorted_x)
    #print(cleaned_y)
'''

def determine_num_groups(sorted_x):
    b = math.floor(len(sorted_x) / 3)
    a = len(sorted_x) / 3
    if a - b == 0:
        return b
    else:
        b = len(sorted_x) % math.floor(a)
        if b == 1:
            return b-1
        else:
            return b

def division(list, num):
    average = len(list) / num
    result = []
    last = 0
    while last < len(list):
        result.append(list[int(last):int(last + average)])
        last += average
    return result
'''

#num = determine_num_groups(sorted_x)
#divided_lists = division(sorted_x, num)
#for list in divided_lists:
#    print(list)
#    print(max(list)-min(list))
