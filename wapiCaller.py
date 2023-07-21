import json
import requests

#NOTE: 22 mox per min of wweather

class Wapi: 

    wapiKey: str= ""

    def __init__(self,wapiKey:str) -> bool:
        self.wapiKey = wapiKey
        

    def isRaining(self,x,y) -> bool:    
        api_url = "https://api.openweathermap.org/data/2.5/weather?lat="+ str(x) +"&lon="+ str(y)+"&mode=json&appid="+ str(self.wapiKey) +""
        rainCheck = requests.get(api_url).json()
        print("Weather got for ", x , y , " [", rainCheck["weather"][0]["main"] ,"]")
        try:
            
            if (rainCheck["weather"][0]["main"]) == 'Rain':
                return 1
            elif (rainCheck["weather"][0]["main"]) != 'Rain':
                return 0
        except:
            return 0



    def getResponse(self,x,y) -> json:    
        api_url = "https://api.openweathermap.org/data/2.5/weather?lat="+ str(x) +"&lon="+ str(y)+"&mode=json&appid="+ str(self.wapiKey) +""
        response= requests.get(api_url).json()
        return response


