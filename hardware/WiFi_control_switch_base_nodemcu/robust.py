import utime
import simple

class MQTTClient(simple.MQTTClient):

    DELAY = 2
    DEBUG = False
    i=0

    def delay(self, i):
        utime.sleep(i)

    def log(self, in_reconnect, e):
        if self.DEBUG:
            if in_reconnect:
                print("mqtt reconnect: %r" % e)
            else:
                print("mqtt: %r" % e)

    def reconnect(self):
        global i
        while 1:
            try:
                return super().connect(False)
            except OSError as e:
                self.log(True, e)
                if i<10:
                  i += 1
                self.delay(i)

    def publish(self, topic, msg, retain=False, qos=0):
        while 1:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.log(False, e)
            self.reconnect()

    def wait_msg(self):
        while 1:
            try:
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
            self.reconnect()

