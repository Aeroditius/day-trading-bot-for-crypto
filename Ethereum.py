import datetime
from datetime import date
import time
import json
import requests
from timeit import default_timer as timer

mstart = timer() #MSTART MASTER START | MEND MASTER END | MTIME MASTER TIME

buyprice = 0.0
sellprice = 0.0
old_sellprice = 0.0
total_profit = 0.0
old_profit = 0.0
w = 1 #W means wait
x = 1 #X means wait

key = "https://api.binance.com/api/v3/ticker/price?symbol="
currencies = ["ETHUSDT"] #MAYBE ADD BTC SOON

while 1: ###
	try: ###
		while 1:
			#BUY
			url = key+currencies[0]  
			data = requests.get(url)
			data = data.json()
			buyprice = float(f"{data['price']}")
			start = timer()
			time.sleep(3) #OLD VALUE 15
			url = key+currencies[0]  
			data = requests.get(url)
			data = data.json()
			cprice1 = float(f"{data['price']}") #no sell price because didn't sell yet | cprice = check price
			end = timer()
			rise = cprice1 - buyprice
			run = end - start
			if rise/run > -0.25: #NORMALLY -0.05
				slope = rise/run
				print(slope)
				print('slope > -0.25\n')
				continue
			else:
				###
				while w == 1:
					url = key+currencies[0]  
					data = requests.get(url)
					data = data.json()
					fc1 = float(f"{data['price']}") #FINAL CHECK 1
					time.sleep(3) ###TEST THIS NUMBER HEAVILY (ei 15)
					url = key+currencies[0]  
					data = requests.get(url)
					data = data.json()
					fc2 = float(f"{data['price']}") #FINAL CHECK 2
					if fc1 >= fc2 and cprice1 >= fc2: #ALSO TRY FC1
						w = 1
					else:
						w = 0
				###
				buyprice = float(f"{data['price']}") #THIS SIMULATES BUYING
				print('Bought at: %f' %buyprice)
				start1 = timer() ###
				execute = 1
			while 1:
				#SELL
				url = key+currencies[0]
				data = requests.get(url) #
				data = data.json()
				sellprice = float(f"{data['price']}")
				print(sellprice)
				if execute == 1: ###
					end1 = timer() ###
					ttime = end1 - start1 ###
					print('Transition time is %f' %ttime) ###
					execute = 0 ###
				else: ###
					pass ###
				if sellprice >= buyprice and sellprice - buyprice >= 0.25: #OR 0.25
					##########
					while w == 1:
						#url = key+currencies[0]  
						#data = requests.get(url)
						data = requests.get(url).json()
						fc1 = float(f"{data['price']}") #FINAL CHECK 1
						#url = key+currencies[0]  
						#data = requests.get(url)
						data = requests.get(url).json()
						fc2 = float(f"{data['price']}") #FINAL CHECK 2
						if fc1 <= fc2: #and fc2 <= buyprice:
							w = 1
						else:
							w = 0
					##########
					sellprice = float(f"{data['price']}") #THIS SIMULATES SELLING
					profit = sellprice - buyprice
					print('\nSOLD')
					print('Profit: %f' %profit)
					total_profit = profit + old_profit
					print('Total profit: %f' %total_profit)
					#
					mend = timer()
					mtime = mend - mstart
					print('Elapsed time: %f seconds\n' %mtime)
					#
					old_profit = total_profit
					break
				else:
					pass
	except ConnectionResetError: ###
		continue ###