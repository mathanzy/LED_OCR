#-*- coding:utf-8 -*-
'''
通过pytesseract包进行图片中文字识别
'''

import ImageProcess.img_pre_process as ppro
import ImageProcess.img_process as pro
from PIL import Image
import get_images
import numpy as np
import pytesseract
import os

def word_in_picture(folderpath):
    # 导入图片
    raw_imagepath = os.path.join(folderpath,'LEDCapturePics\\ledVideCapture.bmp')
    dir_name = os.path.dirname(os.path.abspath(raw_imagepath))
    image_class1 = get_images.Get_Image()
    image_array = image_class1.image_ndarray(raw_imagepath)  # 导入图片形成图像数组
    #image_object = image_class1.image_object(raw_imagepath)  # 导入图片形成图像对象

    # '''
    ##############################无需裁剪时可注释掉该块代码
    #2592*1520像素
    # room1 = [(75,589,291,634),
    #          (82,652,287,696),
    #          (92,711,294,758),
    #          (112,773,263,809),
    #          (375,578,576,626),
    #          (362,642,578,691),
    #          (368,705,587,752),
    #          (372,769,580,806)]
    # room2 = [(698,570,925,616),
    #          (705,633,913,677),
    #          (705,695,922,740),
    #          (706,757,915,802),
    #          (714,817,922,854),
    #          (1019,565,1226,612),
    #          (1014,630,1218,672),
    #          (1016,690,1223,736),
    #          (1016,752,1235,797),
    #          (1020,813,1235,850)
    #          ]
    # room3 = [(1387,558,1559,606),
    #          (1388,622,1603,668),
    #          (1356,685,1631,730),
    #          (1394,748,1603,790),
    #          (1388,810,1599,844),
    #          (1699,556,1910,599),
    #          (1700,618,1913,659),
    #          (1701,680,1905,725),
    #          (1703,743,1906,785),
    #          (1705,804,1881,838)]
    # room4 = [(2056,553,2246,599),
    #          (2054,616,2241,660),
    #          (2051,678,2243,720),
    #          (2050,735,2235,777),
    #          (2052,794,2210,832),
    #          (2341,551,2515,597),
    #          (2335,614,2516,657),
    #          (2335,670,2502,714),
    #          (2326,733,2502,771),
    #          (2339,789,2483,825)]
    #####2560*1440像素
    room1 = [(59,551,283,591),
             (59,611,283,651),
             (59,670,283,710),
             (59,727,283,767),
             (336,541,560,583),
             (336,604,560,644),
             (336,664,560,704),
             (336,722,560,762)]
    room2 = [(686,534,910,574),
             (686,597,910,638),
             (686,658,910,698),
             (686,719,910,759),
             (686,779,910,814),
             (990,525,1214,571),
             (990,590,1214,630),
             (990,652,1214,692),
             (990,715,1214,755),
             (990,774,1214,809),
             ]
    room3 = [(1363,519,1587,559),
             (1363,583,1587,623),
             (1363,647,1587,687),
             (1363,707,1587,747),
             (1363,768,1587,803),
             (1681,518,1905,558),
             (1681,578,1905,618),
             (1681,641,1905,681),
             (1681,702,1905,742),
             (1681,762,1905,796)]
    room4 = [(2018,514,2242,554),
             (2018,573,2242,613),
             (2018,635,2242,675),
             (2018,697,2242,737),
             (2018,753,2242,788),
             (2295,513,2519,553),
             (2295,572,2519,612),
             (2295,632,2519,672),
             (2295,691,2519,731),
             (2295,747,2519,781)]
    room = [room1,room2,room3,room4]
    room_train_list = {}
    for j in range(4):
        room_name = j+1
        room_train_list[room_name] = []
        for i in room[j]:
            # 图像预处理:裁剪和旋转
            image_object = image_class1.image_object(raw_imagepath)
            preimg = ppro.Cut_rotate(raw_imagepath)
            # box_x = (180, 100)  # 左上点像素位置
            # box_y = (879, 244)  # 右下点像素位置
            box_x = (i[0], i[1])  # 左上点像素位置
            box_y = (i[2], i[3])  # 右下点像素位置
            tem_image_path = preimg.image_crop(image_object, x=box_x, y=box_y)

            '''
            raw_matrix = np.float32([[5, 93], [2525, 55], [25, 389], [2520, 343]])  # 待投影图指定区域四个顶点像素位置
            aim_matrix = np.float32([[0, 0], [2550, 0], [0, 350], [2550, 350]])  # 目标图四个顶点像素位置
            preimg.image_rotate(tem_image_path, raw_matrix, aim_matrix)
            '''

            # 图像处理
            # 1.再次导入图片
            image_class2 = get_images.Get_Image()
            image_object = image_class2.image_object(tem_image_path)
            ##########################################
            # '''

            # 2.进行处理
            # myimg = pro.Img_pro()
            # myimg.initTable()
            # image = myimg.image_split2(image_object)  # 通道分离
            # image.save(dir_name + '\\split.png')
            # image = myimg.image_filter(image)  # 图片滤波
            # image.save(dir_name + '\\filter.png')
            # image = myimg.image_enlarge_compress(image,r=1)  # 图片的压缩和扩大,默认系数r=1
            # image = myimg.image_sharp(image)  # 图片锐化，默认系数r=2.0
            # image.save(dir_name + '\\sharp.png')
            # image = myimg.image_binary(image)  # 图片二值化
            # image.save(dir_name + '\\binary.png')
            # image = myimg.image_binary_invert(image)  # 图片二值反转
            # image.save(dir_name + '\\invert.png')
            # image = myimg.image_enlarge_compress(image, r=1)  #默认r=1
            # image.save(dir_name + '\\compress.png')

            # 图像文字识别
            text = pytesseract.image_to_string(image_object)  # 文字识别
            room_train_list[room_name].append(text)

    return room_train_list
    #return sorted(room_train_list.iteritems(),key = lambda room_train_list:room_train_list[0])


if __name__ == "__main__":
    foldername = os.path.dirname(os.path.abspath(__file__))
    text = word_in_picture(foldername)
    print text
