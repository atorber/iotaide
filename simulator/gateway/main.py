import psutil   # cd C:\Python36-32\Scripts  pip install psutil
import os
import platform
import time
import sys
import paho.mqtt.client as mqtt
import uuid
import random
import json
import get_username_password

# 物联网核心套件设备配置信息
IoTCoreId='ahryhns'
templateId='tl05j5ef'
DeviceKey='7fa83d34'
DeviceSecret='lOeUAXBSLYqAKlOH'
topic = templateId + '/' +DeviceKey + '/event/post/request'

config=get_username_password.get_device_config(IoTCoreId,DeviceKey,DeviceSecret,'thingidp',0,'MD5')
print(config)
count=0  

# 定义变量，用于存储设备最新状态
last_state={}
# 内存
last_state['memory_usage']=0
last_state['memory_total'] = 0
last_state['memory_free'] =0
# CPU
last_state['cpu_usage'] = 0
last_state['cpu_core_number']=0
# 磁盘
last_state['disk_usage']=0
# 系统信息,win->'nt'; Linux->'posix'
last_state['system_info']=os.name+'/'+sys.platform
# last_state['gateway_version']=platform.version()
last_state['gateway_version']='0.0.0'


# 获取本机磁盘使用率和剩余空间G信息
def get_disk_info():
    # 循环磁盘分区
    used_disk_size=0
    total_disk_size=0
    for disk in psutil.disk_partitions():
        # 读写方式 光盘 or 有效磁盘类型
        # if 'cdrom' in disk.opts or disk.fstype == '':
        #     continue
        disk_info = psutil.disk_usage(disk.device)
        # 磁盘已使用空间，单位G
        used_disk_size = used_disk_size+disk_info.used/1024/1024/1024
        # 当前磁盘总空间
        total_disk_size= total_disk_size+disk_info.total/1024/1024/1024

    # 计算磁盘总的使用率
    last_state['disk_usage']="%.2f" % ((used_disk_size/total_disk_size)*100)

# 获取CPU信息
def get_cpu_info():
    # CPU使用率
    last_state['cpu_usage'] = "%.2f" % psutil.cpu_percent(interval=1)
    # CPU内核数量
    last_state['cpu_core_number']="%i" % psutil.cpu_count(logical=True)

# 获取内存信息
def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    # 内存使用率
    last_state['memory_usage']="%.2f" % virtual_memory.percent
    # 内存总量
    last_state['memory_total'] = "%.2f" % (virtual_memory.total/1024/1024/1024)
    # 剩余内存
    last_state['memory_free'] ="%.2f" % (virtual_memory.free/1024/1024/1024)

def update_info():
    get_disk_info()
    get_cpu_info()
    get_memory_info()
    # print(last_state)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("#")     

def on_message(client, userdata, msg):
    global count
    count += 1
    print(str(count)+" 主题:"+msg.topic+" 消息:"+str(msg.payload.decode('utf-8')))

def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)

if __name__ == '__main__':
    client = mqtt.Client(config['client_id'])
    client.username_pw_set(config['username'], config['password'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.connect(config['HOST'], config['PORT'], 60)
    while True:
        update_info()
        payload={
        "reqId":str(uuid.uuid4()),
        "method":"thing.event.post",
        "timestamp":int(time.time()*1000),
        "properties":last_state
        }
        payload=json.dumps(payload)
        client.publish(topic,payload ,0)
        count+=1
        print('MQTT message count:%i' % count)
        print('MQTT message published:%s' % payload)
        time.sleep(30)

