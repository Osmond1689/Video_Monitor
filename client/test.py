import urllib.request
req=urllib.request.urlopen('http://eu.hongtaiwei.com/live/6-11.flv')
print(req.headers)
