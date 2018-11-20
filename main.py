#-*- coding:utf-8 -*-
'''
进行图片比对和文字识别
'''
import word_recongination
import picture_compare
import get_trains
import get_images
import os
import send_data
import cv2
import time
import numpy as np
from base64 import b64encode
import base64
import MySQLdb

def compare_result(imagepath1,imagepath2):
    img = get_images.Get_Image()
    image_object1 = img.image_object(imagepath1)
    image_object2 = img.image_object(imagepath2)
    result = picture_compare.image_contract(image_object1,image_object2)
    return result

def recongination_result(folderpath):
    plan_list = get_trains.train_list()
    # fake data：
    # plan_list = {1:['K903','Z7837','K7808(8-17)','K1333','K892','K1292','K520','Z198'],
    #              #2:['K1082','K7802','K7808(1-7)','K566','K374','K962','4619','K604','T41','Z192'],
    #              2: ['K7808(1-7)', 'K566', 'K374', 'K962', '4619', 'K604', 'T41', 'Z192'],
    #              3:['K1807','1365','1485','4636','4643','2095','K1115','Z55','K545'],
    #              4:['K1081','K7807','K961','6032','K7833','K894','Z7806','T175','1551','K730']}

    real_list = word_recongination.word_in_picture(folderpath)
    print 'pss_plan：{}'.format(plan_list)  #旅服到发
    print 'real_led：{}'.format(real_list)  #LED屏显示
    led_flag = 0  #0表示不能确定需核对；1表示完全正确；-1表示错误
    temp_flag = {}
    for i in range(4):
        temp_flag[i+1] = 0
        temp = len(plan_list[i+1])
        for j in range(temp):
            if real_list[i+1][j] == plan_list[i+1][j]:
                temp_flag[i+1] += j+1
        if temp_flag[i+1] <= 1:
            for x in range(temp-1):
                if real_list[i+1][temp-1-x] == plan_list[i+1][temp-1-x-1]:  #错一位相等
                    temp_flag[i+1] -= 2
            if temp_flag[i+1] > -1:
                for y in range(temp-2):
                    if real_list[i+1][temp-1-y] == plan_list[i+1][temp-1-y-2]:  #错两位相等
                        temp_flag[i+1] -= 3


    if temp_flag[1] >= 1 and temp_flag[2] >= 1 and temp_flag[3] >= 1 and temp_flag[4] >= 1:
        if temp_flag[1] >=2 and temp_flag[2] >= 2 and temp_flag[3] >=2 and temp_flag[4] >=2:
            led_flag = 1
        if temp_flag[1] ==1 or temp_flag[2] ==1 or temp_flag[3] == 1 or temp_flag[4] == 1:
            led_flag = 0

    if temp_flag[1] < 0 or temp_flag[2] < 0 or temp_flag[3] < 0 or temp_flag[4] < 0:
        led_flag = -1
    '''针对太原站的led监测具有自主配置的功能，这里分情况'''
    #判断是否一致
    #判断是否某一候车室正常下屏一趟车但屏未刷
    #判断是否某一候车室晚点下屏一趟车但屏未刷
    #判断是否某一候车室正常下屏两趟但屏未刷
    return led_flag

def image_stack(folderpath,path1,path2):
    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)
    # raw_matrix = np.float32([[38,483],[2571,483],[38,867],[2571,867]])
    raw_matrix = np.float32([[23, 481], [2549, 441], [43, 834], [2541, 792]])
    aim_matrix = np.float32([[0, 0], [797, 0], [0, 140], [797, 140]])
    x = aim_matrix[3][0]
    y = aim_matrix[3][1]
    convert_matrix = cv2.getPerspectiveTransform(raw_matrix, aim_matrix)
    # image = cv2.warpPerspective(imagearray,convert_matrix,(x,y),cv2.INTER_LINEAR)
    image_crop = cv2.warpPerspective(image1, convert_matrix, (x, y))  # python2中无cv2.INTER_LINEAR参数
    stack_png = np.vstack((image_crop, image2))
    #vs_imagepath = os.path.join(folderpath,'test_imgs\\vstackimage.png')
    #cv2.imwrite(vs_imagepath, stack_png)
    #return vs_imagepath
    return stack_png

def image_byte_str_to_array(byte_array):
    nparr = np.fromstring(byte_array,np.uint8)
    return cv2.imdecode(nparr,cv2.IMREAD_COLOR)

