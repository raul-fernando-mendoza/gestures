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

ADDRESS = "A8:1B:6A:B3:53:86"
#UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

UART_RX_CHAR_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB"


def notification_handler(num:int, msg:bytearray):
    print(f"num:{num}")
    print("read: {0}\n".format("".join(map(chr, msg))))

async def print_services(mac_addr: str):
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
                    pass
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
