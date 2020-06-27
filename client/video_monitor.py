import urllib.request,json,os
def Huoqu_status(ztxx):
    ztadds=ztxx[1]
    ztstatus=[]
    for url in ztadds:
        try:
            req=urllib.request.urlopen(url)
        #捕捉异常
        except TypeError as e:
            return e
        except urllib.error.HTTPError:
            ztstatus.append(404)
        else:
            ztstatus.append(req.getcode())
    return ztstatus
def Readjson(path):
    #读取json视频列表为对象
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        return e,None
    except json.decoder.JSONDecodeError as e:
        return e,None
    #拿到第一次嵌套的list
    else:
    #遍历拿到第二层嵌套的dict返回 
        list=data.get("list")
        ztname=[]
        ztadds=[]
        for dict in list:
            for x in dict:
                ztname.append(x)
                ztadds.append(dict.get(x))
                ztxx=[ztname,ztadds]
        return None,ztxx
if __name__ == "__main__":
    path="video_list.json"
    req=Readjson(path)
    if req[0] == None:
        ztstatus=Huoqu_status(req[1])
    else:
        print (req[0])
    for i in range(len(ztstatus)):
        print(req[1][0][i],req[1][1][i],ztstatus[i])