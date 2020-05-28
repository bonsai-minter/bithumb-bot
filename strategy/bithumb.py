# Copyright [2020] [commaster] Licensed under the Apache License, Version 2.0 (the «License»);
import logging
import os
import threading
import time

import plyer
import toml
from colorama import Fore, Style

import BithumbGlobal
import prettyoutput
import strategy.first
import strategy.second


def clear() :
	os.system('cls' if os.name == 'nt' else 'clear')


try :
	status = []
	DEBUG = False
	logging.basicConfig(filename="sample.log", level=logging.DEBUG)
	config = toml.load("config.toml")

	client = BithumbGlobal.BithumbGlobalRestAPI(config["auth"]["api_key"], config["auth"]["api_key_auth"])


	def get_balance(limit) :
		text = "Balance:\n" + Style.BRIGHT
		text_frozen = ""
		itera = 0
		for i in client.balance() :
			if float(i["count"]) > 0 and itera <= limit :
				itera += 1
				if float(i["frozen"]) > 0 :
					text_frozen += Style.BRIGHT + str(i["frozen"]).rstrip("0").rstrip(
						".") + Style.RESET_ALL + " " + Fore.YELLOW + i["coinType"] + Style.RESET_ALL + "\n"
				text += Style.BRIGHT + str(i["count"]).rstrip("0").rstrip(".") + Style.RESET_ALL + " " + Fore.YELLOW + \
				        i[
					        "coinType"] + Style.RESET_ALL + "\n"
		text += "\nFrozen:\n" + text_frozen
		return text[:-1]


	clear()
	status.append("Start app")


	def notify(pair) :
		global client, config, status
		while True :
			cost = client.ticker(pair)[0]["c"]
			status.append(f"{cost} {pair}")
			if config["notify"]["nootification_on_desktop"] :
				plyer.notification.notify(message=f'{cost}',
				                          app_name='Bithumb Bot',
				                          title=f'{pair}', )
			time.sleep(config["notify"]["time"] * 60)


	def scallping(pair) :
		global config, client, status
		strateg = strategy.first.strategy(client)

		while True :
			configa = config

			price = strateg.start(pair, status=status, percent=configa['scallping']['percent'],
			                      strategy=configa['scallping']['strategy'], type_thing="buy",
			                      percent_to_play=configa['scallping']['percent_to_play'],
			                      save_percent=configa['scallping']['save_percent'],
			                      nootification_on_desktop=config['scallping']["nootification_on_desktop"])
			time.sleep(5)
			strateg.start(pair, status=status, percent=configa['scallping']['percent'],
			              strategy=configa['scallping']['strategy'], type_thing="sell",
			              percent_to_play=configa['scallping']['percent_to_play'],
			              save_percent=configa['scallping']['save_percent'], price=price,
			              nootification_on_desktop=config['scallping']["nootification_on_desktop"])


	def triangle(symbol) :
		global config, client, status
		while True :
			straa = strategy.second.strategy(client)
			straa.start(config['triangle']["min_percent"], config['triangle']["symbol"],
			            config['triangle']['percent_to_play'], status, config['triangle']["ordering"])
			time.sleep(config['triangle']["timeout"] * 60)


	if not DEBUG :

		if config["scallping"]["enabled"] :
			for i in config["scallping"]["symbols"] :
				my_thread = threading.Thread(target=scallping, args=(i,))
				my_thread.start()


		def _notify() :
			global config
			if config["notify"]["enabled"] :
				for i in config["notify"]["symbols"] :
					my_thread = threading.Thread(target=notify, args=(i,))
					my_thread.start()
					time.sleep(config["notify"]["timeout"])


		threading.Thread(target=_notify).start()
		column = int(os.get_terminal_size().lines * 2 / 5)
		dat = get_balance(column)


		def _balance() :
			global dat, column, config
			column = int(os.get_terminal_size().lines * 2 / 5)
			dat = get_balance(column)
			config = toml.load("config.toml")
			time.sleep(30)


		while True :
			column = int(os.get_terminal_size().lines * 2 / 5)
			columnb = int(os.get_terminal_size().lines * 3 / 5)
			clear()
			print(dat)
			print(Fore.GREEN + "=" * os.get_terminal_size().columns)
			print(Style.RESET_ALL, end="")
			itera = 0
			for i in status[: :-1] :
				itera += 1
				if itera < columnb :
					if "WARNING" in i :
						print(i)
					else :
						print(prettyoutput.info(string=i, prn_out=False, space=False))

			time.sleep(0.1)
except Exception as e :
	print("ERROR!!!!! ")
	print("Write message with error to @commaster1 or issue to https://github.com/bonsai-minter/bithumb-bot", "\n")
	print(e)
	input()
