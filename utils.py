import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image
import matplotlib
#matplotlib.use('TkAgg')

def to_image(img):
    image = Image.fromarray(img) 
    return image
    
def to_array(array):
    image = array.astype('uint8')
    image = Image.fromarray(image)
    return image

# 關於 中間 10*10 pixel
def pixel10(img):
    Y = img[251:261, 251:261]
    return Y

# raw圖片處理
def data_raw_img(path):
    img = np.fromfile(path, dtype='uint8')
    img = img.reshape(512,512)
    return img


# 對數變換、伽馬變換和圖像負片
def Log_tranfrom(c, img):     # 對數變換
    output = c*np.log(1+img)
    output = np.uint8(output+0.5)
    return output

def gamma_trans(img, gamma):  # gamma函式處理
    img = img.astype('uint8')
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  # 建立對映表
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  # 顏色值為整數
    gamma_table = cv2.LUT(img, gamma_table)
    gamma_table = np.asarray(gamma_table).astype('float')
    return gamma_table  # 圖片顏色查表。另外可以根據光強（顏色）均勻化原則設計自適應演算法。

# def gamma_trans(img, gamma):  # gamma函式處理
#     img = img/255
#     img = img**gamma
#     img = 255*img
#     return img  # 圖片顏色查表。另外可以根據光強（顏色）均勻化原則設計自適應演算法。

def negative_tranfrom(img):  # 圖像負片
    output = 255-img
    return output

def Bilinear_interpolation(new_size, img):
    dst_h, dst_w = new_size  #目標圖高寬
    img_h, img_w = img.shape[:2]  #原圖高寬
    scale_x = float(img_w)/dst_w  #x縮放比率
    scale_y = float(img_h)/dst_h
    
    dst = np.zeros((dst_h, dst_w), dtype = np.uint8)
    for dst_y in range(dst_h):
        for dst_x in range(dst_w):
            # 目標在原圖上的座標
            img_x = (dst_x +  0.5) * scale_x -0.5
            img_y = (dst_y +  0.5) * scale_y -0.5
            # 計算在原圖上四個鄰近點的位置
            img_x_0 = int(np.floor(img_x))
            img_y_0 = int(np.floor(img_y))
            img_x_1 = min(img_x_0 + 1, img_w -1)
            img_y_1 = min(img_y_0 + 1, img_h -1)
            
            # 雙線性差值
            value0 = (img_x_1 - img_x) * img[img_y_0, img_x_0] + (img_x - img_x_0) * img[img_y_0, img_x_1]
            value1 = (img_x_1 - img_x) * img[img_y_1, img_x_0] + (img_x - img_x_0) * img[img_y_1, img_x_1]
            dst[dst_y, dst_x] = int((img_y_1 - img_y) * value0 + (img_y - img_y_0) * value1)
    return dst

def Nearest_neighbor_interpolation(new_size, img):
    ratio_h = (img.shape[0]-1)/ (new_size[0]-1)
    ratio_w = (img.shape[1]-1)/ (new_size[1]-1)
    
    target_img = np.zeros((new_size))
    
    for tar_h in range(new_size[0]):
        for tar_w in range(new_size[1]):
            img_h = round(ratio_h*tar_h)
            img_w = round(ratio_w*tar_w)
            target_img[tar_h, tar_w] = img[img_h, img_w]
    return target_img
            