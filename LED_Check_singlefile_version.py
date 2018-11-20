#-*- coding:utf-8 -*-
'''
Recent Modified: 2018-06-06
The file is for LED-Check.
This file is gathering the files (in original version) for checking LED into a single file. which may be long coded and not easy to modifed.
But it will be easy to get a .exe file.
'''
import numpy as np
import urllib2
import urllib
import json
import time
import cv2
from PIL import Image
from base64 import b64encode
import MySQLdb

# 1. Get trains plan info from PSS
def train_list_from_PSS():
    src_url = "http://10.81.33.151/api/oauth/token"
    Authorization = 'Basic bXktdHJ1c3RlZC1jbGllbnQ6c2VjcmV0'
    headers = {'Authorization': Authorization}
    data = {'grant_type': 'password', 'username': 'admin', 'password': 'admin2018'}
    data = urllib.urlencode(data)
    request = urllib2.Request(url=src_url, data=data, headers=headers)
    try:
        response = urllib2.urlopen(request) #make a url request
        #  print response.read()
    except Exception, e:
        print "Error:", e

    response_data = response.read()
    access_token = eval(response_data)['access_token']  # get the token
    temp_url = 'http://10.81.33.151:8080/api/service/monitoringLEDScreen'  #interface modified on 2018-04-26
    paras = {"access_token": access_token, "pageSize": 150}
    paras = urllib.urlencode(paras)
    dest_url = temp_url + "?" + paras
    request = urllib2.Request(dest_url)
    response = urllib2.urlopen(request)
    train_info = response.read().decode('utf-8')
    #print train_info
    train_info_dict = {}
    train_info_dict = json.loads(train_info)
    train_info_dict = train_info_dict['data']['list']
    # sort the train list with 'DEPARTURE_TIME'
    train_info_dict_sort = sorted(train_info_dict,key = lambda train_info_dict:train_info_dict['DEPARTURE_TIME'])
    #train_info_dict_sort = set(train_info_dict_sort)
    # #print train_info_dict_sort

    room1 = []
    room2 = []
    room3 = []
    room4 = []
    realtime = time.strftime('%Y-%m-%d %H:%M:%S.0') #get the now time to comapre with the 'DEPARTURE_TIME'. Is it necessary?
    for i in train_info_dict_sort:
        if i['REAL_WAIT_NAME'] in [u'\u7b2c\u4e00\u5019\u8f66\u5ba4',u'\u7b2c\u4e00\u5019\u8f66\u5ba4\u002c\u7b2c\u4e8c\u5019\u8f66\u5ba4'] and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
            if i['DEPARTURE_TRAIN_CODE'] == 'K7808':
                room1.append(i['DEPARTURE_TRAIN_CODE'] + '(8-17)')
                room2.append(i['DEPARTURE_TRAIN_CODE'] + '(1-7)')
            else:
                room1.append(i['DEPARTURE_TRAIN_CODE'])
        elif i['WAIT_NAME'] == u'\u7b2c\u4e8c\u5019\u8f66\u5ba4' and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
            room2.append(i['DEPARTURE_TRAIN_CODE'])
        elif i['WAIT_NAME'] == u'\u7b2c\u4e09\u5019\u8f66\u5ba4' and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
            room3.append(i['DEPARTURE_TRAIN_CODE'])
        elif i['WAIT_NAME'] == u'\u7b2c\u56db\u5019\u8f66\u5ba4' and i['TRAIN_TYPE'] <> "2" and i['DEPARTURE_TIME'] > realtime:
            room4.append(i['DEPARTURE_TRAIN_CODE'])
    train_list = {}
    train_list[1] = []
    train_list[2] = []
    train_list[3] = []
    train_list[4] = []
    if len(room1) < 9:
        train_list[1].extend(room1)
    else:
        train_list[1].extend(room1[0:8])
    if len(room2) < 11:
        train_list[2].extend(room2)
    else:
        train_list[2].extend(room2[0:10])
    if len(room3) < 11:
        train_list[3].extend(room3)
    else:
        train_list[3].extend(room3[0:10])
    if len(room4) < 11:
        train_list[4].extend(room4)
    else:
        train_list[4].extend(room4[0:10])
    return train_list

