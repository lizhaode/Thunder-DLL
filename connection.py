# SerCvs is Server Conversation

import urls

class SerCvs:

	def __init__(self,channel=''):
		self.channel = ''
		self.response = None
		if channel :
			self.SetChnnel(channel)
			self.UpdateResponse()
		pass

	def SetChnnel(self,c):
		self.channel = '?channel=' + c

	def GetResponse(self):
		return self.response

	def GetJDatas(self):
		if self.response :
			return self.response.read()
		
		return None

	def UpdateResponse(self):
		import urllib
		try:
			self.response = urllib.urlopen(urls.SerIntfUrl + self.channel)
		except:
			self.response = None




if __name__ == '__main__':
	sc = SerCvs('30')
	jdata = sc.GetJDatas()
	print jdata
