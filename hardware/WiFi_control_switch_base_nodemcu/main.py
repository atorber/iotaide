
from machine import Pin
import network
import time
import json
from robust import MQTTClient
#from simple import MQTTClient

#import _thread

# wifi配置信息
SSID="HUAWEI-LUYC"
PASSWORD="15901228151"

# 设备配置信息
SERVER = "ahryhns.iot.gz.baidubce.com"
CLIENT_ID = "e43b3850"
TOPIC = b"t3ta0k6j/e43b3850/event/post/request"
username='thingidp@ahryhns|e43b3850|0|MD5'
password='替换为连接密码'

ON=True
OFF=False
i=0

# 初始化引脚
button=Pin(16,Pin.IN,OFF)
d1=Pin(5,Pin.OUT)   
d2=Pin(4,Pin.OUT)   
d3=Pin(0,Pin.OUT)   
d4=Pin(2,Pin.OUT)   
d5=Pin(14,Pin.OUT)   
d6=Pin(12,Pin.OUT)   
d7=Pin(13,Pin.OUT)   
d8=Pin(15,Pin.OUT)  

# 连接平台     
def connectMQTT():
  global sta_if,c
  c = MQTTClient(CLIENT_ID, SERVER,1883,username,password)
  c.DEBUG = True
  c.set_callback(sub_cb)
  c.connect()
  #close_all()
  cur_state=json.dumps(get_states())
  c.publish(TOPIC,cur_state,retain= True) 
  print(cur_state)  
  sub_msg()
  
# 获取各开关当前状态    
def get_states():
  global states
  states={
  "reqId":123,
  "method":"thing.event.post",
  "properties":{}
  }
  states['properties']['d1']=d1.value()
  states['properties']['d2']=d2.value()
  states['properties']['d3']=d3.value()
  states['properties']['d4']=d4.value()
  states['properties']['d5']=d5.value() 
  states['properties']['d6']=d6.value()
  states['properties']['d7']=d7.value()
  states['properties']['d8']=d8.value()
  return states

# 每30s上报状态信息   
def publish_msg():
    while(1):  
      msg = json.dumps(get_states())
      print(msg)
      c.publish(TOPIC,msg,retain= True)
      time.sleep(30)

# 订阅接收远程控制指令    
def sub_msg():
    c.subscribe(b"t3ta0k6j/e43b3850/service/set/request")
    c.subscribe(b"t3ta0k6j/e43b3850/service/get/request")
    print(sta_if.isconnected())
    while sta_if.isconnected():
      c.wait_msg()
    print('reconnecte')
    do_connect(SSID,PASSWORD)

# 远程指令执行          
def sub_cb(topic, msg):
    print((topic, msg))
    j = json.loads(msg)
    print(j)
    if topic==b"t3ta0k6j/e43b3850/service/get/request":
      pass
    else:
      for k,v in j['params'].items():
        print(k)
        print(v)
        if k=='d1':
          d1.value(v)
        elif k=='d2':
          d2.value(v)
        elif k=='d3':
          d3.value(v)
        elif k=='d4':
          d4.value(v)
        elif k=='d5':
          d5.value(v)
        elif k=='d6':
          d6.value(v)
        elif k=='d7':
          d7.value(v)
        elif k=='d8':
          d8.value(v)
        else:
          pass
    c.publish(TOPIC,json.dumps(get_states()),retain= True)

# 执行关闭所有    
def close_all():
  d1.value(OFF)
  d2.value(OFF)
  d3.value(OFF)
  d4.value(OFF)
  d5.value(OFF)
  d6.value(OFF)
  d7.value(OFF)
  d8.value(OFF)
  c.publish(TOPIC,json.dumps(get_states()),retain= True)

# 执行打开所有 
def open_all():
  d1.value(ON)
  d2.value(ON)
  d3.value(ON)
  d4.value(ON)
  d5.value(ON)
  d6.value(ON)
  d7.value(ON)
  d8.value(ON)
  c.publish(TOPIC,json.dumps(get_states()),retain= True)  

# 复位开关（全部关闭） 
def button_on():
  while True:
    if button.value()==1 and (d1.value() or d2.value() or d3.value() or d4.value() or d5.value() or d6.value() or d7.value() or d8.value()):
          close_all()
    elif button.value()==1:
          open_all()
    else:
          pass
 
def teardown():
  try:
      c.disconnect()
      print("Disconnected.")
  except Exception:
      print("Couldn't disconnect cleanly.")
      
def do_connect(SSID,PASSWORD):
  global sta_if
  sta_if = network.WLAN(network.STA_IF)
  ap_if = network.WLAN(network.AP_IF)
  if ap_if.active():
          ap_if.active(False)
  if not sta_if.isconnected():
          print('connecting to network...')
  sta_if.active(True)
  sta_if.connect(SSID, PASSWORD) #wifi的SSID和密码
  while not sta_if.isconnected():
          pass
  print('network config:', sta_if.ifconfig())
  try:
    connectMQTT()
  except Exception:
      print("connectMQTT() fail.")
      time.sleep(1)
      do_connect(SSID,PASSWORD)
  
if __name__ == '__main__':
  d1.value(OFF)
  d2.value(OFF)
  d3.value(OFF)
  d4.value(OFF)
  d5.value(OFF)
  d6.value(OFF)
  d7.value(OFF)
  d8.value(OFF)
  do_connect(SSID,PASSWORD)

  # try:
  #     publish_msg()
  # finally:
  #     teardown()











