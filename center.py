


from connection import *
from dam import *
from jsonparser import *
from urls import *
from thunder import *
from logger import *
from bigdata import *

import ntpath



class Center(object):
	def __init__(self):
		self.s2bJsons = None
		self.p2bJson = None
		self.b2pJsons = None
		self.th = None
		self.dlData = None
		self.speed = 50
		self.postData = Data()
		self.poster = BigData()


	def InitServerJsonObjs(self,channel):
		connection = SerCvs(channel)
		datas = connection.GetJDatas()
		autolog(4, "server json = %s" % datas)
		if datas :
			self.s2bJsons = ServerJson(datas)


	def InitPlayerJsonObj(self,path):
		try:
			f = open(path)
			self.p2bJson = BulletinJson(f.read())
			f.close()
		except Exception, e:
			pass

	def InitLetterJsonObjs(self,path):
		f = open(path,'a+')
		self.b2pJsons = LetterJson(f.read())
		f.close()


	def InitThunder(self):
		self.th = thunder(os.path.abspath(work_path()))
		if not self.th.init():
			autolog(4, "thunder init error")

	def InitBigData(self):
		self.postData.mac = self.p2bJson.mac
		self.postData.version = self.p2bJson.version
		self.postData.cid = self.p2bJson.channel
		self.postData.did = self.p2bJson.did


	def Dam(self):
		dam = Dam(self.s2bJsons.SJObjs,self.p2bJson, self.b2pJsons.LJObjs)
		dam.DamDatas()

	def AddDownload(self,data):
		self.dlData = data.toSLetterJson()
		self.dlData.status = u"downloading"
		self.speed = int(data.speed)
		autolog(4, "limit speed = %d" % self.speed)

		# post statistics
		self.postData.id = data.id
		self.postData.type = Step.StartDownload
		self.poster.PostOne(self.postData)

		d_list = [data.image, data.apk, data.icon]
		for key in ('image', 'apk', 'icon'):
			url = data.__dict__[key]
			if not os.path.exists(file_path() + ntpath.basename(url)):
				self.dlData.__dict__[key] = None
				self.th.add_task_ex(url, file_path(), ntpath.basename(url), True)
			else:
				self.dlData.__dict__[key] = file_path() + ntpath.basename(url)

		

	def StartDownload(self):
		import time
		self.th.start()
		self.th.set_speedlimit(self.speed)
		autolog(4, "set thunder speed:%s"%(str(self.speed)))

		for key in ('image', 'apk', 'icon'):
			if self.dlData.__dict__[key] :
				continue
			while 1:
				time.sleep(1)
				if self.th.task_count() <= 0:
					autolog(1, "thunder has no task!")
					break
				info = self.th.peek_info()
				status = self.th.peek_info().status
				autolog(4, "%s download percent:%.2f%%"%(str(info.filename), info.precent*100))
				autolog(4, "%s download speed:%d byte/s"%(str(info.filename), info.speed))
				if status in (0,1):
					self.dlData.__dict__[key] = ''
					self.th.start_next()
					autolog(1, "%s download error:%s"%(str(info.filename), str(info.errortype)))
					break
				if status== 4:
					autolog(1, "%s download complete!"%(str(info.filename)))
					self.dlData.__dict__[key] = file_path() + self.th.peek_info().filename
					self.th.start_next()
					break

		self.dlData.status = u"downloaded"
		self.b2pJsons.LJObjs.append(self.dlData)
		self.dlData = None

		self.postData.type = Step.DownloadOver
		self.poster.PostOne(self.postData)

	def Run(self):
		autolog(4, "Run s2bJsons count = %d" % len(self.s2bJsons.SJObjs))
		for one in self.s2bJsons.SJObjs:
			autolog(4, "current run s2bJson = " + one.name.encode("utf-8") + str(one.pkg))
			self.AddDownload(one)
			self.StartDownload()

	def SendLetter(self,path):
		f = open(path,'w')
		f.write(self.b2pJsons.toJson())
		f.close()

if __name__ == '__main__':
	c = Center()
	c.InitThunder()
	c.InitLetterJsonObjs(b2pPath())
	c.InitPlayerJsonObj(p2bPath())
	if c.p2bJson and c.p2bJson.channel:
		c.InitServerJsonObjs(c.p2bJson.channel)

	c.Dam()
	c.Run()
	c.SendLetter(b2pPath())





