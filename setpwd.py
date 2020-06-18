import sys,os,json
sys.path.append('/root/python/Video_monitor')
from model.checkPasswd import User
from werkzeug.security import generate_password_hash
#from flask_login import UserMixin
user=input('输入用户名')
passwd=input('输入密码')
id=int(input('输入id'))

password_hash = generate_password_hash(passwd)
with open("Video_monitor/profiles.json", 'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[user] = [password_hash,
                                       id]
            f.write(json.dumps(profiles))
