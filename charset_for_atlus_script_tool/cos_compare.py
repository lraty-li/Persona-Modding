# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2018/11/17 14:52
# @Author  : xhh
# @Desc    : 余弦相似度计算
# @File    : difference_image_consin.py
# @Software: PyCharm
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2 
 
# 对图片进行统一化处理
def get_thum(image, size=(64,64), greyscale=False):
    # 利用image对图像大小重新设置, Image.ANTIALIAS为高质量的
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        # 将图片转换为L模式，其为灰度图，其每个像素用8个bit表示
        image = image.convert('L')
    return image

def img2Vetor(image):
    ## TODO no thum?
    image = get_thum(image)
    vector = []
    for pixel_tuple in image.getdata():
        vector.append(np.average(pixel_tuple))
    # linalg=linear（线性）+algebra（代数），norm则表示范数
    # 求图片的范数？？
    norm = np.linalg.norm(vector, 2)
    if (norm == 0):
        raise Exception
    normedVetor = vector/norm
    return normedVetor

# def calcDistrance(vec1, vec2):
    
# 计算图片的余弦距离
def image_similarity_vectors_via_numpy(image1, image2):
    # image1 = get_thum(image1)
    # image2 = get_thum(image2)
    images = [image1, image2]
    vectors = []
    norms = []
    a = img2Vetor(image1)
    b = img2Vetor(image2)
    # for image in images:
    #     vector = img2Vetor(image)
    #     vectors.append(vector)

    #     norms.append(np.linalg.norm(vector, 2))
    # a, b = vectors
    # a_norm, b_norm = norms
    # dot返回的是点积，对二维数组（矩阵）进行计算
    res = np.dot(a, b)

    # np.save("temp.npy", {"a":b},  allow_pickle=True)
    # tryLoad = np.load("temp.npy", allow_pickle=True)
    return res
 
    """
    9721 啊
    13896 料
    25537 (啊形近字)
    """
if __name__ == "__main__":
    p1="./font_img_dfyuanlightbold/ya.png"
    # p1="./font_img/20886.png"
    p2="../cropped/7512.png"

    source = "../FONT0.PNG"
 
    image1 = Image.open(p1)
    image2 = Image.open(p2)
    # image3 = Image.open(source)

    plt.subplot(121)
    plt.imshow(image1)
    plt.subplot(122)
    plt.imshow(image2)
    cosin = image_similarity_vectors_via_numpy(image1, image2)
    print('图片余弦相似度',cosin)
    plt.show()

    # image2cv =cv2.imread(p1)
    # cv2.imshow('rgb image',image2cv) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()
