
import Hbase,weijin
def data_comparison(mobile,pdict,ex808dict,sensordict):

    result = Hbase.HbaseData(mobile)
    for k in result[0]:
        if k == result[0][0]:
            row_key = k.encode('hex')
        else:
            data = k
    wj = weijin.wgs2gcj(pdict['wei'], pdict['jin'])

    reswei = round(float(wj[0]), 6)
    resjin = round(float(wj[1]), 6)

    resx = [data['0:SIM_CARD'][0], data['0:ALARM'][0], data['0:STATUS'][0], data['0:LONGTITUDE'][0],
            data['0:LATITUDE'][0], \
            data['0:HEIGHT'][0], data['0:SPEED'][0], data['0:ANGLE'][0], data['0:GPS_MILE'][0],
            data['0:AD_HEIGHT_ONE'][0], data['0:OIL_TANK_ONE'][0]]

    ress = [mobile, pdict['alarm'], pdict['status'], resjin, reswei, float(pdict['high']), pdict['speed'],
            float(pdict['direction']), ex808dict['mel'], sensordict['AD'], float(ex808dict['Oil'])]

    for m in range(len(resx)):
        if str(resx[m]).find(str(ress[m])) == -1:
            print "upload and hbase not match"
            print data['0:SIM_CARD'][1]
            print "error:" + str(resx[m]) + " " + str(ress[m])
            break
        print str(resx[m]) + " " + str(ress[m])