# 2. Get realtime image of the led-camera
def get_image_ndarry(imagepath):
    image_array = cv2.imread(imagepath)
    return image_array
def get_image_object(imagepath):
    image_object = Image.open(imagepath)
    return image_object

# 3. Process the led-image: crop, recrop, rotate, filter
def image_crop(imagepath,image_object,x=None,y=None):  # x:left-up and y:right-down
    try:
        box = (x[0], x[1], y[0], y[1])
    except:
        print('please input the left_up and right_down coordination')
        return
    image = image_object.crop(box)
    imagepath = os.path.join(os.path.dirname(os.path.abspath(imagepath)), 'image_crop.png')
    image.save(imagepath)
    return imagepath

# 4. Recognize the wrods (trains) from the processed images
import os
import pytesseract
def train_in_picture(imagepath):
    raw_imagepath = imagepath
    #raw_imagepath = os.path.join(folderpath, 'test_imgs\\ledVideCapture.bmp')
    #dir_name = os.path.dirname(os.path.abspath(raw_imagepath))
    # crop each train from the led capture image
    room1 = [(59, 551, 283, 591),
             (59, 611, 283, 651),
             (59, 670, 283, 710),
             (59, 727, 283, 767),
             (336, 541, 560, 583),
             (336, 604, 560, 644),
             (336, 664, 560, 704),
             (336, 722, 560, 762)]
    room2 = [(686, 534, 910, 574),
             (686, 597, 910, 638),
             (686, 658, 910, 698),
             (686, 719, 910, 759),
             (686, 779, 910, 814),
             (990, 525, 1214, 571),
             (990, 590, 1214, 630),
             (990, 652, 1214, 692),
             (990, 715, 1214, 755),
             (990, 774, 1214, 809),
             ]
    room3 = [(1363, 519, 1587, 559),
             (1363, 583, 1587, 623),
             (1363, 647, 1587, 687),
             (1363, 707, 1587, 747),
             (1363, 768, 1587, 803),
             (1681, 518, 1905, 558),
             (1681, 578, 1905, 618),
             (1681, 641, 1905, 681),
             (1681, 702, 1905, 742),
             (1681, 762, 1905, 796)]
    room4 = [(2018, 514, 2242, 554),
             (2018, 573, 2242, 613),
             (2018, 635, 2242, 675),
             (2018, 697, 2242, 737),
             (2018, 753, 2242, 788),
             (2295, 513, 2519, 553),
             (2295, 572, 2519, 612),
             (2295, 632, 2519, 672),
             (2295, 691, 2519, 731),
             (2295, 747, 2519, 781)]
    room = [room1, room2, room3, room4]
    room_train_list = {}
    for j in range(4):
        room_name = j+1
        room_train_list[room_name] = []
        for i in room[j]:
            # image process: crop and rotate
            image_object = get_image_object(raw_imagepath)
            #preimg = ppro.Cut_rotate(raw_imagepath)
            box_x = (i[0], i[1])  # position of the left-up pixel
            box_y = (i[2], i[3])  # position of the right-down pixel
            tem_image_path = image_crop(raw_imagepath,image_object, x=box_x, y=box_y)
            new_image_object = get_image_object(tem_image_path)
            text = pytesseract.image_to_string(new_image_object) # word recognization
            room_train_list[room_name].append(text)
    return room_train_list

