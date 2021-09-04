import redis
import time

ADDRESS = "A8:1B:6A:B3:53:86"

r = redis.Redis(
    host='localhost',
    port=6379, 
    password=None)

print("starting\n")
try:
    while True:
        value = r.get(ADDRESS)
        if value:
            print(f"gesture found:{value}")
            r.delete(ADDRESS)
        

except KeyboardInterrupt:
        pass
    