import json
from threading import local
import requests
from DeviceCaller import DeviceCaller

class DeviceManager:

    url = "https://api.particle.io/v1/devices"
    access_token = ""
    cloudCaller = None
    devlist = None
    acct_name:str = None
    localdata:json = None

    #constructior to look through json database and store device list as well as access token
    def __init__(self, fname: str ,acct_name:str):
        print("DeviceManager Constructed: ", fname, "->" ,acct_name)
        f = open(fname)
        self.localdata = json.load(f)[acct_name]
        f.close()
        self.access_token = self.localdata["access_key"]
        self.cloudCaller = DeviceCaller(self.access_token)
        self.acct_name = acct_name
        self.updateDeviceList()
        
    #get new device data from the particle.io cloud
    def updateDeviceList(self):
        self.devlist = self.getCloudDevList()
    
    #get localy stored cloud device daeta
    def getLocalLCloudDevList(self):
        return self.devlist
    
    #get cloud device data from cloud
    def getCloudDevList(self):
        return requests.get(self.url + "?access_token=" + self.access_token).json()
        
    #get a spacific device information from newly pulled data from cloud
    def getDeviceInfoCloud(self, deviceID: str):
        return self.__getDeviceInfo(deviceID, self.getCloudDevList())

    #get a spacific device information from localaly pulled cloud device info
    def getDeviceInfoLocal(self, deviceID: str):
        return self.__getDeviceInfo(deviceID, self.devlist)

    #hunt through device list for id and return device
    def __getDeviceInfo(self, deviceID:str, deviceList: dict()):
        for dev in deviceList:
            if(dev["id"] == deviceID):
                return dev
        return None

    #call particular device function on device
    def callDeviceFunction(self, ID:str, function:str, args:str):
        self.cloudCaller.callThreadDeviceFunction(ID,function,args)
    
    #call particular function of group of devices
    def callDevicesFunction(self, function: str , args: str):
        IDlist = []
        for dev in self.devlist:
            IDlist.append(dev["id"])
        self.cloudCaller.callDevicesFunction(IDlist,function,args)

    #return the localy stored access key for particle.io
    def returnListKey(self) -> str:
        return self.access_token

    #key the localy stored JSON data of the particle devices i.e lat, long
    def getOfflineDevData(self) -> dict:
        #print(self.localdata)
        return self.localdata["device_list"]

