#!/usr/bin/env python
#-*- coding:utf-8 -*-

from decimal import *
import json
import re
import logging
import sqlite3
import logging.config
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
import datetime

# bitcoind
rpc_user=''
rpc_password=''
zeny = AuthServiceProxy("http://%s:%s@ip:port"%(rpc_user, rpc_password))

# logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def get_oauth():
    consumer_key = ''
    consumer_secret = ''
    access_key = ''
    access_secret = ''
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

def DecimaltoStr(d):
	return '{0:f}'.format(d)

def str_isfloat(str):
	try:
		float(str)
		return True
 
	except ValueError:
		return False

def savetip(from_id, to_id, amount):
	con = sqlite3.connect('tipzeny.db')
	c = con.cursor()

	create_table = '''CREATE TABLE IF NOT EXISTS tiplist(from_id int, to_id int, amount text, date_time text)'''
	c.execute(create_table)

	date_str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	amount = str(amount)

	ins = 'insert into tiplist (from_id, to_id, amount, date_time) values (?,?,?,?)'
	tip = (from_id, to_id, amount, date_str)
	c.execute(ins, tip)
	con.commit()
	con.close()

def gettip(user_id):
	con = sqlite3.connect('tipzeny.db')
	c = con.cursor()

	from_ids = c.execute("select * from tiplist where from_id = ?",(user_id,))
	for row in from_ids:
		date = datetime.datetime.strptime(row[3], "%Y/%m/%d %H:%M:%S")
		if datetime.datetime.now() > date + datetime.timedelta(days = 3):
			zeny.move("tippot", "tipzeny-" + str(row[0]), float(row[2]))
			c.execute("delete from tiplist where date_time = ? and from_id = ?", (row[3],row[0]))
	con.commit()

	tos = c.execute("select * from tiplist where to_id = ?",(user_id,))
	for row in tos:
		date = datetime.datetime.strptime(row[3], "%Y/%m/%d %H:%M:%S")
		if datetime.datetime.now() < date + datetime.timedelta(days = 3):
			zeny.move("tippot", "tipzeny-" + str(row[1]), float(row[2]))
			c.execute("delete from tiplist where date_time = ? and from_id = ?", (row[3],row[0]))
	con.commit()
	con.close()


def helptweet(status,txt):
		tweet = "@" + status.user.screen_name + u" " + txt
		api.update_status(status=tweet, in_reply_to_status_id=status.id)

