from machine import ADC
from machine import Pin, Signal
class Button():
    def __init__(self,pin):
        self.buttonpin = Pin(pin, Pin.IN)
        self.last_status = self.buttonpin.value()

    
    def state(self):
        #self.last_status = 1
        self.last_status = self.buttonpin.value()
        return self.last_status
