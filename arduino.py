import paho.mqtt.client as mqtt
import time
import random

broker_address = "mosquitto"
broker_port = 1883

def on_message(client, userdata, message):
    if message.topic=="arduino/getStatus":
        val = random.randint(0,100) 
        msg = format(val)
        client.publish("arduino/status",msg)

client = mqtt.Client('Arduino') 
client.on_message = on_message 
client.connect(broker_address, broker_port, 60) 
client.subscribe("arduino/getStatus") # Subscripción al topic
client.loop_forever()
