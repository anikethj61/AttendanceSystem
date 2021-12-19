from bluepy.btle import Scanner,DefaultDelegate
import paho.mqtt.publish as publish
import time

MQTT_SERVER = "test.mosquitto.org"
MQTT_PATH = "Team6Attendance" #topic
MQTT_MSG = "" #message
#--------------------------------------------------------------------------------------
deviceRSSI = ()
deviceAddr = ()
listRSSI = list(deviceRSSI)
listAddr = list(deviceAddr)
class ScanDelegate(DefaultDelegate):
        def __init__(self):
                DefaultDelegate.__init__(self)

        def handleDiscovery(self,dev,isNewDev,isNewData):
                if isNewDev:
                        print("Discovered Device", dev.addr)
                elif isNewData:
                        print("Received new data from:", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
        print "Device %s(%s), RSSI = %d dB" %(dev.addr, dev.addrType, dev.rssi)
        listRSSI.append(dev.rssi)
        listAddr.append(dev.addr)
        MQTT_MSG = "RSSI: " + "(" + str(dev.rssi) + ")" #part1
        for(adtype,desc,value) in dev.getScanData():
                print" %s = %s" %(desc,value)
                text = dev.getValueText(adtype)
                textString = str(text)
                print "UUID: %s" %(textString[8:40])
                print "\n Manufacturer ID: %s" %(textString[0:4])
                MQTT_MSG = MQTT_MSG + "," + " UUID: " + textString[8:40] + " " + "Manufacturer ID: " + textString[0:4] #part2
        publish.single(MQTT_PATH, MQTT_MSG, hostname=MQTT_SERVER)
        #publish.single(MQTT_PATH, dev.rssi, hostname=MQTT_SERVER)
        time.sleep(1)

deviceRSSIfinal = tuple(listRSSI)
deviceAddrfinal = tuple(listAddr)
print deviceRSSIfinal, deviceAddrfinal