
from LED import Led
from Button import Button
from Relay import Relay

import time 
import uasyncio
import network
import ujson
from umqtt.simple import MQTTClient

"""
Wi-Fi Gateway : SSID and Password
"""
WIFI_AP_SSID = "komorebi"
WIFI_AP_PSW = "asdfghjkl"

"""
QCloud Device Info
"""
DEVICE_NAME = "Led_1"
PRODUCT_ID = "WNSBO8V9GJ"
DEVICE_KEY = "6e5jWv++n7v5DznjpzkVbw=="

"""
MQTT topic
"""
MQTT_CONTROL_TOPIC = "$thing/down/property/"+PRODUCT_ID+"/"+DEVICE_NAME
MQTT_CONTROL_REPLY_TOPIC = "$thing/up/property/"+PRODUCT_ID+"/"+DEVICE_NAME

led = Led(5, 4, 0)
relay = Relay(16)
button = Button(14)

mqtt_client = None
color = 0   #enum 0=red, 1=green, 2=blue
name= ""    #light name. it is optional
brightness = 100  # 0%~100%
light_changed = False

async def wifi_connect(ssid, pwd):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, pwd)

    while not sta.isconnected():
        print("Wi-Fi Connecting...")
        time.sleep_ms(500)

def mqtt_callback(topic, msg):
    global led, relay, button
    global color, name, brightness, light_changed

    print((topic, msg))
    msg_json = ujson.loads(msg)
    if msg_json['method'] == 'control':
        params = msg_json['params']

        power_switch_tmp = params.get('power_switch')
        if power_switch_tmp is not None:
            power_switch = power_switch_tmp
            relay.set_state(power_switch)
        
        brightness_tmp = params.get('brightness')
        if brightness_tmp is not None:
            brightness = brightness_tmp

        color_tmp = params.get('color')
        if color_tmp is not None:
            color = color_tmp
        
        name_tmp = params.get('name')
        if name_tmp is not None:
            name = name_tmp
        
        if brightness_tmp is not None or color_tmp is not None:
            light_changed = True

async def mqtt_connect():
    global mqtt_client

    MQTT_SERVER = PRODUCT_ID + ".iotcloud.tencentdevices.com"
    MQTT_PORT = 1883
    MQTT_CLIENT_ID = PRODUCT_ID+DEVICE_NAME
    MQTT_USER_NAME = "WNSBO8V9GJLed_1;12010126;ES29I;1654689393"
    MQTTT_PASSWORD = "a7da552db0ef10508e17e86768d89cf74525cd848f39e42410971bb97f67242f;hmacsha256"

    mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_SERVER, MQTT_PORT,MQTT_USER_NAME, MQTTT_PASSWORD, 60)
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.connect()

def mqtt_report(client, color, name, switch, brightness):

    msg = {
        "method": "report",
        "clientToken": "clientToken-2444532211",
        "params": {
            "color": color,
            "color_temp": 0,
            "name": name,
            "power_switch": switch,
            "brightness": brightness
        }   
    }

    client.publish(MQTT_CONTROL_REPLY_TOPIC.encode(), ujson.dumps(msg).encode())

async def light_loop():
    global led, relay, button
    global color, name, brightness, light_changed

    switch_status_last = 1
    LED_status = 0  

    color = 2   #blue
    brightness = 100    #here 100% == 1
    led.rgb_light(0, 0, 255, brightness/100.0)

    # ??????????????????LED??????????????????
    # while True:
    #     relay.set_on()
    #     await uasyncio.sleep_ms(2000)
    #     relay.set_off()
    #     await uasyncio.sleep_ms(2000)

    time_cnt = 0
    change_cnt = 0
    twinkle_cnt = 0
    twinkle_cycle = 20


    mqtt_client.subscribe(MQTT_CONTROL_TOPIC.encode())

    while True:
        if change_cnt > 0:
            change_cnt -= 1
        mqtt_client.check_msg()

        switch_status = button.state()
        LED_status = relay.state()
        if switch_status != switch_status_last:
            if switch_status == 0 and switch_status_last == 1:
                LED_status = 0 if LED_status else 1
            relay.set_state(LED_status)
            switch_status_last = switch_status
        
        if light_changed:
            light_changed = False
            change_cnt = 3 * twinkle_cycle
            twinkle_cnt = 0
            led.rgb_light(255 if color==0 else 0, 255 if color==1 else 0, 255 if color==2 else 0, brightness/100.0)

        if change_cnt == 0:
            if twinkle_cnt >= 6 * twinkle_cycle:
                twinkle_cnt = 0 
            elif (twinkle_cnt // twinkle_cycle) == 0:
                led.rgb_light(255, 0 ,0 ,0.1)
                twinkle_cnt += 1
            elif (twinkle_cnt // twinkle_cycle) <= 2:
                led.rgb_light(0, 255, 0, 0.5)
                twinkle_cnt += 1
            elif (twinkle_cnt // twinkle_cycle) <= 5:
                led.rgb_light(0, 0, 255, 1.0)
                twinkle_cnt += 1



        # ?????????0.02*100=2???????????????
        if time_cnt >= 100:
            mqtt_report(mqtt_client, color, name, LED_status, brightness)
            time_cnt = 0
        time_cnt = time_cnt+1
        await uasyncio.sleep_ms(20)# ???????????????????????????50ms???????????????????????????????????????????????????????????????????????????????????????

async def main():
    global mqtt_client

    # Wi-Fi connection
    try:
        await uasyncio.wait_for(wifi_connect(WIFI_AP_SSID, WIFI_AP_PSW), 20)
    except uasyncio.TimeoutError:
        print("wifi connected timeout!")
    
    # MQTT connection
    try:
        await uasyncio.wait_for(mqtt_connect(), 20)
    except uasyncio.TimeoutError:
        print("mqtt connected timeout!")

    await uasyncio.gather(light_loop())

uasyncio.run(main())