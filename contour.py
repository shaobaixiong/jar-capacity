import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from operator import itemgetter
import math
import statistics
import csv

def locate_row(id):
    with open('C:\\Users\\16130\\Desktop\\jar capacity\\xuebu_db.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            if row["Code"] == id:
                return float(row["height"]), float(row["scale bar length"])

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
    cv.namedWindow('input',cv.WINDOW_NORMAL)
    cv.resizeWindow('input', 600,600)
    cv.imshow("input",contour_img)
    cv.imwrite("C:\\Users\\16130\\Desktop\\jar capacity\\contour_repository\\contour_" + no_test + ".jpg", contour_img)
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
    plt.savefig("C:\\Users\\16130\\Desktop\\jar capacity\\scatter_repository\\plot_" + no_test + ".jpg")
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

#set global variables
no_test = "JXSJD1Q2-7"
height, scale_exact_length = locate_row(no_test)
file_path = cv.imread("C:\\Users\\16130\\Desktop\\jar capacity\\jar_repository\\" + no_test +".jpg")

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
    #manual_remove(x,y)
    cleaned_x = []
    cleaned_y = []
    for point in j_x_y_list:
        cleaned_x.append(point[0])
        cleaned_y.append(point[1])
    draw_scatter_plot(cleaned_x, cleaned_y)

    r_list = measuring_radius(cleaned_x, middle_line, scale_exact_length, ratio)
    volume = "{:.2f}".format((math.pi * ((sum(r_list)/len(r_list))**2) * height) / 1000)
    estimated_height = "{:.2f}".format(ratio * (max(cleaned_y) - min(cleaned_y)))
    accuracy_rate = ((height - float(estimated_height)) / height) * 100
    print("{:.2f}".format(accuracy_rate), "%")
    print("The estimated height is", estimated_height, ";" , "the exact height is", height, ".")
    print("The volume of the jar is approximately", volume, "L")
