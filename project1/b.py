import urllib.request
import json
import time

while True:
    TS1 = urllib.request.urlopen("https://api.thingspeak.com/channels/992056/fields/1.json?api_key=57MQYTPTFGYKBGJ2")
    TS2 = urllib.request.urlopen("https://api.thingspeak.com/channels/992056/fields/2.json?api_key=57MQYTPTFGYKBGJ2")
    res1 = TS1.read()
    res2 = TS2.read()
    data1 = json.loads(res1)
    data2 = json.loads(res2)

    i = 0
    while(i!=len(data1['feeds'])):
        if(data1['feeds'][i]['field1']!='' and data1['feeds'][i]['field1'] is not None):
            print('Pulse')
            print(data1['feeds'][i]['field1'],data1['feeds'][i]['created_at'])
            print('\n')
        if(data2['feeds'][i]['field2']!='' and data2['feeds'][i]['field2'] is not None):
            print('Temp')
            print(data2['feeds'][i]['field2'])
            print(data2['feeds'][i]['created_at'].split('T')[0])
            print(data2['feeds'][i]['created_at'].split('T')[1])
            print('\n')
        else:
            pass
        i+=1
    time.sleep(5)
    TS1.close()
    TS2.close()