def image_array_to_byte_str(image_matrix, quality=100, r=None):
    if r:
        image_matrix = cv2.resize(image_matrix, (int(r * image_matrix.shape[1]), int(r * image_matrix.shape[0])))
    return cv2.imencode('.jpg', image_matrix, [cv2.IMWRITE_JPEG_QUALITY, quality])[1].tostring()

def image_to_base64(img_ndarray, encoding='utf-8', quality=100, ratio=1.0):
    try:
        img_bytes = image_array_to_byte_str(img_ndarray, quality=quality, r=ratio)
        base64_bytes = b64encode(img_bytes)
        base64_str = base64_bytes.decode(encoding)
        return base64_str
    except Exception, e:
        print 'image_to_base64', e
        return None


if __name__ == "__main__":
    time_format = '%Y-%m-%d %H:%M:%S'
    folderpath = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.join(folderpath,'LEDCapturePics\\ledVideCapture.bmp')
    path2 = os.path.join(folderpath,'LEDCapturePics\\LedTemp.png')

    # 接口url配置
    raw_url_tujing = "http://10.81.33.113:1500" #和图景的测试接口
    real_url = raw_url_tujing + "/iivms-home/alarmout/putIVAInfo"

    while True:
        try:
            #print "两张图片的不相似程度为：{}".format(compare_result(path1, path2))
            flag = recongination_result(folderpath)
            if flag == -1:
                led_img = image_stack(folderpath,path1,path2)
                vs_imagepath = os.path.join(folderpath,'LEDCapturePics\\-1\\vstackimage.png')
                cv2.imwrite(vs_imagepath, led_img)
                base64_led_img = image_to_base64(led_img, ratio=1)
                now_time = time.time()
                ledInfo = {'cameraId': 301, 'cameraIp': '10.90.129.188', 'createTime': int(now_time), 'type':'ledCheck','desc':[{'flag':-1,}],'img':base64_led_img}
                #now_time = time.strftime(time_format, time.localtime(now_time))  #时间格式调整
                #ledInfo_tujing = {'cameraId': 301, 'cameraIp': '10.90.129.188', 'createTime': now_time, 'type':'ledCheck','desc':[{'flag':-1,}],'img':base64_led_img}
                '''
                #MySQL数据库
                try:
                    db = MySQLdb.connect('10.81.33.117','root','900612','tujing',charset='utf8')
                    cursor = db.cursor()
                    sql = "INSERT INTO LED_ALARM(CAMERAID, CREATETIME, ALARM_TYPE, ALARM_DESC, ALARM_IMG) VALUES('%d','%s','%s','%s','%s')" %(5,now_time,'led',"flag:"+str(flag)+"中央通道屏显示错误",'C:User/desktop/')
                    cursor.execute(sql)
                    db.commit()
                except Expection, e:
                    db.rollback()
                    print e
                finally:
                    cursor.close()
                    db.close()
                    '''
                ledInfo = [ledInfo]
                print send_data.send_post(real_url, ledInfo)
            elif flag == 0 :
                led_img = image_stack(folderpath, path1, path2)
                vs_imagepath = os.path.join(folderpath, 'LEDCapturePics\\0\\vstackimage.png')
                cv2.imwrite(vs_imagepath, led_img)
                base64_led_img = image_to_base64(led_img, ratio=1)
                now_time = time.time()
                ledInfo = {'cameraId': 301, 'cameraIp': '10.90.129.188', 'createTime': int(now_time), 'type':'ledCheck','desc':[{'flag':0,}],'img':base64_led_img}
                ledInfo = [ledInfo]
                print send_data.send_post(real_url, ledInfo)
            else:
                led_img = image_stack(folderpath, path1, path2)
                vs_imagepath = os.path.join(folderpath, 'LEDCapturePics\\1\\vstackimage.png')
                cv2.imwrite(vs_imagepath, led_img)
                base64_led_img = image_to_base64(led_img, ratio=1)
                now_time = time.time()
                ledInfo = {'cameraId': 301, 'cameraIp': '10.90.129.188', 'createTime': int(now_time), 'type':'ledCheck','desc':[{'flag':1,}],'img':base64_led_img}
                ledInfo = [ledInfo]
                print send_data.send_post(real_url, ledInfo_tu)
        except Exception, e:
            print e
        finally:
            time.sleep(10)
