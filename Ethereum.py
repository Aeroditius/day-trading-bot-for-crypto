import datetime
from datetime import date
import time
import json
import requests
from timeit import default_timer as timer

#watch for even higher falling values
#get rid of slope bullshit

url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

# Place a market order by specifying amount of USD to use. 
# Alternatively, 'size' could be used to specify quantity in BTC amount.
#auth_client.place_market_order(product_id='ETH-USD', side='buy', funds='100.00')

buyprice = 0.0
sellprice = 0.0
old_sellprice = 0.0
total_profit = 0.0 #STARTS AT 10 FOR FIRST ITERATION TO CATCH IN CASE OF FALLING PRICES
old_profit = 0.0
w = 1 #W means wait
x = 1 #X means wait

mstart = timer() #MSTART MASTER START | MEND MASTER END | MTIME MASTER TIME

while 1:
	#BUY
	data = requests.get(url).json()
	buyprice = float(f"{data['price']}")
	start = timer()
	time.sleep(5) #OLD VALUE 15
	data = requests.get(url).json()
	cprice1 = float(f"{data['price']}") #no sell price because didn't sell yet | cprice = check price
	old_fc = cprice1
	end = timer()
	rise = cprice1 - buyprice
	run = end - start
	if rise/run > 5: #NORMALLY -0.05
		slope = rise/run
		print(slope)
		print('slope > -0.05\n')
		continue
	else:
		while 1:
			data = requests.get(url).json()
			fc = float(f"{data['price']}") #FINAL CHECK
			print('old_fc: %f\nfc: %f\n' %(old_fc, fc))
			if old_fc - fc >= 0.1: #and cprice1 >= fc: #<>=   |   old_fc - fc >= 0.1   |   old_fc >= fc
				time.sleep(3) ############################JUST A TEST
				buyprice = float(f"{data['price']}") #THIS SIMULATES BUYING
				print('Bought at: %f' %buyprice)
				break
			#elif old_fc >= fc and cprice1 >= fc:
			#	old_fc = fc
			#	continue
			#else:
			#	buyprice = float(f"{data['price']}") #THIS SIMULATES BUYING
			#	print('Bought at: %f' %buyprice)
			#	break
			else:
				old_fc = fc
	'''
	'''
	while 1:
		#SELL
		try:#
			data = requests.get(url).json()
		except ConnectionResetError:#
			continue#
		sellprice = float(f"{data['price']}")
		old_fc = sellprice
		print(sellprice)
		if sellprice - buyprice >= 0.1: #OR 0.25
			while 1:
				data = requests.get(url).json()
				fc = float(f"{data['price']}") #FINAL CHECK
				if fc - old_fc >= 0.1: #and fc >= sellprice: #<>=   |   fc - old_fc >= 0.1   |   fc >= old_fc
					break
				else:
					old_fc = fc
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
		elif sellprice <= buyprice:
			##########
			if sellprice - buyprice < -50: #-1 * total_profit #REPRESENTS LOSS inverse signs
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
				##########
		else:
			pass