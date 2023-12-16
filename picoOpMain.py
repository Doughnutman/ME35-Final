import ostepper
from servo import Servo, servo_angle, servo_Map
import mqtt
from secrets import Tufts_Wireless as wifi
import network, ubinascii, time

def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("MAC " + mac)
    
    station.connect(wifi['ssid'], wifi['pass'])
    while not station.isconnected():
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())
    
my_coord = " "

def whenCalled(topic, msg):
    global my_coord
    print((topic.decode(), msg.decode()))
    my_coord = msg.decode()

connect_wifi(wifi)

# code to connect to MQTT Broker.
# Modified from code from class notion site
#def MQTT_Connect():
try:
    global opBot
    opBot = mqtt.MQTTClient("Dr.Pico", '10.243.87.114', keepalive=60)
    opBot.connect()
    opBot.set_callback(whenCalled)
    opBot.subscribe("coord")
    while True:
        if(opBot.check_msg()):
            print(my_coord)
            break
        time.sleep(0.1)
except OSError as e:
    print('Failed to establish connection to MQTT broker')
    print(e)
finally:
    opBot.disconnect()

theCoords = my_coord.split(',')
print(theCoords)
xmove = float(theCoords[0])
ymove = float(theCoords[1])

# pre-determined movement pattern using found coordinates
s1 = Servo(12)
servo_angle(s1,150)
time.sleep(1)
ostepper.movex(xmove)
ostepper.movey(ymove)
servo_angle(s1,130)
servo_angle(s1,120)
time.sleep(1)
servo_angle(s1,150)
ostepper.movex(-xmove)
ostepper.movey(-ymove)
