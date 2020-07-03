#!/usr/bin/env python3
import urllib.request,json,pymysql,sys,datetime,time
sys.path.append("/root/Python/Video_Monitor")
from model.mariadb import insert
def Huoqu_status(ztxx):
    ztaddr=ztxx[1]
    ztstatus=[]
    for url in ztaddr:
        try:
            req=urllib.request.urlopen(url)
        #捕捉异常
        except TypeError as e:
            return e
        except urllib.error.HTTPError:
            ztstatus.append(404)
        except urllib.error.URLError:
            ztstatus.append(408)
        else:
            ztstatus.append(req.getcode())
    return ztstatus
def Readjson(path):
    #读取json视频列表为对象
    try:
        with open(path, 'r') as f:
            list = json.load(f)
    except FileNotFoundError as e:
        return e,None
    except json.decoder.JSONDecodeError as e:
        return e,None
    #拿到第一次嵌套的list
    else:
    #遍历拿到第二层嵌套的dict返回 
        ztname=[]
        ztaddr=[]
        for x in range(len(list)):
            ztname.append(list[x][0])
            ztaddr.append(list[x][1])
        ztxx=[ztname,ztaddr]
        return None,ztxx
if __name__ == "__main__":
    while True:
        now = datetime.datetime.now()
        if now.minute==10 or now.minute==20 or now.minute==30 or now.minute==40 or now.minute==50 or now.minute==00:
            #时间戳
            tick = datetime.datetime.now()
            ticks=tick.strftime('%Y-%m-%d %H:%M')
            print(ticks)
            path="video_list.json"
            req=Readjson(path)
            print(req[0])
            if req[0] == None:
                ztstatus=Huoqu_status(req[1])
                for i in range(len(ztstatus)):
                    if req[1][0][i][0]=="B" or req[1][0][i][0]=="T":
                        tingfang="AGQJ"
                    elif req[1][0][i][0]=="C" or req[1][0][i][0]=="V":
                        tingfang="AGGB"
                    elif req[1][0][i][0]=="D":
                        tingfang="AGEU"
                    else:
                        tingfang="NW"
                    insert(tingfang,req[1][0][i],req[1][1][i],ztstatus[i],ticks)
                print ("yes")