from concurrent.futures import thread
from curses.panel import top_panel
from os import access
from urllib import response
import requests
#import DeviceManager
import KeyMngr
import threading
import time


class DeviceCaller:
    token = ""
    url = "https://api.particle.io/v1/devices/"
    threadlistlock =  threading.Lock()
    threadlist = []
    #threadData = {"deviceID": "" , "timeStarted" : 0, "function" : ""}
    
    #constructor to store particle.io access token
    def __init__(self,access_token: str) -> None:
        self.token = access_token
        print("DeviceFunction constructed: ", access_token)

    #non threaded calling of device function that will wait until response is recived
    def callDeviceFunction(self, ID:str, function:str, args:str):
        
        reponse = self.__cloudCall(ID,function,args)
        print(reponse)

    #threaded calling of device function that will not suspend program while running
    def callThreadDeviceFunction(self, ID:str, function:str, args:str) -> bool:
        self.threadlistlock.acquire()
        for runningThread in self.threadlist:
            if(runningThread["deviceID"] == ID and runningThread["function"] == function):
                return False
        self.threadlist.append({"deviceID": ID , "timeStarted" : float( time.time_ns() / 1000 ), "function" : ""})
        threading.Thread(target=self.__deviceCallThread,args=(ID,function,args)).start()
        self.threadlistlock.release()
        return True
    
    #function that is passed to thread to call
    def __deviceCallThread(self, ID:str, function:str, args:str):
        #print("CallingDevice:", ID, "Funct:", function,"arg:", args)
        info = {"arg" : args, "access_token": self.token}
        #for now it will take 5 attempts to update
        #TODO: keep accureate state information on the devices sleep period so it will only update around the time it is neccisary
        #TODO: Try for sleep period
        for i in range(1):
            response = self.__cloudCall(ID,function,args)
            print("CallingDevice:", ID, "Funct:", function,"arg:", args, " " ,response.json())
            if(response.ok):
               break
        
        #clean up
        self.threadlistlock.acquire()
        time.sleep(2)
        for runningThread in self.threadlist:
            if(runningThread["deviceID"] == ID and runningThread["function"] == function):
                self.threadlist.remove(runningThread)
        
        self.threadlistlock.release()

    #function that is the particle API request for function as well as data    
    def __cloudCall(self, ID:str, function:str, args:str):
        return requests.get(url=(self.url + ID + "/" + function), params={"arg" : args, "access_token": self.token})

    #function for called function of list of devices
    def callDevicesFunction(self, IDs:list, function: str , args: str):
        threading.Thread(target=self.__threadGroupCall,args=(IDs,function,args)).start()

    #functioin to start new threads for a group of devcies as individual theads.
    def __threadGroupCall(self, IDs:list, function: str , args: str):
        print("Bulk started on", IDs)
        for id in IDs:
            self.callThreadDeviceFunction(id, function, args)
    










