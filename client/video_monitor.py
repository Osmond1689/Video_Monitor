import urllib.request,json,os
def Video_monitor(url):
    try:
        req=urllib.request.urlopen(url)
    #捕捉异常
    except TypeError as e:
        return 0,e
    except urllib.error.HTTPError:
        return 1,404
    else:
        return 1,req.getcode()
def Readjson(path):
    #读取json视频列表为对象
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        return e,None
    #拿到第一次嵌套的list
    else:
    #遍历拿到第二层嵌套的dict返回
        return None,data.get("list")
def main():
    print(1)
    path="video_list.json"   
    req=Readjson(path)
    # list=[1,]
    # if req[0] == None:
    #     list=req[1]
    # else:
    #     print (req[0])
    print(req)