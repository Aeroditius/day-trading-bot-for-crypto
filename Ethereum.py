import datetime
from datetime import date
import time
import json
import requests
from timeit import default_timer as timer

#watch for even higher falling values
#get rid of slope bullshit

#url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

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

#def PriceRequest(data):
#	data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()

while 1:
	#BUY
	data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
	fc1 = float(f"{data['price']}") #FINAL CHECK
	time.sleep(3)
	data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
	fc2 = float(f"{data['price']}") #FINAL CHECK
	old_fc = fc2
	print('fc1: %f\nfc2: %f\n' %(fc1, fc2))
	if fc1 - fc2 >= 0.25: #<>=   |   0.5
		while 1:
			data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
			fc = float(f"{data['price']}") #FINAL CHECK
			print('old_fc: %f\nfc: %f\n' %(old_fc, fc))
			if fc > old_fc: #and fc >= sellprice: #<>=   |   fc - old_fc <= 0.1   |   fc <= old_fc
				break
			else:
				old_fc = fc
		data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
		buyprice = float(f"{data['price']}") #THIS SIMULATES BUYING
		print('Bought at: %f\n' %buyprice)
	else:
		continue
	while 1:
		#SELL
		data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
		sellprice = float(f"{data['price']}")
		old_fc = sellprice
		'''
		old_fc = sellprice
		'''
		print('Bought at: %f' %buyprice)
		print(sellprice)
		print('\n')
		if sellprice >= buyprice: #OR 0.25
			while 1:
				data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
				fc = float(f"{data['price']}") #FINAL CHECK
				print('old_fc: %f\nfc: %f\n' %(old_fc, fc))
				if fc < old_fc: #and fc >= sellprice: #<>=   |   fc - old_fc >= 0.1   |   fc >= old_fc
					break
				else:
					old_fc = fc
			data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
			sellprice = float(f"{data['price']}") #THIS SIMULATES SELLING
			profit = sellprice - buyprice
			print('\nSOLD')
			print('Profit: %f' %profit)
			total_profit = profit + old_profit
			print('Total profit: %f' %total_profit)
			mend = timer()
			mtime = mend - mstart
			print('Elapsed time: %f seconds\n' %mtime)
			old_profit = total_profit
			break
		elif sellprice <= buyprice:
			if sellprice - buyprice < -5: #-1 * total_profit #REPRESENTS LOSS inverse signs
				data = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT').json()
				sellprice = float(f"{data['price']}") #THIS SIMULATES SELLING
				profit = sellprice - buyprice
				print('\nSOLD')
				print('Profit: %f' %profit)
				total_profit = profit + old_profit
				print('Total profit: %f' %total_profit)
				mend = timer()
				mtime = mend - mstart
				print('Elapsed time: %f seconds\n' %mtime)
				old_profit = total_profit
				break
			else:
				continue
		else:
			pass