import ctypes
from ctypes import *
import struct

class thunder_info(ctypes.Structure):
    _fields_ = [
        ("status", c_int),
        ("errortype", c_int),
        ("filename", c_wchar*260),
        ("szreserverd0", c_wchar*260),
        ("totalsize", c_int64),
        ("totaldownload", c_int64),
        ("precent", c_float),
        ("nreserved0", c_int),
        ("srctotal", c_int),
        ("srcusing", c_int),
        ("nreserved1", c_int),
        ("nreserved2", c_int),
        ("nreserved3", c_int),
        ("nreserved4", c_int),
        ("nreserved5", c_int64),
        ("donationp2p", c_int64),
        ("nreserved6", c_int64),
        ("donationorgin", c_int64),
        ("donationp2s", c_int64),
        ("nreserved7", c_int64),
        ("nreserved8", c_int64),
        ("speed", c_int),
        ("speedp2s", c_int),
        ("speedp2p", c_int),
        ("isoriginusable", c_bool),
        ("hashpercent", c_float),
        ("iscreatingfile", c_int),
        ("reserved", c_long)
        ]

class task_param(ctypes.Structure):
    _fields_ = [
        ("nreserved1", c_int),
        ("taskurl", c_wchar*2084),
        ("refurl", c_wchar*2084),
        ("cookies", c_wchar*4096),
        ("filename", c_wchar*260),
        ("szreserved0", c_wchar*260),
        ("savepath", c_wchar*260),
        ("hreserved", c_void_p),
        ("breserved", c_bool),
        ("szreserved1", c_wchar*64),
        ("szreserved2", c_wchar*64),
        ("isonlyoriginal", c_bool),
        ("nreserved1", c_int),
        ("disableautorename", c_bool),
        ("isresume", c_bool),
        ("reserved", c_long)
        ]

class thunder(object):
    def __init__(self, thunderdllpath):
        '''
        thunder dll wrapper
        input thunderdllpath when __init__
        '''
        super(thunder, self).__init__()
        self.lib = None
        self.dllpath = thunderdllpath + r"/xldl.dll"
        self.missions = []
        self.urls = []
        self.downloading = False
        self.info = thunder_info()

    def init(self):
        '''
        load library by dllpath
        return True if success, or return False
        '''
        try:
            self.lib = ctypes.cdll.LoadLibrary(self.dllpath)
            return self.lib.XL_Init()
        except:
            return False

    def add_task_ex(self, url, localpath, filename, iscontinue):
    	'''
    	add task to download list
    	@url : something like "http://dl.haima.me/download/r.zip"
    	@localpath : "c:/a/b/"
    	@filename : 
    	@iscontinue : (bool) old download mission
    	'''
        if url in self.urls:
            return 0
    	param = task_param()
    	param.taskurl = url
    	param.savepath = localpath
    	param.filename = filename
    	param.isresume = iscontinue
        self.lib.XL_CreateTask.argtypes = [POINTER(task_param)]
    	h = self.lib.XL_CreateTask(byref(param))
    	if not h:
    		return 0
        self.urls.append(url)
    	self.missions.append(h)
    	return h

    def peek_info(self):
        '''return infomation of current mission '''
        ctypes.memset(ctypes.addressof(self.info), 0, ctypes.sizeof(self.info))
        self.lib.XL_QueryTaskInfo.argtypes = [c_int, POINTER(thunder_info)]
        if not self.lib.XL_QueryTaskInfo(self.missions[0], byref(self.info)):
            return None
        return self.info

    def start(self):
        '''
        start first/current mission
        return True if success, or return False otherwise
        '''
        if len(self.missions) <= 0:
            return False
        if self.lib.XL_StartTask(self.missions[0]):
        	self.downloading = True
        	return True
        return False

    def start_next(self):
        '''
        start seccond mission
        return True if success, or return False otherwise
        '''
        self.stop()
    	self.missions.pop(0)
    	if len(self.missions) <= 0:
    		return False
    	return self.start()

    def stop(self):
    	'''
    	stop current mission
    	return True, or False
    	'''
    	if self.lib.XL_StopTask(self.missions[0]):
    		self.downloading = False
    		return True
    	return False

    def set_speedlimit(self, kbps):
    	'''
    	set download speed limit
    	@kbps : int32, KBps
    	'''
    	self.lib.XL_SetSpeedLimit(kbps)

    def task_count(self):
    	''' return missions count for current '''
    	return len(self.missions)

    def is_downloading(self):
    	''' return True if downloading, or return False '''
    	return downloading

    def test(self):
        ''' pass '''
        print self.lib

if __name__ == '__main__':
    import time
    th = thunder("..//..//@bin//")
    if not th.init():
        print 'load error'
        
    print "addtask=", th.add_task_ex(r"http://dl.haima.me/download/DXDown/win/000000133/Droid4XInstaller.exe", r".//", "installer.exe", True)

    if th.start():
        print "start ok"
    else:
    	print "start failed"
    th.set_speedlimit(50)
    while True:
        time.sleep(1)
        info = th.peek_info()
        print info.precent
        if info.precent > 0.1:
            print "addtask=", th.add_task_ex(r"http://dl.haima.me/download/DXDown/win/000000133/Droid4XInstaller.exe", r".//", "installer.exe", True)
            th.start_next()