# ツイート処理
def on_tweet(status):
	if status.text.find("RT") == -1 and status.text.find("QT") == -1 and status.user.screen_name != "zenytips":
		if status.text.find("@zenytips") == -1:
			return

		name = status.user.screen_name
		message = status.text[(status.text.find("@zenytips")+10):]
		account = "tipzeny-" + str(status.user.id)

		if re.search("balance", message) or re.search(u"残高", message):
			gettip(status.user.id)
			balance = zeny.getbalance(account,6)
			all_balance = zeny.getbalance(account,0)

			if all_balance < 10:
				f = open('accountlist.json','r')
				json_data = json.load(f)
				if status.user.id in json_data:
					datas = filter(lambda x: x == status.user.id, json_data)
					w = open('accountlist.json','w')
					json.dump(datas, w)
			else:
				f = open('accountlist.json','r')
				json_data = json.load(f)
				if status.user.id not in json_data:
					json_data.append(status.user.id)
					w = open('accountlist.json','w')
					json.dump(json_data, w)


			logger.info("check balance..." + name)
			logger.info(DecimaltoStr(balance) + "ZNY all(" + DecimaltoStr(all_balance) + "ZNY)")
			tweet = "@" + name + " " + DecimaltoStr(balance) + u"ZNY持ってます！"
			if balance < all_balance:
				tweet += u"\n(confirm中" + DecimaltoStr(all_balance-balance) + u"ZNY)"
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

		elif re.search("deposit", message) or re.search(u"入金", message):
			address = zeny.getaccountaddress(account)
			logger.info("get deposit address..." + name)
			logger.info(account + " => " + address)
			tweet = "@" + name + " " + address + u" に送金お願いしますっ！"
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

		elif re.match("withdrawall", message) or re.match(u"全額出金", message):
			m = re.split(" ", message)
			if len(m) < 2:
				helptweet(status, u"withdrawall(全額出金)の使い方\n@￰zenytips withdrawall 受取ZNYアドレス\nhttps://github.com/trasta298/tipzeny/wiki")
				return

			address = m[1]
			balance = zeny.getbalance(account,6)
			tax = 0.01
			payying = float(balance)-tax

			logger.info("withdraw..."+name)

			if round(0-payying,7) >= 0:
				logger.info("-> Not enough ZNY (0.01 > " + str(payying) + ")")
				tweet = "@" + name + u" 残高が足りないみたいですっ！\n所持zny: " + str(balance) + "ZNY"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			validate = zeny.validateaddress(address)
			if not validate['isvalid']:
				logger.info("-> Invalid address")
				tweet = "@" + name + u" アドレスが間違ってるみたいですっ"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			logger.info("-> Sending...")
			txid = zeny.sendfrom(account,address,payying)

			# taxまわりとりあえず後回し
			logger.info("-> Checking transaction...")
			tx = zeny.gettransaction(txid)
			if tx:
				fee = float(tx['fee'])
				logger.info("-> Tax: " + str(fee))
			else:
				fee = 0
				logger.info("-> No Tax")

			zeny.move(account, "taxpot", tax+fee)
			logger.info("-> Fee sent to taxpot: " + str(tax+fee) + "ZNY")
			tweet = "@" + name + u" zenyを引き出しましたっ！(手数料0.01ZNY)\nhttp://namuyan.dip.jp/MultiLightBlockExplorer/gettxid.php?coin=zeny&txid=" + str(txid)
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

			f = open('accountlist.json','r')
			json_data = json.load(f)
			if status.user.id in json_data:
				datas = filter(lambda x: x == status.user.id, json_data)
				w = open('accountlist.json','w')
				json.dump(datas, w)

		elif re.match("withdraw", message) or re.match(u"出金", message):
			m = re.split(" ", message)
			if len(m) < 3 or not str_isfloat(m[2]):
				helptweet(status, u"withdraw(出金)の使い方\n@￰zenytips withdraw 受取ZNYアドレス 出金額(ZNY)\nhttps://github.com/trasta298/tipzeny/wiki")
				return

			address = m[1]
			amot= float(m[2])
			balance = zeny.getbalance(account,6)
			tax = 0.01
			amount = amot-tax

			if amount <= 0:
				tweet = "@" + name + u" 0以下の数は指定できません！"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			logger.info("withdraw..."+name)

			if round(Decimal(amount)-balance,7) >= 0:
				logger.info("-> Not enough ZNY ("+ DecimaltoStr(balance) + " < " + str(amount) + ")")
				tweet = "@" + name + u" 残高が足りないみたいですっ！\n所持zny: " + DecimaltoStr(balance) + "ZNY"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			validate = zeny.validateaddress(address)
			if not validate['isvalid']:
				logger.info("-> Invalid address")
				tweet = "@" + name + u" アドレスが間違ってるみたいですっ"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			logger.info("-> Sending...")
			txid = zeny.sendfrom(account,address,amount)

			# taxまわりとりあえず後回し
			logger.info("-> Checking transaction...")
			tx = zeny.gettransaction(txid)
			if tx:
				fee = float(tx['fee'])
				logger.info("-> Tax: " + str(fee))
			else:
				fee = 0
				logger.info("-> No Tax")

			zeny.move(account, "taxpot", tax+fee)
			logger.info("-> Fee sent to taxpot: " + str(tax+fee) + "ZNY")
			tweet = "@" + name + u" zenyを引き出しましたっ！(手数料0.01ZNY)\nhttp://namuyan.dip.jp/MultiLightBlockExplorer/gettxid.php?coin=zeny&txid=" + str(txid)
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

			if float(balance)-amount < 10:
				f = open('accountlist.json','r')
				json_data = json.load(f)
				if status.user.id in json_data:
					datas = filter(lambda x: x == status.user.id, json_data)
					w = open('accountlist.json','w')
					json.dump(datas, w)

		elif re.match("rain", message) or re.match(u"撒き銭", message):
			m = re.split(" ", message)
			if len(m) < 2 or not str_isfloat(m[1]):
				helptweet(status, u"rain(撒き銭)の使い方\n@￰zenytips rain 撒銭額(ZNY)\nhttps://github.com/trasta298/tipzeny/wiki")
				return
			amount = float(m[1])
			balance = zeny.getbalance(account,6)

			if amount <= 0:
				tweet = "@" + name + u" 0以下の数は指定できません！"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			logger.info("Raining..."+str(amount)+"ZNY from "+name)

			if round(Decimal(amount)-balance,7) > 0:
				logger.info("-> Not enough ZNY ("+ DecimaltoStr(balance) + " < " + str(amount) + ")")
				tweet = "@" + name + u" 残高が足りないみたいですっ！\n所持zny: " + DecimaltoStr(balance) + "ZNY"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			f = open('accountlist.json','r')
			json_data = json.load(f)
			nmb = len(json_data)
			if nmb == 0:
				tweet = "@" + name + u" 対象者がいないみたいです。。。"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)

			mon = round(amount/nmb,7)
			for userid in json_data:
				to_account = "tipzeny-" + str(userid)
				zeny.move(account,to_account,mon)
			logger.info("-> Sent.")

			tweet = "@" + name + u" " + str(nmb) + u"人にそれぞれ " + str(mon) + u"ZNYずつ送りましたっ！"
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

		elif re.match("send", message) or re.match(u"送金", message):
			m = re.split(" ", message)
			if len(m) < 3 or not str_isfloat(m[2]):
				helptweet(status, u"send(送金)の使い方\n@￰zenytips send @￰twitterアカウント 投銭額(ZNY)\nhttps://github.com/trasta298/tipzeny/wiki")
				return
			if m[1][0] != "@":
				helptweet(status, u"send(送金)の使い方\n@￰zenytips send @￰twitterアカウント 投銭額(ZNY)\nhttps://github.com/trasta298/tipzeny/wiki")
				return

			to = m[1][1:]
			amount = float(m[2])
			balance = zeny.getbalance(account,6)

			if amount <= 0:
				tweet = "@" + name + u" 0以下の数は指定できません！"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			logger.info("Sending..."+str(amount)+"ZNY from "+name+" to "+to)

			if round(Decimal(amount)-balance,7) > 0:
				logger.info("-> Not enough ZNY ("+ DecimaltoStr(balance) + " < " + str(amount) + ")")
				tweet = "@" + name + u" 残高が足りないみたいですっ！\n所持zny: " + DecimaltoStr(balance) + "ZNY"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			try:
				to_user = api.get_user(to)

			except:
				logger.info("-> User not found.")
				tweet = "@" + name + u" 送り主(" + to + u")が見つかりませんでした…"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			to_account = "tipzeny-" + str(to_user.id)
			zeny.move(account,to_account,amount)
			logger.info("-> Sent.")
			tweet = "@" + to + u" りん姫より @" + name + u" さんから" + str(amount) + u"ZNYのお届け物だよっ！"
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

		elif re.match("tip", message) or re.match(u"投銭", message):
			m = re.split(" ", message)
			if len(m) < 3 or not str_isfloat(m[2]):
				helptweet(status, u"tip(投銭)の使い方\n@￰zenytips tip @￰twitterアカウント 投銭額(ZNY)\nhttps://github.com/trasta298/tipzeny/wiki")
				return
			if m[1][0] != "@":
				helptweet(status, u"tip(投銭)の使い方\n@￰zenytips tip @￰twitterアカウント 投銭額(ZNY)\nhttps://github.com/trasta298/tipzeny/wiki")
				return

			to = m[1][1:]
			amount = float(m[2])
			balance = zeny.getbalance(account,6)

			if amount <= 0:
				tweet = "@" + name + u" 0以下の数は指定できません！"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			logger.info("Tip..."+str(amount)+"ZNY from "+name+" to "+to)

			if round(Decimal(amount)-balance,7) > 0:
				logger.info("-> Not enough ZNY ("+ DecimaltoStr(balance) + " < " + str(amount) + ")")
				tweet = "@" + name + u" 残高が足りないみたいですっ！\n所持zny: " + DecimaltoStr(balance) + "ZNY"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			try:
				to_user = api.get_user(to)

			except:
				logger.info("-> User not found.")
				tweet = "@" + name + u" 送り主(" + to + u")が見つかりませんでした…"
				api.update_status(status=tweet, in_reply_to_status_id=status.id)
				return

			to_account = "tipzeny-" + str(to_user.id)
			savetip(status.user.id, to_user.id, amount)
			zeny.move(account,"tippot",amount)
			logger.info("-> Sent.")
			tweet = "@" + to + u" りん姫より @" + name + u" さんから" + str(amount) + u"ZNYのお届け物だよっ！ 3日以内にbalanceして受け取ってね！"
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

		elif len(message) < 2:
			helptweet(status, u"りん姫の使い方はここっ\nhttps://github.com/trasta298/tipzeny/wiki")


#3029861817
class Listener(StreamListener):
    def on_status(self, status):
    	on_tweet(status)
        return True

    def on_error(self, status_code):
        logger.error('エラー発生: ' + str(status_code))
        return True

    def on_connect(self):
        logger.info('Streamに接続しました')
        return

    def on_disconnect(self, notice):
        logger.info('Streamから切断されました:' + str(notice.code))
        return

    def on_limit(self, track):
        logger.warning('受信リミットが発生しました:' + str(track))
        return

    def on_timeout(self):
        logger.info('タイムアウト')
        return True

    def on_warning(self, notice):
        logger.warning('警告メッセージ:' + str(notice.message))
        return

    def on_exception(self, exception):
        logger.error('例外エラー:' + str(exception))
        return


# main
if __name__ == '__main__':
    auth = get_oauth()
    api = API(auth)
    stream = Stream(auth, Listener(), secure=True)
    stream.userstream()