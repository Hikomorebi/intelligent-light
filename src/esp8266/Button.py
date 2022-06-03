from machine import ADC
from machine import Pin, Signal
class Button():
    def __init__(self,pin):
        self.buttonpin = Pin(pin, Pin.OUT)
        self.relayled = Signal(self.relaypin, invert=True) # 将信号置反, 实现开与关和输入信号对应
    
    def state(self):
        self.sta = 1
        return self.sta
