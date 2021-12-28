import redis
import time
import playsound

ADDRESS = "A8:1B:6A:B3:53:86"

r = redis.Redis(
    host='localhost',
    port=6379, 
    password=None)

near = False
print("starting\n")
try:
    while True:
        value = r.get(ADDRESS)
        if value:
            print(f"gesture found:{value}")
            
            if  near == False and int(value) < 15 :
                near = True
                playsound.playsound('C:\\projects\\gestures\\python\\reader\\mixkit-drum-and-percussion-545.wav', True)
            elif near == True and int(value) > 25 : 
                near = False

        

except KeyboardInterrupt:
        pass
    