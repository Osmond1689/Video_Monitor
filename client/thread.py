#!/usr/bin/env python3
import urllib.request,json,pymysql,sys,datetime,time,threading
sys.path.append("/root/Python/Video_Monitor")
from model.mariadb import insert
def hqxrdb(ztaddr,ztname):
    lock.acquire()
    global i
    url=ztaddr[i]
    name=ztname[i]
    ztstatus=0
    i=i+1
    lock.release()
    try:
        req=urllib.request.urlopen(url)
    #捕捉异常
    except TypeError as e:
        return e
    except urllib.error.HTTPError:
        ztstatus=404
    except urllib.error.URLError:
        ztstatus=404
    else:
        ztstatus=req.getcode()
    tick = datetime.datetime.now()
    ticks=tick.strftime('%Y-%m-%d %H:%M')
    if name[0]=="B" or name[0]=="T":
        tingfang="AGQJ"
    elif name[0]=="C" or name[0]=="V":
        tingfang="AGGB"
    elif name[0]=="D":
        tingfang="AGEU"
    else:
        tingfang="NW"
    insert(tingfang,name,url,ztstatus,ticks)
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
    #时间戳
    tick = datetime.datetime.now()
    ticks=tick.strftime('%Y-%m-%d %H:%M')
    i=0
    lock = threading.Lock()
    path="/root/Python/Video_Monitor/video_list.json"
    req=Readjson(path)
    if req[0] == None:
        ztaddr=req[1][1]
        ztname=req[1][0]
        threads=[]
        for j in range(len(ztaddr)):
            t=threading.Thread(target=hqxrdb,args=(ztaddr,ztname))
            threads.append(t)
        for thr in threads:
            thr.start()
        for thr in threads:
            if thr.is_alive():
                thr.join()
        print(("总耗时 %s 秒" % (datetime.datetime.now()-tick).seconds))
    else:
        print(req[0])
