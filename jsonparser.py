


class JsonObj(object):
    ''' Server Json data object.
        One piece of Server Json data is a SJObj instance.
        The key name of data's dictionary is SJObj's properties.
    '''

    def __init__(self,SJData):
        ''' SJData is a dict about one of server json data.
            When you input a available SJData, the SJObj instance
            will delegate the data of dict.
        '''
        self.__dict__ = SJData

    def toSLetterJson(self):
        if self.__dict__.has_key('channel'):
            return None
        elif self.__dict__.has_key('speed'):
            Dict = {}
            Dict["id"] = self.__dict__["id"]
            Dict["name"] = self.__dict__["name"]
            Dict["size"] = self.__dict__["size"]
            Dict["image"] = self.__dict__["image"]
            Dict["icon"] = self.__dict__["icon"]
            Dict["starttime"] = self.__dict__["starttime"]
            Dict["endtime"] = self.__dict__["endtime"]
            Dict["pkg"] = self.__dict__["pkg"]
            Dict["apk"] = self.__dict__["apk"]
            Dict["status"] = "None"

            return JsonObj(Dict)

        else:
            return JsonObj(self.__dict__)






class JsonMgr(object):
    '''This class is a Manager that tow types string conversion
        between Python and Json
    '''
    def __init__(self):
        pass

    @staticmethod
    def j2p(jstr):
        ''' json to Python string
        '''
        import json
        return json.loads(jstr)

    @staticmethod
    def p2j(pstr):
        ''' python string to json
        '''
        import json
        return json.dumps(pstr)


class ServerJson(JsonMgr):
    '''This is a object of server data, Only need you provide datas
        from server interface
    '''
    def __init__(self,jstr = None):
        ''' jstr is Server Json string
        '''
        self.SJObjs = []

        if jstr:
            self.SetJDatas(jstr)
        pass

    def SetJDatas(self,jstr):
        '''input json datas string, which get from server.
        '''

        strJson = self.j2p(jstr)

        # By default, The json of server type is list. 
        # Otherwise an error occurred.
        if isinstance(strJson,list):
            for one in strJson:
                self.SJObjs.append(JsonObj(one))


class BulletinJson(JsonMgr):
    def __init__(self,jstr = None):
        if jstr:
            self.SetJDatas(jstr)


    def SetJDatas(self,jstr):
        strJson = self.j2p(jstr)
        if isinstance(strJson,dict):
            self.__dict__ = strJson

class LetterJson(JsonMgr):
    def __init__(self,jstr = None):
        self.LJObjs = []
        if jstr :
            self.SetJDatas(jstr)

    def SetJDatas(self,jstr):
        strJson = self.j2p(jstr)
        if isinstance(strJson, list):
            for one in strJson:
                self.LJObjs.append(JsonObj(one))

    def toJson(self):
        jsonArray = []
        for one in self.LJObjs:
            jsonArray.append(one.__dict__)
        return JsonMgr.p2j(jsonArray)





if __name__ == '__main__':
    from pprint import *
    f = open(r"C:\Users\Mazg\AppData\Local\Droid4X\bt\p2b.json")

    sj = BulletinJson(f.read())
    print sj.JObj.channel
    '''
    for one in sj.SJDatas:
        import time
        print time.localtime(float(one.starttime))
    '''
