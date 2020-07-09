import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

organization = "t3ackb"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        i=cmd.data['command']
        if i=='motoron':
                print("Motor is on")
        elif i=='motoroff':
                print("Motor is off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()

while True:
        
        status = random.randint(0,100) #Measures water level in the tank(ultrasonic senser)
        flow_rate = random.randint(0,40) #Measures the flow rate of the water(water flow sensor)
        avg_usage = random.randint(0,28) #Measures the overall consumption of water(RTC module)
   
        data = { 'Tank_Status' : status, 'Flow_Rate': flow_rate, 'Avg_Consumption' : avg_usage }
    
        def myOnPublishCallback():
            print ("Published Tank Status = %s %%" % status, "Flow Rate = %s L/hr" % flow_rate, "Avg Consumption = %s L" % avg_usage, "to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback
        time.sleep(5)
deviceCli.disconnect()
