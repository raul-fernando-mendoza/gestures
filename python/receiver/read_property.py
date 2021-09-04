"""
Services
----------------

An example showing how to fetch all services and print them.

Updated on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

"""

import sys
import asyncio
import platform

from bleak import BleakClient
from bleak.exc import BleakError
import redis

r = redis.Redis(
    host='localhost',
    port=6379, 
    password=None)



ADDRESS = "A8:1B:6A:B3:53:86"
r.set(ADDRESS, "hola")

#UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

UART_RX_CHAR_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"

def notification_handler(num:int, msg:bytearray):
    msg:str = "".join(map(chr, msg))
    msg = msg.strip()

    print(f"read: {msg}\n")
    r.set(ADDRESS, msg)



async def print_services(mac_addr: str):
    global x
    async with BleakClient(mac_addr) as client:
        svcs = await client.get_services()
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
