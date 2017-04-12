

class Dam(object):
	''' Dam will filter out some datas which
		doesn't need to download.
	'''

	def __init__(self, SJObjs = [], PObj = None, LterObjs = []):
		self.SJObjs = SJObjs
		self.PObj = PObj
		self.LterObjs = LterObjs

		pass

	def DamDatas(self):
		try:
			tempObjs = self.SJObjs[:]
			for one in tempObjs :
				# 必备判断条件
				if not (self.IsAvailableTime(one) and self.IsUnInstall(one) and self.IsUnPush(one)):
					self.SJObjs.remove(one)
					continue


				if not self.IsDestine(one):
					# 不在购物车，不在忽略列表中，证明是老接口 静默下载 
					if not self.IsIgnore(one) and not self.IsOrder(one):
						if not self.IsSilent(one):
							self.SJObjs.remove(one)
							continue

					# 根据需求推理，不在购物车内，就不下载
					elif not self.IsOrder(one):
						self.SJObjs.remove(one)
						continue
						
		except Exception, e:
			raise e

	# 服务器预定标记是否为 1
	def IsDestine(self, JsonObj):
		try:
			return bool(int(JsonObj.destine))
		except Exception, e:
			return False

	# 服务器静默标记是否为 1
	def IsSilent(self,JsonObj):
		'''	Server has a sign what mark the download
			effect or not.
		'''
		try:
			return bool(int(JsonObj.silent))
		except Exception, e:
			return False

	# 是否在可用时间段内
	def IsAvailableTime(self,JsonObj):
		try:
			import time
			curTime = time.time()
			return int(curTime) >= int(JsonObj.starttime) and int(curTime) < int(JsonObj.endtime)

		except Exception, e:
			return False

	# 是否未安装过
	def IsUnInstall(self,JsonObj):
		try:
			return len(set(self.PObj.packages) & set(JsonObj.pkg.split(','))) == 0
		except Exception, e:
			return False

	# 是否未推送过
	def IsUnPush(self,JsonObj):
		for one in self.LterObjs:
			if one.pkg.split(',')[0] == JsonObj.pkg.split(',')[0]:
				return False

		return True 

	# 是否在购物车内
	def IsOrder(self, JsonObj):
		try:
			return JsonObj.id in set(self.PObj.order)
		except Exception, e:
			return False

	# 是否被用户忽略
	def IsIgnore(self, JsonObj):
		try:
			return JsonObj.id in set(self.PObj.ignore)
		except Exception, e:
			return False



		

