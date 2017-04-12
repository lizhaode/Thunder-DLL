#from thunder import *
from center import *
from logger import *
from urls import *
from time import *


from sys import *


def main():
    if len(sys.argv) > 2:
        urls.DataPath = sys.argv[2].replace('/','\\')
    else:
        exit()

    logname = "downloader%s.log"%(strftime("%Y-%m-%d", gmtime()))
    log_init(log_path()+logname)

    c = Center()
    c.InitThunder()
    c.InitLetterJsonObjs(b2pPath())
    c.InitPlayerJsonObj(p2bPath())
    if c.p2bJson and c.p2bJson.channel:
        c.InitServerJsonObjs(c.p2bJson.channel)

    if c.s2bJsons :
        c.InitBigData()
        c.Dam()
        c.Run()
        c.SendLetter(b2pPath())

    autolog(4, "exit main() for normal")

if __name__ == '__main__':
    try:
        main()
    except:
        exit(0)
