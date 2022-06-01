
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
		

    def rgb_light(self, red, green, blue, brightness):
		#red green blue的范围在range(256)内，brightness的范围在[0,1]内，如果取值不在正确范围内，什么也不做
        #调用duty成员函数来设置三种颜色的占空比
		

    def deinit(self):
        """
        析构函数
        """
        self.led_red.deinit()
        self.led_green.deinit()
        self.led_blue.deinit()