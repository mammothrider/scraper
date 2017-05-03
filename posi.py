import json
import requests
import time

url = r"http://api.map.baidu.com/geocoder/v2/"
para = {"address":0, "output":"json", "ak":"W5CCXR7wFKTcApjwCz5aeZeQoeK1b0rH","callback":"showLocation"}
file = open("e:\data.csv", "r").readlines()
res = []
for line in file[1:]:
    tmp = line.strip().split(",")
    while tmp[-1] == '': 
        tmp.pop()
    
    para["address"] = tmp[-1]
    jsonData = requests.get(url, params = para).text
    #print(jsonData)
    s = jsonData.find("{")
    jsonData = jsonData[s:-1]
    #print(jsonData)
    jsonData = json.loads(jsonData)
    #print(jsonData)
    try:
        lng, lat = jsonData["result"]["location"]["lng"], jsonData["result"]["location"]["lat"]
    except:
        print(jsonData)
        lng, lat = 0, 0
    tmp += [str(lng), str(lat)]
    res.append(",".join(tmp) + "\n")
    
file = open(r"e:\newData.csv", "w")
file.write("".join(res))
file.close()