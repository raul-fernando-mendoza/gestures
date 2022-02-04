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
import numpy as np
from scipy.optimize import curve_fit
import numpy 

ADDRESS = "A8:1B:6A:B3:53:86" #bluetooth MLT-BT05 in protoboard password 123456
#ADDRESS = "50:F1:4A:6E:67:6D" #soldado 




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
setupNoiseLevelsDown = [None] * 6
setupNoiseLevelsUp = [None] * 6

soundLastTime = [ 0, 0, 0, 0, 0, 0]
setup = True
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
            'BLE-05 connection!',
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

#Fitting curve variables
fitting_x_values  = [] 
fitting_y_values  = [] 
fitting_current_slop = 0 
fitting_previous_slop = 0
fitting_max = 0
fitting_min = 0


max_time = 0
min_value = 0
max_value = 0 
MIN_DIFF = 3000
# define the true objective function
def objective(x, a, b, c):
	return numpy.sin((x * (3.1416))/(max_time)  + a) * (max_value-min_value) * b + c


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
    global setupNoiseLevelsUp
    global setupNoiseLevelsDown
    global setup
    global setupAverages
    global setupAggregates
    global setupNumReads
    global keyboard
    global soundLastTime
    global currentPosX
    global currentPosY
    global previousTime
    global soundIsActivated
    global buttonLastPushTime
    global buttonIsActive
    global fitting_x_values
    global fitting_y_values
    global fitting_previous_slop
    global fitting_current_slop
    global fitting_max 
    global fitting_min
    global max_time
    global min_value
    global max_value
    global MIN_DIFF 

    
    TIME = 0
    GIROX = 1
    GIROY = 2
    GIROZ = 3
    ACCEX = 4
    ACCEY = 5
    ACCEZ = 6  
    BUTTON = 7  

    
    MAX_READS = 30

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
                    values = [0] * 8
                    for j in range(0,8):
                        if j == TIME:
                            values[j] = int(parts[j])
                        elif j >= GIROX and j <=GIROZ:                            
                            if setupNoiseLevelsUp[j-1] != None and int(parts[j]) > setupNoiseLevelsUp[j-1]:
                                values[j]  = (int(parts[j]) -setupNoiseLevelsUp[j-1]) #* (250.0/32768.0)  
                            elif setupNoiseLevelsDown[j-1] != None and int(parts[j-1]) < setupNoiseLevelsDown[j-1]: 
                                values[j]  = (int(parts[j])- setupNoiseLevelsDown[j-1]) #* (250.0/32768.0)
                            else:
                                values[j]  = int(parts[j]) # * (250.0/32768.0)
                        elif j >=ACCEX and j <=ACCEZ:
                            if setupNoiseLevelsUp[j-1] != None and int(parts[j]) > setupNoiseLevelsUp[j-1]:
                                values[j]  = (int(parts[j]) -setupNoiseLevelsUp[j-1]) / 32768.0  
                            elif setupNoiseLevelsDown[j-1] != None and int(parts[j]) < setupNoiseLevelsDown[j-1]: 
                                values[j]  = (int(parts[j])- setupNoiseLevelsDown[j-1]) / 32768.0
                            else:
                                values[j]  = int(parts[j]) / 32768.0
                        elif j == BUTTON:
                            values[BUTTON] = int(parts[BUTTON])

                     
                    currentTime = values[TIME]

                    buttonStatus = values[BUTTON]

                    #add fitting values
                    if len( fitting_x_values) >= MAX_READS:
                        del fitting_x_values[0]
                        del fitting_y_values[0]
                    fitting_x_values.append(currentTime)
                    fitting_y_values.append(values[GIROZ])  

                    currentValue = 0.0
                    nextValue = 0.0

                    #creating fitting curve 
                    if len( fitting_x_values) >= MAX_READS:
                        fitting_times_converted = [0] * len(fitting_x_values)
                        fitting_values_converted = [0] * len(fitting_x_values)
                        startTime = fitting_x_values[0]
                        for j in range(len(fitting_times_converted)):
                            fitting_times_converted[j] = fitting_x_values[j] - startTime
                            if j == 0 :
                                fitting_values_converted[j] = fitting_times_converted[j+1] * fitting_y_values[j]
                            else:
                                fitting_values_converted[j] = (fitting_times_converted[j] - fitting_times_converted[j-1]) * fitting_y_values[j]
                        
                        max_time = max(fitting_times_converted)
                        min_value = min(fitting_values_converted)
                        max_value = max(fitting_values_converted)
                        popt, pcov  = curve_fit(objective, fitting_times_converted, fitting_values_converted)
                        a, b, c = popt
                        #print('a=%.5f b=%.5f + c=%.5f' % (a, b, c))
                        #calculate next value
                        lastTime = fitting_times_converted[ len(fitting_times_converted) - 1]
                        currentValue = objective( lastTime, a, b , c)
                        nextValue = objective( lastTime + 10, a, b , c)
                        
                        if nextValue > currentValue:
                            fitting_current_slop = 1
                        elif nextValue < currentValue: 
                            fitting_current_slop = -1 
                        else: 
                            fitting_current_slop = 0
                    if fitting_current_slop == fitting_previous_slop:
                        if values[GIROZ] < fitting_min:
                            fitting_min = values[GIROZ]
                        elif values[GIROZ] > fitting_max:
                            fitting_max = values[GIROZ]                             

                    if buttonIsActive:
                        #print(f"{parts[0]}\t{parts[1]}\t{parts[2]}\t{parts[3]}\t{parts[4]}\t{parts[5]}\t{parts[6]}\t{parts[7]}\t{int(currentValue):04}\t{int(nextValue):04}\t{fitting_current_slop}\t{fitting_max:05}\t{fitting_min:05}")
                        print(f"{values[0]}\t{values[1]:06.1f}\t{values[2]:06.1f}\t{values[3]:06.1f}\t{values[4]:06.1f}\t{values[5]:06.1f}\t{values[6]:06.1f}\t{values[7]}\t{int(currentValue):05}\t{int(nextValue):05}\t{fitting_current_slop}\t{fitting_max:05.1f}\t{fitting_min:05.1f}")
                    
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

                        win32gui.MoveToEx(dc, 0, int(screenHeight/2 + MIN_DIFF * (250.0/32768.0)) )
                        win32gui.LineTo(dc,  screenWidth,  int(screenHeight/2 + MIN_DIFF * (250.0/32768.0)) )

                        win32gui.MoveToEx(dc, 0, int(screenHeight/2 - MIN_DIFF * (250.0/32768.0)) )
                        win32gui.LineTo(dc,  screenWidth,  int(screenHeight/2 - MIN_DIFF * (250.0/32768.0)) )
                        

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
                    win32gui.DrawText(dc, f"giroX:{values[GIROX]:05}" , -1, (  0,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"giroY:{values[GIROY]:05}" , -1, (100,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"giroZ:{values[GIROZ]:05}" , -1, (200,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"accelX:{values[ACCEX]:05}" , -1, (400,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"accelY:{values[ACCEY]:05}" , -1, (500,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"accelZ:{values[ACCEZ]:05}" , -1, (600,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )
                    win32gui.DrawText(dc, f"str_buttonStatus:{values[BUTTON]}" , -1, (700,0,100,100) , win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS )


#                    dancer =  (int(currentPosX) , int(currentPosY), int(currentPosX + 20), int(currentPosY + 20))
#                    win32gui.FillRect(dc, dancer, redBrush)



                    #grafica los valores escalados
                    if buttonIsActive:    
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

                    if (buttonStatus==0 and (currentTime - 1000) > buttonLastPushTime) or keyboard.is_pressed('b'):
                        buttonLastPushTime = currentTime
                        buttonIsActive = not buttonIsActive
                        print("button changed")
                        time.sleep(2)

                    if keyboard.is_pressed('s') and setup == False:   
                        setup = True
                        setupNumReads = 0
                        print('Setup starting!')

                    if keyboard.is_pressed('u'):   
                        MIN_DIFF += 10

                    if keyboard.is_pressed('d'):   
                        MIN_DIFF -= 10

                    if setup == True and setupNumReads<100:
                        for n in range(len(setupNoiseLevelsDown)):
                            v = int(parts[n+1])

                            if setupNoiseLevelsDown[n] == None:
                                setupNoiseLevelsDown[n] = v
                            if setupNoiseLevelsUp[n] == None:
                                setupNoiseLevelsUp[n] = v
                            if v < setupNoiseLevelsDown[n] :
                                setupNoiseLevelsDown[n] = v
                            elif v > setupNoiseLevelsUp[n] :
                                setupNoiseLevelsUp[n] = v

                            setupNumReads += 1 
                    if setup == True and setupNumReads>=100:
                        setup = False
                        print("noise levels")
                        for n in range(len(setupNoiseLevelsUp)):
                            print(f"{setupNoiseLevelsDown[n]:05} - {setupNoiseLevelsUp[n]:05}")
                        time.sleep(5)
                    """
                    # lee 100 valores los agrega y saca el promedio en setupAverages                    
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

                    

                    #active sound 
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


                    
                    #Play sounds                          
                    try:    
                        if buttonIsActive:   
                            (sd, su) = sounds[0]
                            if  (fitting_previous_slop == -1 and fitting_current_slop == 1 and fitting_min<-MIN_DIFF and fitting_max-fitting_min> MIN_DIFF) :
                                print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< {fitting_max} - {fitting_min} >")
                                #winsound.PlaySound(memoryRight, winsound.SND_MEMORY | winsound.SND_NOWAIT )
                                #winsound.PlaySound(memoryRight, winsound.SND_NOSTOP | winsound.SND_MEMORY )
                                pygame.mixer.find_channel().play(sd)

                            if (fitting_previous_slop == 1 and fitting_current_slop == -1 and fitting_max>MIN_DIFF and fitting_max-fitting_min> MIN_DIFF):
                                print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {fitting_max} - {fitting_min}")
                                pygame.mixer.find_channel().play(su)
                    except Exception as e1:
                        print(f"SOUND {e1}")
                    

                    #this should be the last line
                    previousTime = currentTime  
                    
                    if fitting_current_slop != fitting_previous_slop:
                        fitting_min = values[GIROZ]
                        fitting_max = values[GIROZ]
                    fitting_previous_slop = fitting_current_slop                                    
                    
                else: 
                    print( f"len: {len(parts)}  {message}" )
                message = ""
                
    except Exception as e:
        print(f'error outer:{e}') 
        #sexit(1)   
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
