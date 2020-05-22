import time
import plyer
import logging
import prettyoutput
logging.basicConfig(filename="sample.log", level=logging.DEBUG) 
class strategy:
    client = None
    def __init__(self,client):
        self.client = client
    def start(self,min_percent,symbol,percent_to_play,status,ordering):
        all_pairs = self.client.ticker("ALL")



        coin = symbol

        dat = []
        aa = 1 + (min_percent / 100)
        for i in all_pairs:
            if coin == i['s'].split("-")[0] and float(i['v']) != 0:

                for x in all_pairs:
                    if i['s'].split("-")[1] == x['s'].split('-')[0] and x['s'].split('-')[1] != coin and float(x['v']) != 0:

                        for y in all_pairs:
                            if x['s'].split("-")[1] == y['s'].split('-')[0] and y['s'].split('-')[1] == coin:
                                dat.append([i,'b',x,'b',y,'b',(float(i['c']) - client.get_coin_fee()) * float(x['c']) * float(y['c'])])
                            elif x['s'].split("-")[1] == y['s'].split('-')[1] and y['s'].split('-')[0] == coin:
                                dat.append([i,'b',x,'b',y,'s',float(i['c']) * float(x['c']) / float(y['c'])])
                        # print(i,x,win,win * float(x['c']))
                        # print()
                    elif i['s'].split("-")[1] == x['s'].split('-')[1] and x['s'].split('-')[0] != coin and float(x['v']) != 0:
                        for y in all_pairs:
                            if x['s'].split("-")[0] == y['s'].split('-')[0] and y['s'].split('-')[1] == coin and float(y['v']) != 0:
                                dat.append([i,'b',x,'b',y,'s',float(i['c']) / float(x['c']) * float(y['c'])])
                            elif x['s'].split("-")[0] == y['s'].split('-')[1] and y['s'].split('-')[0] == coin and float(y['v']) != 0:
                                dat.append([i,'b',x,'s',y,'s',float(i['c']) / float(x['c']) / float(y['c'])])
            elif coin == i['s'].split("-")[1] and float(i['v']) != 0:
                for x in all_pairs:
                    if i['s'].split("-")[0] == x['s'].split('-')[0] and x['s'].split('-')[1] != coin and float(x['v']) != 0:

                        for y in all_pairs:
                            if x['s'].split("-")[1] == y['s'].split('-')[0] and y['s'].split('-')[1] == coin:
                                dat.append([i,'s',x,'b',y,'b',1 / float(i['c']) * float(x['c']) * float(y['c'])])
                            elif x['s'].split("-")[1] == y['s'].split('-')[1] and y['s'].split('-')[0] == coin:
                                dat.append([i,'s',x,'b',y,'s',1 / float(i['c']) * float(x['c']) / float(y['c'])])
                        # print(i,x,win,win * float(x['c']))
                        # print()
                    elif i['s'].split("-")[0] == x['s'].split('-')[1] and x['s'].split('-')[0] != coin and float(x['v']) != 0:
                        for y in all_pairs:
                            if x['s'].split("-")[0] == y['s'].split('-')[0] and y['s'].split('-')[1] == coin and float(y['v']) != 0:
                                dat.append([i,'s',x,'s',y,'b',1 / float(i['c']) / float(x['c']) * float(y['c'])])
                            elif x['s'].split("-")[0] == y['s'].split('-')[1] and y['s'].split('-')[0] == coin and float(y['v']) != 0:
                                dat.append([i,'s',x,'s',y,'s',1 / float(i['c']) / float(x['c']) / float(y['c'])])

        
        dat.sort(key=lambda input: float(input[-1]),reverse=True)
        i = dat[3]
        for t in dat[::-1]:
            if t[-1] > aa:
                s = t[0]["s"] + " > " + t[2]["s"] + " > " + t[4]["s"] + " x" + str(t[-1])
                status.append(s)

        if i[-1] > aa and ordering:
            count = self.client.balance(symbol)
            count = float(count[0]["count"]) * (percent_to_play / 100)
            if 'b' in i[1]:
                i[1] = 's'
            else:
                i[1] = 'b'
                count = float(count) / float(i[0]['c'])
            
            id = self.client.place_order(i[0]["s"],i[1],i[0]['c'],float(count))
            dat = self.client.query_order(i[0]["s"],id)
            while dat["status"] == "pending":
                time.sleep(1)
                dat = self.client.query_order(i[0]["s"],id)

            if 'b' in i[3]:
                count = self.client.balance(i[2]["s"].split("-")[0])
                count = float(count[0]["count"]) * (percent_to_play / 100)
                i[3] = 's'
            else:
                count = self.client.balance(i[2]["s"].split("-")[1])
                count = float(count[0]["count"]) * (percent_to_play / 100)
                i[3] = 'b'
                count = float(count) / float(i[3]['c'])
            
            
            id = self.client.place_order(i[2]["s"],i[3],i[2]['c'],float(count))
            dat = self.client.query_order(i[2]["s"],id)
            while dat["status"] == "pending":
                time.sleep(1)
                dat = self.client.query_order(i[2]["s"],id)

            if 'b' in i[5]:
                count = self.client.balance(i[4]["s"].split("-")[0])
                count = float(count[0]["count"]) * (percent_to_play / 100)
                i[5] = 's'
            else:
                count = self.client.balance(i[4]["s"].split("-")[1])
                count = float(count[0]["count"]) * (percent_to_play / 100)
                i[5] = 'b'
                count = float(count) / float(i[5]['c'])
            
            
            id = self.client.place_order(i[4]["s"],i[5],i[4]['c'],float(count))
            dat = self.client.query_order(i[4]["s"],id)
            while dat["status"] == "pending":
                time.sleep(1)
                dat = self.client.query_order(i[4]["s"],id)
        #print(dat)
        # for i in dat:
        #     print(i)
        #     print(i[0]["s"])