
from machine import ADC
from machine import Pin

class LightSensor():

    def __init__(self, pin):
        #设置一个成员变量，使用Pin和ADC来绑定引脚
        self.lightadc = ADC(Pin(pin)) 

    def value(self):
        tlight = int(self.lightadc.read() * 6000 / 4096)
        return tlight
        #读取成员变量的数值，转换成Lux单位的光照数值，并返回，返回值为int类型