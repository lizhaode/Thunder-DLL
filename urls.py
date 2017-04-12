SerIntfUrl = r'http://api.droid4x.cn/api/getPopups'

DataPath = ''



import os
import sys

def log_path():
	return DataPath + "log\\"

def bt_path():
	return DataPath + "bt\\"

def file_path():
	return bt_path() + 'files\\'

def work_path():
	return os.getcwd() + '\\'

def p2bPath():
	return bt_path() + r'p2b.json'

def b2pPath():
	return bt_path() + r'b2p.json'
