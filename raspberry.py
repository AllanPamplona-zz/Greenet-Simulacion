import paho.mqtt.client as mqtt
import schedule
import time
import pika
import json
import threading
import pyrebase

# TODO: REFACTOR DE TODO ESTO
userId = "5ee50e159926985894ea56c3"
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

broker_address = "localhost"
broker_port = 1883

def report(message, water):
    msg = {
            "temperatura": str(message.decode('utf-8'))+'°C',
            "user": userId
            }
    if(water):
        msg["extra"] = "Se regó la planta por altas temperaturas"
    channel.basic_publish(exchange='',
                      routing_key='notification',
                      body=json.dumps(msg))

def on_message(client, userdata, message):
    if message.topic=="arduino/status":
        if int(message.payload.decode('utf-8')) > 30:
            client.publish("setWater", "ON")
            report(message.payload, True)    
        else:
            report(message.payload, False)

def verifyTemp():
    client.publish("arduino/getStatus")

def request(command):
    if command == 'getStatus':
        verifyTemp()

client = mqtt.Client('Raspberry') 
client.on_message = on_message 
client.connect(broker_address, broker_port, 60) 
client.subscribe("arduino/status")
client.loop_start()

config = {  "apiKey": "",  "authDomain":
        "","databaseURL": "","storageBucket":  "",  "serviceAccount": "iot.json" } 

firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
auth = firebase.auth()
db = firebase.database()

def stream_handler(message):
    if 'method' in message["data"]:
        event = message["data"]
        request(event["method"])

my_stream = db.child("user/"+userId).stream(stream_handler)
schedule.every(1).minutes.do(verifyTemp)
while True:
    schedule.run_pending()
    time.sleep(1)
