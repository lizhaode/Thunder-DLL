

from logger import *
import httppush
import urls

class Step:
	StartDownload = '20'
	DownloadOver = '21'


class Data(object):
	def __init__(self):
		self.type = 'null'
		self.mac = 'null'
		self.version = 'null'
		self.cid = 'null'
		self.result = 'null'
		self.id = 'null'
		self.did = 'null'


class BigData(object):
	def __init__(self):
		pass

	def PostOne(self,data):
		
		strData = self.MakeData(data)
		autolog(4, "post data : %s " % strData)
		httppush.http_post(r"http://log.droid4x.cn/dxadmin/launchclick.php", {"CLIENT_VERSION" : data.version}, strData)


	def MakeData(self,data):
		listData = [data.type, data.mac, data.version, data.cid, data.id, data.did ]
		strData = []
		for one in listData:
			if not one:
				one = 'null'
			one = str(one).replace('\t','#').replace('\n','#')

			strData.append(one)

		return '\t'.join(strData)




if __name__ == '__main__':

	bd = BigData()
	d = Data()
	d.type = Step.StartDownload
	d.mac = "28:D2:44:EC:D9:B7"
	d.version = '0.8.3'
	d.cid = "ooppp"
	d.result =''
	d.id = 3
	d.did = "3a87e348a964e1404255c83de013c0a6"

	bd.PostOne(d)


