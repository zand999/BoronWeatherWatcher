from DeviceManager import DeviceManager
from WeatherWatcher import WeatherWatcher
import KeyMngr



def mhain():
    print("Initilization Started")
    fwrrtflow = DeviceManager("AcctDeviceData.json","fwrrtflow")
    WeatherWatcher("11111111111111111111111111", fwrrtflow)


#Calls Driver Function called it mhain becuase I can
mhain()

print("Boot Thread Finished")







