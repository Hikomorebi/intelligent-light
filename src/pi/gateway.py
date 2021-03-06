from blescan import LightScanner, MiBeaconData

import time 
import asyncio
import json
import uuid
import paho.mqtt.client as MQTTClient

"""
QCloud Device Info
"""
DEVICE_NAME = "Lightsensor_1"
PRODUCT_ID = "OTPFS209VP"
DEVICE_KEY = "Vq768IJeXJrBIEzdnteVQw=="

"""
MQTT topic
"""
MQTT_CONTROL_TOPIC = "$thing/down/property/"+PRODUCT_ID+"/"+DEVICE_NAME
MQTT_CONTROL_REPLY_TOPIC = "$thing/up/property/"+PRODUCT_ID+"/"+DEVICE_NAME

def mqtt_callback(client, userdata, msg):
    # Callback
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

async def mqtt_connect():
    #connect callback
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    mqtt_client = None
    MQTT_SERVER = PRODUCT_ID + ".iotcloud.tencentdevices.com"
    MQTT_PORT = 1883
    MQTT_CLIENT_ID = PRODUCT_ID+DEVICE_NAME
    MQTT_USER_NAME = "OTPFS209VPLightsensor_1;12010126;FVO7F;1654699892"
    MQTTT_PASSWORD = "10a882943335d7f95be625a5a019017570e993f8b4e6ce6576cb75556062b47c;hmacsha256"

    mqtt_client = MQTTClient.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER_NAME, MQTTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    
    mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)

    return mqtt_client

def mqtt_report(client, light_level):
    client_token = "clientToken-" + str(uuid.uuid4())

    msg = {
        "method": "report",
        "clientToken": client_token,
        "params": {
            "Illuminance": light_level
        }
    }

    client.publish(MQTT_CONTROL_REPLY_TOPIC, json.dumps(msg))

async def light_loop(mclient):

    bles = LightScanner('Nodemcu')

    mclient.subscribe(MQTT_CONTROL_TOPIC)
    mclient.on_message = mqtt_callback

    mclient.loop_start()

    # while True:
    #     try:
    #         data = bles.status_update()
    #         #调用bles成员函数读取扫描到的光照强度数值
    #     except Exception as e:
    #         print("BLE SCAN error:", e)
    #         continue
        
	# 	#上传扫描到的光照强度数值
    #     mqtt_report(mclient,data.lightlevel)
        
    #     time.sleep(0.3)
    while True:
        try:
            data = bles.status_update()
        except Exception as e:
            print("BLE SCAN error:", e)
            continue
        mqtt_report(mclient,data.lightlevel)
        time.sleep(0.3)

async def main():
    mqtt_client = None
    # MQTT connection
    try:
        mqtt_client = await asyncio.wait_for(mqtt_connect(), 20)
    except asyncio.TimeoutError:
        print("mqtt connected timeout!")

    if mqtt_client is not None:
        await asyncio.gather(light_loop(mqtt_client))

asyncio.run(main())