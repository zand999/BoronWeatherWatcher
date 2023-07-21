
from DeviceManager import DeviceManager
import time
import threading
from wapiCaller import Wapi
#from wapi2 import wapi2

#class to prevent over calling of Weather API
class WapiBuffer:

    apilist:str = []
    devCalledBuff: dict = []
    devUncalledBuff: dict = []
    manageBuff = [False]

    #Fucntion for starting up buffer
    def __init__(self):
        #call watcher
        if(not self.manageBuff[0]):
            print("manageBuff:", self.manageBuff)
            self.manageBuff[0] = True
            threading.Thread(target=self.__BufferManagement).start()
        
    #Function to freeze current state of buffer    
    def stopBufferManagement(self):
        self.manageBuff = False


    def addAcct(self, api_key: str):#ALPHA PLZ do not try Unused
        if (api_key in self.apilist):
            self.apilist.append(api_key)

    #function to add device to buffer to be called
    def pushDev(self, dev: dict, wapi_key:str ,callback: DeviceManager.callDeviceFunction):
        print("Pushing Weather Check List", dev["id"])
        
        dev["callback"] = callback
        dev["api_key"] = wapi_key
        self.devUncalledBuff.append(dev)
    #print("push done")
        #print(self.devUncalledBuff)
        #print(self.devCalledBuff)

    #threaded functon that manages buffer
    def __BufferManagement(self):
        print("Buffer Thread Started")

        
        while(self.manageBuff[0]):
            #Check for expired api calles and delete them
            for dev in self.devCalledBuff:
                if(time.time() - dev["time"] > 60):
                    print("Deleting From Cooldown: " , )
                    del dev["callback"]
                    del dev["api_key"]
                    del dev["time"]
                    self.devCalledBuff.remove(dev)
            #check if buffer as space avalibilty and add new items to it
            #after calling the device update function
            if (len(self.devCalledBuff) < 20):
                for list in self.devUncalledBuff:
                    self.devCalledBuff.append(list)
                    print("Checking Weather for: ", list["id"])
                    # call weather api
                    if(Wapi(list["api_key"]).isRaining(list["Latitude"],list["Longitude"])):
                        list["callback"](list["id"], "weatherUpdater", "300000")
                    else:
                        list["callback"](list["id"], "weatherUpdater", "900000")
                    list["time"] = time.time()
                    print("CooldownStamp ", list["id"], "->" , list["time"])
                    self.devUncalledBuff.remove(list)
                    if (len(self.devCalledBuff) >= 20):
                        break
            

            


    
    
#class to watch an account of particle.io devices
class WeatherWatcher:
    threshhold: float
    devlist: DeviceManager
    watch = True
    #weatherAcct: wapi2
    acctKey: str

    #constructor that stores api key as well as the list of devices
    def __init__(self, api_key: str, devices: DeviceManager):
        self.threshhold = 10
        self.acctKey = api_key
        self.devlist = devices
        #self.weatherAcct = wapi2(api_key)
        print("WeatherWatcher Constructed: ", api_key)
        threading.Thread(target=self.__watcher).start()
        #WapiBuffer().addAcct(api_key)

    #threaded function that periodicly check weather of devices
    def __watcher(self):
        print("Watching for ", self.devlist.returnListKey())
        self.__addDevToBuffer()
        while(self.watch):
            self.__addDevToBuffer()
            #add to buffer
            time.sleep(15*60)

    #function to add neccissary data to the weather api buffer and add it.
    def __addDevToBuffer(self):
        #print(self.devlist.getOfflineDevData())
        for dev in self.devlist.getOfflineDevData():
            print("Adding To Buffer: ", dev["id"], " ,name:" , dev["name"], ' ,Lat:', dev["Latitude"], ' ,Long', dev["Longitude"])
            
            WapiBuffer().pushDev(dev, self.acctKey ,self.devlist.callDeviceFunction)
        
    #fuction to stop the class from monitoring devices
    def stopWatch(self):
        self.watch = False

    #function to resume the class monioring of devices
    def startWatch(self):
        self.watch = True
        self.__watcher()
    



