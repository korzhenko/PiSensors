import sys
import requests
import Adafruit_DHT


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}* Humidity={1:0.1f}%'.format(temperature, humidity))
    cmd = 'http://127.0.0.1:7080/json.htm?type=command&param=udevice&idx=10&nvalue=0&svalue='+'{0:0.1f}'.format(temperature)+';'+'{0:0.0f}'.format(humidity)+';0'
    #   cmd = ('http://127.0.0.1:3333/json.htm?type=command&param=udevice&idx=3&nvalue=0&svalue='   '{0:0.1f}'.format(temperature)   ';'   '{0:0.0f}'.format(humidity)   ';0')
    requests.get(cmd)
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
