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
import time

from bleak import BleakClient
from bleak.exc import BleakError
import winsound


from win32api import GetSystemMetrics, Sleep
import win32gui
import win32api
import win32con
import serial
import pygame
import keyboard
import math


#ADDRESS = "A8:1B:6A:B3:53:86" #bluetooth in protoboard password 123456
ADDRESS = "50:F1:4A:6E:67:6D" #soldado 

pygame.init()
pygame.mixer.init()

soundPath = "C:\\projects\\gestures\\python\\sounds\\"

sounds = [ 
    (pygame.mixer.Sound(soundPath + "dum.wav"), pygame.mixer.Sound(soundPath + "tac.wav") ),
    (pygame.mixer.Sound(soundPath + "4b.wav"), pygame.mixer.Sound(soundPath + "4c.wav") ), 
    (pygame.mixer.Sound(soundPath + "12a.wav"), pygame.mixer.Sound(soundPath + "12b.wav") ) # lados campanas 
    # frente abajo
     #izq der
    #(pygame.mixer.Sound(soundPath + "5.wav"), pygame.mixer.Sound(soundPath + "6a.wav") ),# frente y atras
    #(pygame.mixer.Sound(soundPath + "11c.wav"), pygame.mixer.Sound(soundPath + "11d.wav") ),
    #(pygame.mixer.Sound(soundPath + "13a.wav"), pygame.mixer.Sound(soundPath + "13b.wav") )
]
soundsFlags = [ 
    (False,False),
    (False,False),
    (False,False),
    (False,False),
    (False,False),
    (False,False) 
]
soundsLevels = [ 
    (-10000,10000),
    (-10000,10000),
    (-10000,10000),
    (-10000,10000),
    (-10000,10000),
    (-10000,10000), 
]

soundLastTime = [ 0, 0, 0, 0, 0, 0]
setup = False
setupAverages = [0,0,0,0,0,0]
setupAggregates = [0,0,0,0,0,0]
setupNumReads = 0







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
            0,0,900,900, 0, 0, 0, None)

        return hwnd

wincreator = WindowCreator()

hwnd = wincreator.create_window(0)

dc = win32gui.GetDC(hwnd)

red = win32api.RGB(255, 0, 0)

clientRect = win32gui.GetClientRect(hwnd)
whiteColor = win32api.RGB(255,255,255)
whiteBrush = win32gui.CreateSolidBrush(whiteColor)
redColor = win32api.RGB(255,0,0)
redBrush = win32gui.CreateSolidBrush(redColor)
blackColor = win32api.RGB(0,0,0)
blackBrush = win32gui.CreateSolidBrush(blackColor)

win32gui.FillRect(dc, clientRect, whiteColor)


    

colors = [ 
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(255,0,0)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,255,0)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,0,255)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,0,0)),
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(0,255,255)), #light blue 0, 255, 255
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(255,255,0)), #yellow 255,255,0
    win32gui.CreatePen(win32con.PS_SOLID,0,win32api.RGB(125,125,125)) #gray
]



i=0


previousTime = 0
currentPosX = int(clientRect[2]/2)
currentPosY = int(clientRect[3]/2)

soundIsActivated = False



lastpos = [
            (0, int(clientRect[3]/2)),
            (0, int(clientRect[3]/2)),
            (0, int(clientRect[3]/2)),
            (0, int(clientRect[3]/2)),
            (0, int(clientRect[3]/2)),
            (0, int(clientRect[3]/2)),
            (0, int(clientRect[3]/2))
        ]

buttonLastPushTime = 0
buttonIsActive = False

import queue
q1 = queue.Queue()
message = ""





#SERVICEID="0000ffe0-0000-1000-8000-00805f9b34fb"
#UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
               
UART_RX_CHAR_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"
leftSide = 0
leftTime = 0

gr = False
memoryfileRight=open('C:\\projects\\gestures\\python\\sounds\\right.wav',"rb")
memoryRight = memoryfileRight.read()

gl = False
memoryfileLeft=open('C:\\projects\\gestures\\python\\sounds\\left.wav',"rb")
memoryLeft = memoryfileLeft.read()


gu = False
memoryfileUp=open('C:\\projects\\gestures\\python\\sounds\\up.wav',"rb")
memoryUp = memoryfileUp.read()

