import redis
import random
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Simulated user pool
users = [f"user{i}" for i in range(1, 51)]

def simulate_chat():
    while True:
        user = random.choice(users)

        # Increment global message count
        r.incr("total_messages")

        # Increment user-specific message count
        r.zincrby("user_message_counts", 1, user)

        # Track active user with TTL of 1 minute
        r.setex(f"active_user:{user}", 60, 1)

        time.sleep(random.uniform(0.2, 1.2))  # Simulate messages at random intervals

if __name__ == "__main__":
    simulate_chat()
