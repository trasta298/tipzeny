#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import logging
import logging.config
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API

# bitcoind
rpc_user=""
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

# ツイート処理
def on_tweet(status):
	if status.text.find("RT") == -1 and status.text.find("QT") == -1 and status.user.screen_name != "zeny_sis":
		if status.text.find("@zeny_sis") == -1:
			return

		name = status.user.screen_name
		message = re.sub("@zeny_sis ", "", status.text)
		account = "tipzeny-" + str(status.user.id)

		if re.match("balance", message):
			balance = DecimaltoStr(zeny.getbalance(account,6))
			all_balance = DecimaltoStr(zeny.getbalance(account,0))
			logger.info("check balance..." + name)
			logger.info(balance + "ZNY all(" + all_balance + "ZNY)")
			tweet = "@" + name + " " + balance + u"ZNY持ってます！"
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

		elif re.match("deposit", message):
			address = zeny.getaccountaddress(account)
			logger.info("get deposit address..." + name)
			logger.info(account + " => " + address)
			tweet = "@" + name + " " + address + u" に送金お願いしますっ！"
			api.update_status(status=tweet, in_reply_to_status_id=status.id)

		elif re.match("withdraw", message):
			m = re.split(" ", message)
			if len(m) < 4:
				return
			address = m[1]
			amount = float(m[2])


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