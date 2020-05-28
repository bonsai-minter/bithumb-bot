#Copyright [2020] [commaster] Licensed under the Apache License, Version 2.0 (the «License»);
import logging
import time

import plyer

import prettyoutput

logging.basicConfig(filename="sample.log", level=logging.DEBUG)
class strategy:
	client = None
	def __init__(self,client):
		self.client = client

	


	def start(self,symbol,status,percent=0.01,strategy='last',type_thing="sell",percent_to_play=80,save_percent=2,price=None,nootification_on_desktop=True):
		choose = {
			'last':	lambda data: float(data["c"]),
			'normal': lambda data: (float(data["h"]) + float(data["l"])) / 2
		}
		data = self.client.ticker(symbol)[0]
		percent_lower = (-percent) / 100 + 1
		percent_high = (percent) / 100 + 1
		fun = choose[strategy]
		pricea = price		
		if price == None:
			price = fun(data)
		

		accuracy = self.client.get_accuracy(symbol)["accuracy"]

		if type_thing == "buy":
			side = symbol.split("-")[1]
			sida = symbol.split("-")[0]
			count = self.client.balance(side)
			max_count = self.client.get_coin_fee(symbol.split("-")[0])
			price_to_buy = percent_lower * price
			price_to_sell = percent_high * price
		else:
			side = symbol.split("-")[0]
			sida = symbol.split("-")[1]
			count = self.client.balance(side)
			max_count = self.client.get_coin_fee(symbol.split("-")[1])
			price_to_buy = percent_high * price
			price_to_sell = percent_lower * price

		count = float(count[0]["count"]) * (percent_to_play / 100)
		min_count = self.client.get_coin_fee(side)
		if type_thing == "sell":
			counts = round(float(count),int(accuracy[1]))
		else:
			counts = round(float(count / price_to_buy),int(accuracy[0]))
		if count < float(min_count["minTxAmt"]):
			countaaa = str(count)
			status.append(prettyoutput.warning(string=f"Not enough amount {countaaa} {side}",prn_out=False,space=False))
			return None


		if type_thing == "sell":
			id = self.client.place_order(symbol,type_thing,float(price_to_buy),float(count))
			counts = round(float(count),8)
		else:
			id = self.client.place_order(symbol,type_thing,float(price_to_buy),float(count / price_to_buy))
			counts = round(float(count / price_to_buy),8)
		
		price_to_buy = float(price_to_buy)
		if type_thing == "buy":
			sida = symbol.split("-")[1]
		else:
			sida = symbol.split("-")[0]
		countss = '{0:.10f}'.format(counts)
	
		status.append(f'Create order, Price: {price_to_buy} Count: {countss} {sida}')
		if nootification_on_desktop:
			plyer.notification.notify( message=f'Price: {price_to_buy}\nCount: {countss} {sida}',
				app_name='Bithumb Bot',
				title=f'Order Created {symbol}', )
		time.sleep(3)

		dat = self.client.query_order(symbol,id)
		while dat["status"] == "pending":

			time.sleep(1)
			data = self.client.ticker(symbol)[0]

			if float(data["c"]) * (1 + save_percent / 100) < price_to_buy or float(data["c"]) * (1 - save_percent / 100) > price_to_buy:
				try:
					self.client.cancel_order(symbol,id)
				except:
					pass
			time.sleep(0.5)
			dat = self.client.query_order(symbol,id)
		if dat["status"] == "success":
			countss = '{0:.10f}'.format(counts)
			status.append(f'Order bought {symbol}, Price: {price_to_buy} Count: {countss} {sida}')
			if nootification_on_desktop:
				plyer.notification.notify( message=f'Price: {price_to_buy}\nCount: {countss} {sida}',
					app_name='Bithumb Bot',
					title=f'Order bought {symbol}', )
		else:
			status.append(f'Order cancel, {symbol}',)
			if nootification_on_desktop:
				plyer.notification.notify( message=f'cancel',
					app_name='Bithumb Bot',
					title=f'Order cancel {symbol}', )

		return fun(data)