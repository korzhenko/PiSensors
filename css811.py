import time
import board
import busio
import adafruit_ccs811
import requests

i2c = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)

# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass

medium_eco = ccs811.eco2
medium_tvoc = ccs811.tvoc
medium_temp = ccs811.temperature
iter = 10

for _ in range(iter):
    if ccs811.eco2>0 and ccs811.temperature>0:
        medium_eco=(medium_eco+ccs811.eco2)/2
        medium_tvoc=(medium_tvoc+ccs811.tvoc)/2
        medium_temp=(medium_temp+ccs811.temperature)/2
    time.sleep(1)

if medium_temp != 0:
    print("medium CO2: {} PPM, TVOC: {} PPB, Temp: {} ".format(medium_eco, medium_tvoc,medium_temp))
    cmd = 'http://127.0.0.1:7080/json.htm?type=command&param=udevice&idx=11&nvalue={0:0.1f}'.format(medium_eco)
    requests.get(cmd)
