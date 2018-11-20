#-*- coding:utf-8 -*-
'''
进行图片两张图片相似度的比较
'''

import math
import operator
from functools import reduce

def image_contract(image_object1,image_object2):
    '比较两张图片的像素分布'
    h1 = image_object1.histogram()
    h2 = image_object2.histogram()
    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return result
