#!/usr/bin/env python
#-*- coding:utf-8 -*-

from decimal import *
import json
import re
import logging
import sqlite3
import string
import logging.config
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import datetime
import time
import random

# bitcoind
rpc_user=''
rpc_password=''
ip=''
port=''
zeny = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password,ip,port))

# logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def get_oauth():
	consumer_key = ''
	consumer_secret = ''
	access_key = ''
	access_secret = ''

#decimalからstringへ
def DecimaltoStr(d):
	n = '{0:f}'.format(d).strip('0')
	if n[-1] == '.':
		n += '0'
	return n

#数字かどうか判定
def str_isDecimal(str):
	try:
		Decimal(str)
		return True
 
	except ValueError:
		return False

#空白で文字列を分割
def split_command(message):
	m = re.split(" ", message)
	while True:
		if m.count("") == 0:
			break
		else:
			n = m.index("")
			del m[n]
	return m

def add_addresslist(userid, addr):
	con = sqlite3.connect('addresslist.db')
	c = con.cursor()
	create_table = '''CREATE TABLE IF NOT EXISTS addresslist(account int primary key, address text)'''
	c.execute(create_table)
	ins = 'replace into addresslist (account, address) values (?,?)'
	dat = (userid, addr)
	c.execute(ins, dat)
	con.commit()
	con.close()

def get_addersslist(userid):
	con = sqlite3.connect('addresslist.db')
	c = con.cursor()
	c.execute("select * from addresslist where account = ?",(userid,))
	data = c.fetchone()
	con.commit()
	con.close()
	if data:
		return data[1]
	return False

def add_rainlist(userid,screen_name):
	con = sqlite3.connect('rainlist.db')
	c = con.cursor()

	create_table = '''CREATE TABLE IF NOT EXISTS rainlist(account int, name text)'''
	c.execute(create_table)

	if in_rainlist(userid):
		return
	
	ins = 'insert into rainlist (account, name) values (?,?)'
	tip = (userid, screen_name)
	c.execute(ins, tip)
	con.commit()
	con.close()

def get_rainlist(n):
	con = sqlite3.connect('rainlist.db')
	c = con.cursor()
	rainlist = []
	tos = c.execute("select * from rainlist")
	for row in tos:
		rainlist.append(row[n])
	con.commit()
	con.close()
	return rainlist

def in_rainlist(userid):
	if userid in get_rainlist(0):
		return True
	return False

def delete_rainlist(userid):
	if in_rainlist(userid):
		con = sqlite3.connect('rainlist.db')
		c = con.cursor()
		c.execute("delete from rainlist where account = ?",(userid,))
		con.commit()
		con.close()

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

def gettip(userid):
	con = sqlite3.connect('tipzeny.db')
	c = con.cursor()

	from_ids = c.execute("select * from tiplist where from_id = ?",(userid,))
	for row in from_ids:
		date = datetime.datetime.strptime(row[3], "%Y/%m/%d %H:%M:%S")
		if datetime.datetime.now() > date + datetime.timedelta(days = 3):
			zeny.move("tippot", "tipzeny-" + str(row[0]), float(row[2]))
			c.execute("delete from tiplist where date_time = ? and from_id = ?", (row[3],row[0]))
	con.commit()

	tos = c.execute("select * from tiplist where to_id = ?",(userid,))
	for row in tos:
		date = datetime.datetime.strptime(row[3], "%Y/%m/%d %H:%M:%S")
		if datetime.datetime.now() < date + datetime.timedelta(days = 3):
			zeny.move("tippot", "tipzeny-" + str(row[1]), float(row[2]))
			c.execute("delete from tiplist where date_time = ? and from_id = ?", (row[3],row[0]))
	con.commit()
	con.close()

