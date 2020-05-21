#Copyright [2020] [commaster] Licensed under the Apache License, Version 2.0 (the «License»);
import time
import plyer

import prettyoutput
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
		if price == None:
			price = fun(data)
		

		accuracy = self.client.get_accuracy(symbol)["accuracy"]

		if type_thing == "buy":

			aa = accuracy[0]
			bb = accuracy[1]
			side = symbol.split("-")[1]
			count = self.client.balance(side)
			price_to_buy = percent_lower * price
			price_to_sell = percent_high * price
		else:
			aa = accuracy[1]
			bb = accuracy[0]
			side = symbol.split("-")[0]
			count = self.client.balance(side)
			price_to_buy = percent_high * price
			price_to_sell = percent_lower * price

		count = float(count[0]["count"]) * (percent_to_play / 100)


		if type_thing == "sell":
			id = self.client.place_order(symbol,type_thing,round(float(price_to_buy),int(bb)),round(float(count),int(aa)))
			counts = round(float(count),int(aa))
		else:
			id = self.client.place_order(symbol,type_thing,round(float(price_to_buy),int(aa)),round(float(count / price_to_buy),int(bb)))
			counts = round(float(count / price_to_buy),int(bb))
		price_to_buy = round(float(price_to_buy),int(aa))
		status.append(f'Create order, Price: {price_to_buy} Count: {counts} {side}')
		if nootification_on_desktop:
			plyer.notification.notify( message=f'Price: {price_to_buy}\nCount: {counts} {side}',
				app_name='Bithumb Bot',
				title=f'Order Created {symbol}', )
		time.sleep(3)

		dat = self.client.query_order(symbol,id)
		while dat["status"] == "pending":

			time.sleep(1)
			data = self.client.ticker(symbol)[0]

			if float(data["c"]) * (1 + save_percent / 100) < price_to_buy or float(data["c"]) * (1 - save_percent / 100) > price_to_buy:
				self.client.cancel_order(symbol,id)
				# if type_thing == "sell":
				# 	self.client.place_order(symbol,type_thing,-1,round(float(count),int(aa)),type_sell="market")
				# else:
				# 	self.client.place_order(symbol,type_thing,-1,round(float(count),int(bb)),type_sell="market")
			time.sleep(0.5)
			dat = self.client.query_order(symbol,id)
		if dat["status"] == "success":
			if price == None:
				status.append(f'Order bought {symbol}, Price: {price_to_buy} Count: {count} {side}')
				if nootification_on_desktop:
					plyer.notification.notify( message=f'Price: {price_to_buy}\nCount: {count} {side}',
						app_name='Bithumb Bot',
						title=f'Order bought {symbol}', )
			else:
				win = round(abs(price_to_buy - price) * count,6)
				status.append(f'Order bought {side}, Win: {win} {side}, Price: {price_to_buy} Count: {count} {side}')
				if nootification_on_desktop:
					plyer.notification.notify( message=f'Price: {price_to_buy}\nCount: {count} {side}',
						app_name='Bithumb Bot',
						title=f'Order bought {symbol}\nWin: {win} {side}', )
		else:
			status.append(f'Order cancel, {symbol}',)
			if nootification_on_desktop:
				plyer.notification.notify( message=f'cancel',
					app_name='Bithumb Bot',
					title=f'Order cancel {symbol}', )

		return fun(data)