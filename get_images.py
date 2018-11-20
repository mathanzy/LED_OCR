#-*- coding:utf-8 -*-
'''
从图站本地文件获取图片
'''

import cv2 
from PIL import Image

class Get_Image(object):
	def __init__(self):
		pass
		#self.imagepath1 = imagepath1
		#self.imagepath2 = imagepath2


	def image_ndarray(self,imagepath):
		image_array = cv2.imread(imagepath)
		return image_array

	def image_object(self,imagepath):
		image_object = Image.open(imagepath)
		return image_object