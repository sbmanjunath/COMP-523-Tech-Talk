import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True) # Establish connection to redis

# Waits to send messages to the channel
while True:
    print("What message do you want to send?")
    message = input()
    r.publish('notifications', message) # Publishes message to notifications channel