gd = False
memoryfileDown=open('C:\\projects\\gestures\\python\\sounds\\down.wav',"rb")
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
    global clientRect
    global whiteColor
    global blackColor
    global redColor
    global whiteBrush
    global blackBrush
    global redBrush    
    #global ser
    global pygame
    global soundsFlags
    global sounds
    global lastpos
    global colors
    global soundsLevels
    global setup
    global setupAverages
    global setupAggregates
    global setupNumReads
    global keyboard
    global numLearningReads
    global soundLastTime
    global currentPosX
    global currentPosY
    global previousTime
    global soundIsActivated
    global buttonLastPushTime
    global buttonIsActive

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
                if( len(parts) == 8):
                    #print_there( 1,1,f"{parts}")
                    

                    
                    print(f"{parts[0]},{parts[1]},{parts[2]},{parts[3]},{parts[4]},{parts[5]},{parts[6]},{parts[7]}")
                    (timestr, str_girox, str_giroy, str_giroz, str_accelx,str_accely,str_accelz,str_buttonStatus) = parts
                     
                    currentTime = int(timestr)

                    giroX = int(str_girox) 
                    giroY = int(str_giroy) 
                    giroZ = int(str_giroz)

                    
                    accelX = int(str_accelx) 
                    accelY = int(str_accely) 
                    accelZ = int(str_accelz) 

                    buttonStatus = int(str_buttonStatus)

                    
                    if previousTime == 0:
                            previousTime = currentTime
                    ( screenX, screenY, screenWidth, screenHeight) = clientRect 
                    
                    
                    #if we are startin or have reach the end of the screen clean and restart
                    if( i==0 or i >= screenWidth ):
                        i = 0
                        for j in range(len(lastpos)):
                            lastpos[j] = (0, int(screenHeight/2))

                        #reset the screen
                        win32gui.FillRect(dc, clientRect, whiteBrush)

                        win32gui.SelectObject(dc, blackColor)

                        win32gui.MoveToEx(dc, 0, int(screenHeight/2) )
                        win32gui.LineTo(dc, screenWidth, int(screenHeight/2) )

                        win32gui.MoveToEx(dc, 0, int(screenHeight/2 - 250) )
                        win32gui.LineTo(dc,  screenWidth,  int(screenHeight/2 - 250) )
                        
                        win32gui.MoveToEx(dc, 0, int(screenHeight/2 + 250) )
                        win32gui.LineTo(dc,  screenWidth,  int(screenHeight/2 + 250) )

                    #imprime los valores raw
                    win32gui.SelectObject(dc, blackColor)

                    fontSize = 13
                    lf = win32gui.LOGFONT()
                    lf.lfFaceName = "Stencil"
                    lf.lfHeight = fontSize
                    lf.lfWeight = 600

                    lf.lfQuality = win32con.NONANTIALIASED_QUALITY
                    hf = win32gui.CreateFontIndirect(lf)
                    win32gui.SelectObject(dc, hf) 
                    win32gui.FillRect(dc, (0,0,screenWidth, 100), whiteBrush)                           
                    win32gui.DrawText(dc, f"giroX:{giroX:05}" , -1, (  0,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"giroY:{giroY:05}" , -1, (100,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"giroZ:{giroZ:05}" , -1, (200,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"accelX:{accelX:05}" , -1, (400,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"accelY:{accelY:05}" , -1, (500,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"accelZ:{accelZ:05}" , -1, (600,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"str_buttonStatus:{str_buttonStatus}" , -1, (700,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )


#                    dancer =  (int(currentPosX) , int(currentPosY), int(currentPosX + 20), int(currentPosY + 20))
#                    win32gui.FillRect(dc, dancer, redBrush)



                    #grafica los valores escalados    
                    try:
                        for j in range(len(lastpos)):   
                            x , y = lastpos[j]

                            win32gui.MoveToEx(dc, x, y)
                            win32gui.SelectObject(dc, colors[j])
                            val:int = 0
                            if j >=0 and j<3 : #giroscopio
                                val = int(parts[j+1]) * (250.0/32768.0)
                            if j >=3 and j<=5 : #acelerometer
                                val = (int(parts[j+1]) / 32768.0)*100
                            if j == 6:                                 
                                val = int(parts[j+1]) * 100

                            win32gui.LineTo(dc, i, int(val + screenHeight/2 ) )
                            lastpos[j] = (i,int(val + int(screenHeight/2)) )
                        i = i + 1

                    except Exception as e:
                        print(f"error:{e}")
                        exit()

                    if buttonStatus==0 and (currentTime - 1000) > buttonLastPushTime:
                        buttonLastPushTime = currentTime
                        buttonIsActive = not buttonIsActive

                    
                    """
                    #start setup 
                    if keyboard.is_pressed('i') and setup == False:
                        setup = True
                        setupNumReads = 0
                        for k in range(len(setupAggregates)):
                            setupAggregates[k] = 0
                        print(f"setup averages >>>>>>>>>>>>>>>")
                    elif  setup == True and setupNumReads < 100:
                        for k in range(len(setupAggregates)):
                            setupAggregates[k] = setupAggregates[k] + int(parts[k+1])
                        setupNumReads = setupNumReads + 1
                    elif setup == True and setupNumReads>= 100:
                        print("______________________ averages ")
                        for k in range(len(setupAggregates)):
                            setupAverages[k] = setupAggregates[k]/setupNumReads
                            print(f"average {k} {setupAverages[k]}")
                        time.sleep(5)
                        setup = False

                    

                    #start setup 
                    if keyboard.is_pressed('a') and setup == False:
                        soundIsActivated = True
                        print(f"Activate >>>>>>>>>>>>>>>")  

                    if soundIsActivated == True or True:
                        
                        #I wnat to know if is moving
                        #first calculate the component to the ground
                       
                        acc_lsb_to_g = 16384.0
                        gX = accelX / acc_lsb_to_g
                        gY = accelY / acc_lsb_to_g
                        gZ = accelZ / acc_lsb_to_g

                        sgZ:float = (accelZ>=0)-(accelZ<0); # allow one angle to go from -180 to +180 degrees
                        RAD_2_DEG=57.29578 # [deg/rad]
                        angleAccX =   math.atan2(gX, sgZ*math.sqrt(gZ*gZ + gX*gX)) * RAD_2_DEG; # [-180,+180] deg
                        angleAccY =  - math.atan2(gX,math.sqrt(gZ*gZ + gY*gY)) * RAD_2_DEG;# [- 90,+ 90] deg

                        
                        win32gui.FillRect(dc, (0,100,screenWidth, 100), whiteBrush)                           
                        win32gui.DrawText(dc, f"{angleAccX:06.2f}" , -1, (  0,100,0,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )                        
                        win32gui.DrawText(dc, f"{angleAccY:06.2f}" , -1, (  100,100,0,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )                        

                        #need to calculate displacement in the x position
                        
                        distanceX = (accelX - setupAverages[3]) * (pow((currentTime-previousTime)/1000,2))
                        win32gui.DrawText(dc, f"{distanceX:06.2f}" , -1, (  0,300,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )                        
                        distanceG =  (accelZ - setupAverages[5]) * (pow((currentTime-previousTime)/1000,2))
                        win32gui.DrawText(dc, f"{distanceG:06.2f}" , -1, (  100,300,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )                        
                        currentPosX = currentPosX + distanceX + distanceG                                                   
                        win32gui.DrawText(dc, f"{currentPosX:06.2f}" , -1, (  300,300,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )                        
                        
                    """



                         
                    try:    
                        if buttonIsActive:   
                            l = len(sounds)
                            t = currentTime
                            for s in range(l):
                                v = int(parts[1+s])
                                (sd, su) = sounds[s]
                                (fd, fu) = soundsFlags[s]
                                (lowLevel,highLevel) = soundsLevels[s]
                                """
                                if setup == True:
                                    if keyboard.is_pressed('s'):  # if key 'q' is pressed 
                                            
                                            print('starting!')
                                            for d in range(l):
                                                print( soundsLevels[d] )
                                            time.sleep(3)
                                            setup = False

                                    if lowLevel == 0:
                                        lowLevel = v
                                    if highLevel == 0:
                                        highLevel = v
                                    if v < lowLevel :
                                        lowLevel = v
                                    elif v > highLevel :
                                        highLevel = v

                                    soundsLevels[s] = (lowLevel, highLevel)
                                    continue
                                """
                                if  (fd == False or soundLastTime[s] < t-400) and v < lowLevel  :
                                    fd = True
                                    soundsFlags[s] = (fd,fu)
                                    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                                    #winsound.PlaySound(memoryRight, winsound.SND_MEMORY | winsound.SND_NOWAIT )
                                    #winsound.PlaySound(memoryRight, winsound.SND_NOSTOP | winsound.SND_MEMORY )
                                    pygame.mixer.find_channel().play(sd)
                                    soundLastTime[s] = t
                                    #ser.write(b'a')
                                elif fd == True and v > lowLevel:
                                    fd = False
                                    soundsFlags[s] = (fd, fu)

                            
                                if (fu == False or soundLastTime[s] < t-400) and  v > highLevel:
                                    fu =True
                                    soundsFlags[s] = (fd, fu)
                                    
                                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                    pygame.mixer.find_channel().play(su)
                                    soundLastTime[s] = int(parts[0])
                                    
                                    #winsound.PlaySound("C:\\projects\\gestures\\python\\reader\\right.wav", winsound.SND_ASYNC |  winsound.SND_FILENAME)

                                elif fu == True and v < highLevel:
                                    fu = False
                                    soundsFlags[s] = (fd, fu)
                
                    except Exception as e1:
                        print(f"{e1} s:{s}")
                        
                    #this should be the last line
                    previousTime = currentTime                    
                    
                else: 
                    print( f"len: {len(parts)}  {message}" )
                message = ""
                
    except Exception as e:
        print(f'error outer:{e}') 
        exit(1)   
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
