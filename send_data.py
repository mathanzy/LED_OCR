#-*- coding:utf-8 -*-
import urllib2
import json

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