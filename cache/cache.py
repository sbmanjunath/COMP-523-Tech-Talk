import time
import redis

# Connect to Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def slow_function(n):
    """Simulates a time-consuming computation"""
    print(f"Computing square of {n}...")
    time.sleep(3) # time delay to simulate api call access
    return n * n

def get_cached_result(n):
    key = f"square:{n}"
    
    # Try fetching from Redis cache
    cached = cache.get(key)
    if cached:
        print("Cache hit!")
        return int(cached)
    
    # If not found, compute and store in cache
    print("Cache miss. Computing...")
    result = slow_function(n)
    cache.set(key, result, ex=10)  # Store with 10 sec expiry
    return result

# Try it
if __name__ == "__main__":
    num = 81
    print("First call:")
    start_time = time.time()
    print(get_cached_result(num))  # Cache miss
    end_time = time.time()
    print(f"Response time = {end_time-start_time} sec")
    print("\nSecond call:")
    start_time = time.time()
    print(get_cached_result(num))  # Cache hit
    end_time = time.time()
    print(f"Response time = {end_time-start_time} sec")