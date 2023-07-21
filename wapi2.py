import json
import os
import requests


class Wapi: 
	
	x=36.1628
	y=-85.5016
	wapiKey= "1111111111111111111111"
	api_url = "https://api.openweathermap.org/data/2.5/weather?lat="+ str(x) +"&lon="+ str(y)+"&mode=json&appid="+ str(wapiKey) +""
	trigger = 1
	boron = "https://api.particle.io/v1/devices/f/11111111111111111111/weatherUpdater"
	params = {"access_token":  "1111111111111111111111", "args" : "900"}
	params2 ={"access_token":  "111111111111111111111", "args" : "120"}

	def __init__(self,x,y,wapiKey):
		self.wapiKey = wapiKey
		self.x = x
		self.y = y
	def response(self):
		print(response.json())
	


	response= requests.get(api_url)
	#print(response.json())
	rainCheck= response.json()



	if (rainCheck["weather"][0]["main"]) == 'rain':
		trigger = 1
		response=requests.get(boron,params=params)
		print(response.json())
	elif not (rainCheck["weather"][0]["main"]) != 'rain':
		if (bool(trigger)) == 1:
			trigger = 0
			response=requests.get(boron,params=params2)
			print("no rain")
		









#if rainCheck[1]["Main"] == "Rain":
#	print(rainCheck["rain"])

'''if rainCheck["rain"]:
	trigger = 1
	response=requests.get(boron,params=params)
	print(response.json())
elif not rainCheck["rain"]:
	if (bool(trigger)) == 1:
		trigger = 0
		response=requests.get(boron,params=params2)
		print(response.json())
		
'''

#	if (rainCheck["weather"][0]["main"]) == 'rain':
	#	print("it be rain")
#	else:
	#	print(response.json())





