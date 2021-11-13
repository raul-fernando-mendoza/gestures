"""
Services
----------------

An example showing how to fetch all services and print them.

Updated on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

"""

from os import read
import sys
import asyncio
import platform

from bleak import BleakClient
from bleak.exc import BleakError
import winsound


from win32api import GetSystemMetrics
import win32gui
import win32api
width = GetSystemMetrics (0)
height = GetSystemMetrics (1)
print(f"Screen resolution = {width} {height}");
dc = win32gui.GetDC(0)
red = win32api.RGB(255, 0, 0)
i=0


import queue
q1 = queue.Queue()
message = ""




ADDRESS = "A8:1B:6A:B3:53:86"


#UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
               
UART_RX_CHAR_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"
leftSide = 0
leftTime = 0

gr = False
memoryfileRight=open('C:\\projects\\gestures\\python\\reader\\right.wav',"rb")
memoryRight = memoryfileRight.read()

gl = False
memoryfileLeft=open('C:\\projects\\gestures\\python\\reader\\left.wav',"rb")
memoryLeft = memoryfileLeft.read()


gu = False
memoryfileUp=open('C:\\projects\\gestures\\python\\reader\\up.wav',"rb")
memoryUp = memoryfileUp.read()

gd = False
memoryfileDown=open('C:\\projects\\gestures\\python\\reader\\down.wav',"rb")
memoryDown = memoryfileDown.read()



def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()

def notification_handler(num:int, msg:bytearray):
    try:
        msg:str = "".join(map(chr, msg))
        #msg = msg.strip()
        global q1
        global message
        global leftSide
        global memoryLeft
        global memoryRight
        global memoryUp
        global memoryDown

        global leftTime
        global i
        global width
        global height
        global red
        global dc
        global gr
        global gl
        global gu
        global gd

        process = False

        #print(f"({msg})")
        #first put the message in the queu
        for c in msg:
            q1.put(c)

        while q1.empty() == False: 
            c = q1.get()
            
            if c == '\r' or c=='\n':
                if c=='\r':
                    None
                else:
                    process = True 
                    print(f"line:{message}\n")          
            else:
                message = message + c
                process = False

            if process == True:
                
                parts = message.split("\t")
                if( len(parts) == 7):
                    #print_there( 1,1,f"{parts}")
                    print(f"{parts}")
                    if( i < 1024):

                        xgiro:int = int( (int(parts[1])/(32768/256)) + (height/2) ) 
                        win32gui.SetPixel(dc, i, xgiro, red) 
                        i = i + 1
                    else:
                        i = 0
                    
                    #r.set(ADDRESS, msg)
                    t = int(parts[0])
                    gz = int(parts[3])
                    
                    
                    if  gr == False and gz < -17000:
                        gr = True
                        winsound.PlaySound(memoryRight, winsound.SND_MEMORY | winsound.SND_NOWAIT)
                    elif gr == True and gz > -17000:
                        gr = False

                    if gl == False and  gz > 17000:
                        gl = True
                        winsound.PlaySound(memoryLeft, winsound.SND_MEMORY | winsound.SND_NOWAIT)
                    elif gl == True and gz < 17000:
                        gl = False 
                    
                    """
                    gx = int(parts[1] )

                    if gu == False  and gx < -17000:
                        gu = True
                        winsound.PlaySound(memoryUp, winsound.SND_MEMORY | winsound.SND_NOWAIT)
                    if gu == True and gx > -17000:
                        gu = False

                    if gd == False  and  gx > 17000:
                        gd = True
                        winsound.PlaySound(memoryDown, winsound.SND_MEMORY | winsound.SND_NOWAIT)
                    if gd == True and gx < 17000:
                        gd = False 
                    """                                   
                    
                else: 
                    print( f"len: {len(parts)}" )
                message = ""
    except Exception as e:
        print("error converting to integer:" + e)    
    #    #winsound.PlaySound("C://projects//gestures//python//reader//mixkit-drum-and-percussion-545.wav", False)
    #elif near == True and int(msg) > 17 : 
    #    near = False


async def print_services(mac_addr: str):
    global x
    async with BleakClient(mac_addr) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service.description) 
            for c in service.characteristics:
                print(f"\t {c.description} {c.properties} ")                       
        try:
            text = ""
            #l = await client.read_gatt_char(UART_RX_CHAR_UUID)
            #print("read: {0}".format("".join(map(chr, l))))
            await client.start_notify(UART_RX_CHAR_UUID, notification_handler)
        
            
            try:
                while True:
                    await asyncio.sleep(0.1, loop=loop)  # Sleeping just to make sure the response is not missed...;
                    
            except KeyboardInterrupt:
                   await client.stop_notify(UART_RX_CHAR_UUID)            
            
        except BleakError as e:
            print("BleakError" + str(e) )
        except TimeoutError as e:
            print("timeout error")
        except Exception as e:
            print("EXEPTION" + str(e) )
        finally:
            await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(ADDRESS))
