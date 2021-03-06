import asyncio
from bleak import BleakClient

#ADDRESS = "A8:1B:6A:B3:53:86" #test
ADDRESS = "50:F1:4A:6E:67:6D" #soldado 
MODEL_NBR_UUID = "00002A00-0000-1000-8000-00805F9B34FB"

async def run(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

loop = asyncio.get_event_loop()
loop.run_until_complete(run(ADDRESS))