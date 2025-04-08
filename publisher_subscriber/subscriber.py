import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True) # Establish connection to redis

p = r.pubsub(ignore_subscribe_messages=True) # Create Pub/Sub object

p.subscribe('notifications') # Subscribes to desired channel

# Waits to recieve message
while True:
    message = p.get_message() # Polls redis to see if any new messages have come in, returns None if not
    if message:
        print("New Message from " + message['channel'] + ": " + message['data'])
    time.sleep(0.001)