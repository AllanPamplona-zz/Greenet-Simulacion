import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_publish(exchange='',
                      routing_key='request',
                      body='getStatus')
print(" [x] Sent 'Hello World!'")
connection.close()

