
from machine import PWM
from machine import Pin

class Led():
    """
    创建LED类
    """
    def __init__(self, rpin, gpin, bpin, sfreq=1000):
        """
        构造函数
        :param pin: 接LED的管脚，必须支持PWM
        :param freq: PWM的默认频率是1000
        """
        #以rpin, gpin, bpin为参数，使用Pin和PWM来绑定三个引脚来控制led灯的红黄蓝的三个PWM信号
        self.led_red = PWM(Pin(rpin), freq = sfreq)
        self.led_green = PWM(Pin(gpin), freq = sfreq)
        self.led_blue = PWM(Pin(bpin), freq = sfreq)
		

    def rgb_light(self, red, green, blue, brightness):
		#red green blue的范围在range(256)内，brightness的范围在[0,1]内，如果取值不在正确范围内，什么也不做
        #调用duty成员函数来设置三种颜色的占空比
        if brightness < 0.0 or brightness > 1.0:
            return
        if red not in range(256):
            return
        if green not in range(256):
            return
        if blue not in range(256):
            return
        self.pwm_red = self.led_red.duty(int(red/255*brightness*1023))
        self.pwm_green = self.led_green.duty(int(green/255*brightness*1023))
        self.pwm_blue = self.led_blue.duty(int(blue/255*brightness*1023))
		

    def deinit(self):
        """
        析构函数
        """
        self.led_red.deinit()
        self.led_green.deinit()
        self.led_blue.deinit()