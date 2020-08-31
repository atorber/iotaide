# -*- coding:utf-8 -*-

import hmac
import hashlib

def jm_sha256_single(value):
    """
    sha256加密
    :param value: 加密字符串
    :return: 加密结果转换为16进制字符串，并大写
    """
    hsobj = hashlib.sha256()
    hsobj.update(value.encode("utf-8"))
    return hsobj.hexdigest().lower()

def jm_md5_singlt(value):
    """
    md5加密
    :param value: 加密字符串
    :return: 加密结果转换为16进制字符串，并大写
    """
    hsobj = hashlib.md5()
    hsobj.update(value.encode("utf-8"))
    return hsobj.hexdigest().lower()

def hmac_sha256_single(value):
    """
    hmacsha256加密
    :param value: 加密字符串
    :return: 加密结果转换为16进制字符串，并大写
    """
    message = value.encode("utf-8")
    return hmac.new(message, digestmod=hashlib.sha256).hexdigest().lower()

def hmac_md5_single(value):
    """
    hmacmd5加密
    :param value: 加密字符串
    :return: 加密结果转换为16进制字符串，并大写
    """
    message = value.encode("utf-8")
    return hmac.new(message, digestmod=hashlib.md5).hexdigest().lower()

def get_device_config(IoTCoreId,device_key,device_secret,adp_type='thingidp',timestamp=0,algorithm_type='MD5'):
    """
        iotCoreId='ahryhns'
        templateId='tl05j5ef'
        device_name='7fa83d34'
        HOST = iotCoreId+'.iot.gz.baidubce.com'
    """
    username=adp_type+'@'+IoTCoreId+'|'+device_key+'|'+str(timestamp)+'|'+algorithm_type
    passwore_join=device_key+'&'+str(timestamp)+'&'+algorithm_type+device_secret

    if algorithm_type=='MD5':
        password=jm_md5_singlt(passwore_join)
    elif algorithm_type=='SHA256':
        password=jm_sha256_single(passwore_join)
    else:
        password=''

    config={}

    config['HOST'] = IoTCoreId+'.iot.gz.baidubce.com'
    config['PORT'] = 1883
    config['username'] = username
    config['password'] = password
    config['client_id'] = device_key

    return config




