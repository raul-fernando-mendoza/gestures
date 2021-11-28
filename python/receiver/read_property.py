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


from win32api import GetSystemMetrics, Sleep
import win32gui
import win32api
import win32con
import serial
import pygame

pygame.init()
pygame.mixer.init()

good1 = pygame.mixer.Sound("C:\\projects\\gestures\\python\\reader\\right.wav")
good2 = pygame.mixer.Sound("C:\\projects\\gestures\\python\\reader\\left.wav")

pygame.mixer.find_channel().play(good1)

pygame.mixer.find_channel().play(good2)

#Sleep(3000)



#ser = serial.Serial('COM4')
#print(ser.name) 
#ser.write(b'a')
#ser.close()  
#exit(1)

width = GetSystemMetrics (0)
height = GetSystemMetrics (1)
print(f"Screen resolution = {width} {height}")


#create window
class WindowCreator:
    def create_window(self,hwndparent):
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = 'test_win32gui_1'
        wc.style =  win32con.CS_GLOBALCLASS|win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hbrBackground = win32con.COLOR_WINDOW+1
        #wc.lpfnWndProc=wndproc_1
        class_atom=win32gui.RegisterClass(wc)       
        hwnd = win32gui.CreateWindow(wc.lpszClassName,
            'Spin the Lobster!',
            win32con.WS_CAPTION|win32con.WS_VISIBLE,
            100,100,900,900, 0, 0, 0, None)

        return hwnd

wincreator = WindowCreator()

hwnd = wincreator.create_window(0)

dc = win32gui.GetDC(hwnd)
red = win32api.RGB(255, 0, 0)

rect = win32gui.GetClientRect(hwnd)
whiteColor = win32api.RGB(255,255,255)
brush = win32gui.CreateSolidBrush(whiteColor)

colors = [ 
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(255,0,0)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,255,0)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,0,255)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,0,0)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,255,255)), #light blue 0, 255, 255
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(255,255,0)) #yellow 255,255,0
]



i=0
win32gui.SetPixel(dc, 0, int(rect[3]/2), red)

lastpos = [
            (0, int(rect[3]/2)),
            (0, int(rect[3]/2)),
            (0, int(rect[3]/2)),
            (0, int(rect[3]/2)),
            (0, int(rect[3]/2)),
            (0, int(rect[3]/2))
        ]


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
    global hwnd
    global rect
    global whiteColor
    global brush
    global ser
    global pygame
    global good1
    global good2
    global lastpos
    global colors
    process = False

    try:
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
                    #print(f"line:{message}\n")          
            else:
                message = message + c
                process = False

            if process == True:
                
                parts = message.split("\t")
                if( len(parts) == 7):
                    #print_there( 1,1,f"{parts}")
                    print(f"{parts}")
                    if( i < rect[2] ):
                        
                        try:
                            for j in range(len(lastpos)):
                                x , y = lastpos[j]

                                win32gui.MoveToEx(dc, x, y)
                                win32gui.SelectObject(dc, colors[j])
                                val:int = int( (int(parts[j+1])/(32000/256)) + (800/2) )
                                #print(f'coordenadas:{i},{xgiro}') 
                                #win32gui.SetPixel(dc, i, xgiro, red) 
                                win32gui.LineTo(dc, i, val)
                                lastpos[j] = (i,val)
                        except Exception as e:
                            print(f"error setpixel:{e}")
                            exit()
                        i = i + 1
                    else:
                        i = 0
                        for j in range(0,len(lastpos) ):
                            lastpos[j] = (0, int(rect[3]/2))
                        win32gui.FillRect(dc, rect, brush)
                       

                        

                    
                    #r.set(ADDRESS, msg)
                    t = int(parts[0])
                    gz = int(parts[3])
                    
                    
                    if  gr == False and gz < -10000:
                        gr = True
                        print("****************************************************")
                        #winsound.PlaySound(memoryRight, winsound.SND_MEMORY | winsound.SND_NOWAIT )
                        #winsound.PlaySound(memoryRight, winsound.SND_NOSTOP | winsound.SND_MEMORY )
                        pygame.mixer.find_channel().play(good1)
                        #ser.write(b'a')
                    elif gr == True and gz > -10000:
                        gr = False

                    
                    if gl == False and  gz > 10000:
                        gl = True
                        pygame.mixer.find_channel().play(good2)
                        #winsound.PlaySound("C:\\projects\\gestures\\python\\reader\\right.wav", winsound.SND_ASYNC |  winsound.SND_FILENAME)

                    elif gl == True and gz < 10000:
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
        print(f'error outer:{e}')    
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
