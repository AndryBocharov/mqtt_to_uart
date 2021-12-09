# pip  install paho-mqtt
# pip3 install paho-mqtt

import paho.mqtt.client as mqtt
import time
import serial
import  binascii
############
PORT='/dev/ttyUSB0'
############
def on_message(client, userdata, message):
    print(message.topic,": " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
    ###############
    ser = serial.Serial(PORT, 9600, timeout=5)
    command = message.payload.decode("utf-8")
    #command = '0c030000000584d4'
    c2 = bytes.fromhex(command)
    ser.write(c2)
    zcnt = 1000
    while ((ser.inWaiting() == 0) and (zcnt > 0)):
       time.sleep(0.01)
       zcnt = zcnt - 1
    zcnt = 0
    ###### to be sure that we have all bytes
    while (ser.inWaiting() != zcnt):
       zcnt = zcnt + ser.inWaiting()
       time.sleep(0.01)
    r = ser.read(zcnt).hex()
    ser.close();
    client.publish("pi3zory/response",r, retain = False)
    print("pi3zory/response: ",r)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("pi3zory/request")
########################################
client = mqtt.Client(client_id="pi3zory356232",clean_session=True,userdata=None,protocol=mqtt.MQTTv311,transport="tcp")
client.on_message = on_message
client.on_connect = on_connect
client.username_pw_set(username="admin",password="mqttpass")
client.connect("135.181.152.164" , port=8001, keepalive=60) #connect to broker
client.loop_start() #start the loop
while True:
        time.sleep(0.1)
client.loop_stop() #stop the loop

### wow wow wow, i want to edit it online
