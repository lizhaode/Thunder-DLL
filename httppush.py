import httplib, urllib
import urlparse


def http_post(url, header, param):
	#formatparam = urllib.urlencode(param)
	host = urlparse.urlparse(url).netloc
	#print host
	interface = urlparse.urlparse(url).path
	#print interface
	try:
		conn = httplib.HTTPConnection(host)
		conn.request("POST", interface, param, header)
		return conn.getresponse().read()
	except:
		return "error"

if __name__ == '__main__':
	print http_post("http://log.droid4x.cn/dxadmin/launchclick.php", {"CLIENT_VERSION" : "0.8.3"}, r"26	28:D2:44:C6:06:99	null	ooppp	null	-1163005939	5de6f4cac75fad7b4bd1b035d74219f6")