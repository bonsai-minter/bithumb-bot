#Copyright [2020] [commaster] Licensed under the Apache License, Version 2.0 (the «License»);
from json import loads as load_json
from datetime import datetime as DateTime
from base64 import b64encode, b64decode
from hmac import digest
import requests
import time
from decimal import Decimal

URL_WITHDRAW= 'https://global-openapi.bithumb.pro/openapi/v1/withdraw'
URL         = 'https://global-openapi.bithumb.pro/openapi/v1/spot/'
DEPTH_URL   = 'https://global-openapi.bithumb.pro/market/data/orderBook?symbol='
CONFIG_URL  = 'https://global-openapi.bithumb.pro/market/data/config'


class BithumbGlobalError(RuntimeError):
    def __init__(self, code, msg):
        super().__init__('[%s] %s' % (code, msg))


SIDE_MAP = {
    'ask':  'sell',
    'bid':  'buy',
    'sell': 'sell',
    's':    'sell',
    'buy':  'buy',
    'a':    'sell',
    'b':    'buy',
}


def direction(direction):
    return SIDE_MAP[direction.lower()]


def depth(data):
    data = data['info']
    asks = [(float(row[0]), float(row[1])) for row in data['s']]
    bids = [(float(row[0]), float(row[1])) for row in data['b']]

    return {'asks': asks, 'bids': bids}
        

def all_pairs(data):
    return data['info']['spotConfig']


class Secret:
    def __init__(self, api_key, secret_code):
        self.__api_key = api_key
        self.__secret_code = secret_code.encode()

    def sign(self, data):
        data = list(data.items())
        data.sort()
        msg = '&'.join(['%s=%s' % (k, v) for k, v in data])
        return digest(self.__secret_code, msg.encode('utf-8'), 'sha256').hex()

    @property
    def api_key(self):
        return self.__api_key




class BithumbGlobalRestAPI:
    def __init__(self, api_key, secret_code):
        if api_key and secret_code:
            self.__secret = Secret(api_key, secret_code)
        else:
            self.__secret = None
        self.__session = session = requests.session()
        session.headers.update({'content-Type': 'application/json'})

    config_dat = None
    @property
    def session(self):
        return self.__session


    def post(self, action, parms):
        ts = str(int(DateTime.now().timestamp() * 1000))
        data = {
            'apiKey': self.__secret.api_key,
            'bizCode': action,
            'msgNo': ts,
            'timestamp': ts,
        }
        if parms is not None:
            data.update(parms)
        data['signature'] = self.__secret.sign(data)
        response = self.session.post(url=URL + action, json=data, timeout=15)
        response = load_json(response.text)

        if response['code'] != '0':
            raise BithumbGlobalError(response['code'], response['msg'])
        return response['data']


    def config(self):
        if self.config_dat is None:
            self.config_dat = self.post('config',parms=None)
        return self.config_dat
    def get_coin_fee(self,coin):
        for i in self.config()["coinConfig"]:
            if i["name"] == coin:
                return i

    def withdraw(self, cointype, address, volume, mark='AUTO', memo=None):
        parms = {
            'coinType': cointype,
            'address': address,
            'quantity': volume,
            'mark': mark
        }
        action = 'withdraw'
        if memo:
            parms['extendParam'] = memo
        ts = str(int(DateTime.now().timestamp() * 1000))
        data = {
             'apiKey': self.__secret.api_key,
             'bizCode': action,
             'msgNo': ts,
             'timestamp': ts,
        }
        data.update(parms)

        data['signature'] = self.__secret.sign(data)

        response = self.session.post(url=URL_WITHDRAW, json=data, timeout=15)
        response = load_json(response.text)

        if response['code'] != '0':
           raise BithumbGlobalError(response['code'], response['msg'])
        return response['data']



    def all_pairs(self):
        response = self.__session.get(CONFIG_URL)
        data = load_json(response.text)
        return all_pairs(data)

    def get_accuracy(self,symbol):
        for i in self.all_pairs():
            if i["symbol"] == symbol:
                return i
        return None

    def place_order(self, symbol, side, price, amount,type_sell='limit'):
        symbol = symbol.replace('/', '-')
        accuracy = self.get_accuracy(symbol)["accuracy"]
        if direction(side) == "buy":
            price = round(float(price),int(accuracy[0]))
            amount = round(float(amount),int(accuracy[1]))
        else:
            price = round(float(price),int(accuracy[0]))
            amount = round(float(amount),int(accuracy[1]))

        parms = {
            'symbol': symbol,
            'type': type_sell,
            'side': direction(side),
            'price': str(Decimal('%.8f' % price).normalize()),
            'quantity': str(Decimal('%.8f' % amount).normalize())
        }

        return self.post('placeOrder', parms)['orderId']


    def cancel_order(self, symbol, order_id):
        parms = {
            'symbol': symbol.replace('/', '-'),
            'orderID': order_id,
        }
        result = self.post('cancelOrder', parms)
        return result


    def balance(self, coin=None):
        parms = {
            'assetType': 'spot'
        }
        if coin:
            parms['coinType']=coin
        result = self.post('assetList', parms)
        return result


    def orders(self, side=None, queryRange='thisweek', coinType=None, marketType=None, status=None, page=1, count=10):
        parms = {
            'page': str(page),
            'count': str(count)
        }
        parms['queryRange'] = queryRange
        if side:
            assert side in ('buy', 'sell')
            parms['side'] = side
        if coinType:
            parms['coinType'] = coinType
        if marketType:
            parms['marketType'] = marketType
        if status:
            assert status in ('traded', 'trading')
            parms['status'] = status
        return self.post('orderList', parms)


    def order_detail(self, order_id,symbol, page=1, count=10):
        parms = {
            'orderId': order_id,
            'symbol': symbol,
            'page': str(page),
            'count': str(count)
        }
        return self.post('orderDetail', parms)

    def kline(self,symbol,typeb="m30",start=int(time.time() - 30 * 60 ),end=int(time.time())):
        parms = dict(symbol=symbol,type=typeb,start=start,end=end)
        return self.post('kline', parms)

    def ticker(self,symbol):
        parms = dict(symbol=symbol)
        return self.post('ticker', parms)

    def market(self, coin=None, market=None):
        parms = {}
        if coin:
            parms['fcoinId'] = coin
        if market:
            parms['fmarketId'] = market
        return self.post('MARKET_SPOT', parms)


    def depth(self, symbol, count):
        url = DEPTH_URL + symbol.replace('/', '-')
        data = load_json(self.__session.get(url, timeout=5).text)
        return depth(data)


    def query_order(self, symbol, order_id):
        symbol = symbol.replace('/', '-')
        order = self.post('singleOrder', {'symbol': symbol, 'orderId': order_id})
        return order
   

    def openning_orders(self, symbol, id_only=True):
        result = []
        page = 1
        while True:
            parms = {
                'count': 50,
                'page':  page,
                'symbol': symbol.replace('/', '-'),
            }
            orders = self.post('openOrders', parms)
            result += orders['list']
            if int(orders['num']) <= page*50:
                break
            else:
                page += 1
        if id_only:
            result = [row['orderId'] for row in result]
        return result


