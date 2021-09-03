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
UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def print_services(mac_addr: str):
    async with BleakClient(mac_addr) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service.description)
            for c in service.characteristics:
                print(f"\t {c.description} {c.properties} ")
                if "read" in c.properties:
                    l = await client.read_gatt_char(c.uuid)
                    print("read: {0}".format("".join(map(chr, l)))) 
                if c.uuid == UART_RX_CHAR_UUID: 
                    print(c)
                    try:
                        #await client.connect()
                        byte = [0x31]
                        write_value = bytearray(byte)
                        
                    except BleakError as e:
                        print("BleakError" + str(e) )
                    except TimeoutError as e:
                        print("timeout error")
                        break
                    except Exception as e:
                        print("EXEPTION" + str(e) )
                    #finally:
                        #await client.disconnect()



loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(ADDRESS))
