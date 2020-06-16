import paho.mqtt.client as mqtt
import time

broker_address = "mosquitto"
broker_port = 1883
water_status = 'OFF'
def on_message(client, userdata, message):
    if message.topic=="setWater":
        water_status = str(message.payload.decode('utf-8'))
        print("Water is on")
        time.sleep(5)
        water_status = 'OFF'
        print("Water is off")

client = mqtt.Client('Water') 
client.on_message = on_message 
client.connect(broker_address, broker_port, 60) 
client.subscribe("setWater") # Subscripción al topic
client.loop_forever()
