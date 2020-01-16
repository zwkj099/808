import TAException
__funclist         = []
__argslist         = []
__func             = None
testinfo           = {}

def readtestfile():
    from xml.dom import minidom
    try:
        testfile = "./DataReady/dataready.xml"
        dom = minidom.parse(testfile)
        tmp = dom.getElementsByTagName("TestList")
        if tmp != []:
            if tmp[0].getElementsByTagName("Test") != []:
                testlist =  tmp[0].getElementsByTagName("Test")
                for item in testlist:
                    func = ""
                    arg  = ""
                    try:
                        func, arg = item.childNodes[0].data.split(",",1)
                    except:
                        func = item.childNodes[0].data
                        arg  = ""
                    __funclist.append(func)
                    __argslist.append(arg)
        keyvalueslst = dom.getElementsByTagName("KeyValues")
        for keyvalue in keyvalueslst:
            key   = keyvalue.getElementsByTagName("Key")[0].childNodes[0].data
            value = keyvalue.getElementsByTagName("Value")[0].childNodes[0].data
            testinfo[key] = value
    except:
            raise TAException.taexception(3,"\n"+testfile+" format is not correct\n","TEST_AUTOMATION_ERROR")

    return [__funclist,__argslist,testinfo]

def dynamicimport(__funclist):
    import sys
    sys.path.append(testinfo['TestLibPath'])
    del sys
    # print __funclist
    try:
        __func = map(__import__, __funclist)
    except ImportError, err:
        print err
        raise TAException.taexception(4,"import module error:\n"+err.message,"TEST_AUTOMATION_ERROR")
    return __func

def datatest(tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id):

    __funclist,__argslist,testinfo=readtestfile()
    __func=dynamicimport(__funclist)

    for test in range(len(__func)):
        __func[test].main(__argslist[test], testinfo, tp,link, mobile, extrainfo_id, idlist, wsid,deviceid,port,vehicle_id)