# 5. Compare the trains from PPS with the trains get from recognization. Alarm with the result
def recongination_result(imagepath):
    #plan_list = train_list_from_PSS()
    # fake data：
    plan_list = {1:['K903','Z7837','K7808(8-17)','K1333','K892','K1292','K520','Z198'],
                  #2:['K1082','K7802','K7808(1-7)','K566','K374','K962','4619','K604','T41','Z192'],
                  2: ['K7808(1-7)', 'K566', 'K374', 'K962', '4619', 'K604', 'T41', 'Z192'],
                  3:['K1807','1365','1485','4636','4643','2095','K1115','Z55','K545'],
                  4:['K1081','K7807','K961','6032','K7833','K894','Z7806','T175','1551','K730']}

    real_list = train_in_picture(imagepath)
    print 'train list of plan：{}'.format(plan_list)  # train list from PSS
    print 'train list of led：{}'.format(real_list)   # trian list form LED
    led_flag = 0  #0: not clearly；1: exactly right；-1: exactly wrong
    temp_flag = {}
    for i in range(4):
        temp_flag[i+1] = 0
        temp = len(plan_list[i+1])
        for j in range(temp):
            if real_list[i+1][j] == plan_list[i+1][j]:
                temp_flag[i+1] += j+1
        if temp_flag[i+1] <= 1:
            for x in range(temp-1):
                if real_list[i+1][temp-1-x] == plan_list[i+1][temp-1-x-1]:  # equal with offset is one
                    temp_flag[i+1] -= 2
            if temp_flag[i+1] > -1:
                for y in range(temp-2):
                    if real_list[i+1][temp-1-y] == plan_list[i+1][temp-1-y-2]:  #equal with offset is two
                        temp_flag[i+1] -= 3


    if temp_flag[1] >= 1 and temp_flag[2] >= 1 and temp_flag[3] >= 1 and temp_flag[4] >= 1:
        if temp_flag[1] >=2 and temp_flag[2] >= 2 and temp_flag[3] >=2 and temp_flag[4] >=2:
            led_flag = 1
        if temp_flag[1] ==1 or temp_flag[2] ==1 or temp_flag[3] == 1 or temp_flag[4] == 1:
            led_flag = 0

    if temp_flag[1] < 0 or temp_flag[2] < 0 or temp_flag[3] < 0 or temp_flag[4] < 0:
        led_flag = -1

    # other cases: offset is three ...
    return led_flag

#6. vstack the raw image with the manual image
def image_stack(path1,path2):
    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)
    raw_matrix = np.float32([[23, 481], [2549, 441], [43, 834], [2541, 792]])
    aim_matrix = np.float32([[0, 0], [797, 0], [0, 140], [797, 140]])
    x = aim_matrix[3][0]
    y = aim_matrix[3][1]
    convert_matrix = cv2.getPerspectiveTransform(raw_matrix, aim_matrix)
    # image = cv2.warpPerspective(imagearray,convert_matrix,(x,y),cv2.INTER_LINEAR)
    image_crop = cv2.warpPerspective(image1, convert_matrix, (x, y))  # python2中无cv2.INTER_LINEAR参数
    stack_png = np.vstack((image_crop, image2))
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

# 7. Send data: get and post
def send_get(request_url=None, request_params={}):
    if request_url:
        request_url = request_url.strip()
        if request_url:
            params_str = '&'.join('{}={}'.format(key, value) for key, value in request_params.items())
            if request_url[-1] == '?':
                request_url = '{}{}'.format(request_url, params_str)
            else:
                request_url = '{}?{}'.format(request_url, params_str)
            request = urllib2.Request(request_url)
            try:
                response_data = urllib2.urlopen(request)
                return response_data.read()
            except Exception, e:
                print 'Error:', e
                return None
        else:
            print 'request url bad'
            return None
    print 'request url bad'
    return None

def send_post(request_url, request_params={}):
    if request_url:
        request_url = request_url.strip()
        if request_url:
            request = urllib2.Request(url=request_url, data=json.dumps(request_params))
            try:
                response_data = urllib2.urlopen(request)
                return response_data.read()
            except Exception, e:
                print 'Error:', e
                return None
        else:
            print 'request url bad'
            return None
    print 'request url bad'
    return None

# 7. main
if __name__ == "__main__":
    time_format = "%Y-%m-%d %H:%M:%S"
    folder_path = os.path.dirname(os.path.abspath(__file__))
    raw_image_path = os.path.join(folder_path, 'LEDCapturePics\\ledVideCapture.bmp')
    manual_image_path = os.path.join(folder_path,'LEDCapturePics\\LedTemp.png')
    test_url = "http://127.0.0.1:8082"
    tujing_url2 = "http://10.81.33.178:1500"  # test interface
    real_url = test_url + "/iivms-home/alarmout/putIVAInfo"

    while True:
        try:
            flag = recongination_result(raw_image_path)
            if flag == -1:
                led_check_show = image_stack(raw_image_path, manual_image_path)
                vs_imagepath = os.path.join(folder_path, 'LEDCapturePics\\-1\\{}.png'.format('wrong'))
                cv2.imwrite(vs_imagepath, led_check_show)
                base64_led_img = image_to_base64(led_check_show, ratio=1)
                now_time = time.time()
                ledInfo = {"cameraid": 301, "createTime": int(now_time), "type": "led", "desc": "中央通道屏显示错误",
                           "img": base64_led_img}
                now_time = time.strftime(time_format, time.localtime(now_time))
                ledInfo_tujing = {"cameraid": 301, "createTime": now_time, "type": "led", "desc": "中央通道屏显示错误",
                                  "img": base64_led_img}
                '''
                # MySQL
                try:
                    db = MySQLdb.connect('localhost', 'root', '900612', 'tujing', charset='utf8')
                    cursor = db.cursor()
                    sql = "INSERT INTO LED_ALARM(CAMERAID, CREATETIME, ALARM_TYPE, ALARM_DESC, ALARM_IMG) VALUES('%d','%s','%s','%s','%s')" % (
                           5, now_time, 'led', "flag:" + str(flag) + "中央通道屏显示错误", 'C:User/desktop/')
                    cursor.execute(sql)
                    db.commit()
                except Expection, e:
                    db.rollback()
                    print e
                finally:
                    cursor.close()
                    db.close()
                    print send_post(real_url, ledInfo_tujing)
                '''
                print send_post(real_url,ledInfo_tujing)
            elif flag == 0:
                led_check_show = image_stack(raw_image_path, manual_image_path)
                vs_imagepath = os.path.join(folder_path, 'LEDCapturePics\\0\\{}.png'.format('unsure'))
                cv2.imwrite(vs_imagepath, led_check_show)
                base64_led_img = image_to_base64(led_check_show, ratio=1)
                now_time = time.time()
                ledInfo = {"cameraid": 301, "createTime": int(now_time), "type": "led", "desc": "中央通道屏显示需确认",
                           "img": base64_led_img}
                now_time = time.strftime(time_format, time.localtime(now_time))
                ledInfo_tujing = {"cameraid": 301, "createTime": now_time, "type": "led", "desc": "中央通道屏显示需确认",
                                  "img": base64_led_img}
                print send_post(real_url, ledInfo_tujing)
            else:
                led_check_show = image_stack(raw_image_path, manual_image_path)
                vs_imagepath = os.path.join(folder_path, 'LEDCapturePics\\1\\{}.png'.format('right'))
                cv2.imwrite(vs_imagepath, led_check_show)
                base64_led_img = image_to_base64(led_check_show, ratio=1)
                now_time = time.time()
                ledInfo = {"cameraid": 301, "createTime": int(now_time), "type": "led", "desc": "中央通道屏显示正确",
                           "img": base64_led_img}
                now_time = time.strftime(time_format, time.localtime(now_time))
                ledInfo_tujing = {"cameraid": 301, "createTime": now_time, "type": "led", "desc": "中央通道屏显示正确",
                                  "img": base64_led_img}
                print send_post(real_url, ledInfo_tujing)
        except Exception, e:
            print e
        finally:
            time.sleep(10)