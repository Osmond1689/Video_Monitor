from flask import Flask
from flask import render_template,Response
from flask import redirect
from threading import Lock
import os,sys,logging,time,json,datetime
from client import video_monitor as vm
from model.mariadb import insert
from client.video_monitor import Readjson
# sys.path.append('/root/Python/Video_Monitor')
from flask_wtf.csrf import CSRFProtect
from model.checkPasswd import User
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user
from form.login_form import LoginForm
from flask import request,url_for,flash
from pyecharts import options as opts
from pyecharts.charts import Bar
from random import randrange
from pyecharts.charts import HeatMap
from model.mariadb import select,selectyc
from pyecharts.globals import WarningType
WarningType.ShowWarning = False

app = Flask(__name__)
csrf = CSRFProtect(app)
# csrf protection
# WTF_CSRF_ENABLED = False
app.config["SECRET_KEY"] = os.urandom(24)


# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

# @app.route('/setpwd')
# def setpwd():
#      User.password.setter('Osmond1689')
#      return '密码修改成功'

# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/login',methods=('GET', 'POST'))
def login():
    form = LoginForm()
    #日志
    # app.logger.info(form.validate_on_submit())
    if form.validate_on_submit():
       user_name = request.form.get('accountNumber', None)
       password = request.form.get('password', None)
    #    app.logger.info(user_name)
       user = User(user_name)
       if user.verify_password(password):
           login_user(user)
           return redirect(request.args.get('next') or url_for('main'))
        #    return redirect(url_for('main'))
    return render_template('login.html',form=form)  

@app.route('/')
@app.route('/main')
@login_required
# @csrf.exempt
def main():
    return render_template(
        'main.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#@app.route('/submit', methods=('GET', 'POST'))
#def submit():
#    form = MyForm()
#    if form.validate_on_submit():
#        return redirect('login')
#    return render_template('submit.html', form=form)
def bar_base() -> Bar:
    path="Video_Monitor/video_list.json"
    ztstatus=Readjson(path)
    now = datetime.datetime.now()
    zsf=now.minute%10
    time=[]
    if zsf>0:
        dqzsj=now-datetime.timedelta(minutes=zsf)
    else:
        dqzsj=now
    for j in range(720):
        tssj1=dqzsj-datetime.timedelta(minutes=1*(j-1))
        tssj=tssj1.strftime('%Y-%m-%d %H:%M')
        time.insert(0,tssj)
    # app.logger.info(time)
    data=select(time[0])
    # app.logger.info(data)
    name = ztstatus[1][0]
    newData=[]
    for value in range(len(data)):
        x=time.index(data[value].get('testtime'))
        y=name.index(data[value].get('ztname'))
        z=data[value].get('ztstatus')
        newData.append([x,y,z])
    data = [[d[0], d[1], d[2] or "-"] for d in newData]
    c = (
     HeatMap()
    .add_xaxis(xaxis_data=time)
    .add_yaxis(
        series_name="详情",
        yaxis_data=name,
        value=data,
        label_opts=opts.LabelOpts(
            is_show=True, color="#fff", position="bottom", horizontal_align="100%"
        ),
        
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True),minortick_opts=opts.MinorTickOpts(is_show=True,split_number=8),minorsplitkine_opts=opts.MinorSplitLineOpts(is_show=True))
    .set_global_opts(
        # tooltip_opts=opts.TooltipOpts(formatter='{a},{@time}:\n,{@[0]}'),
        # axistick_opts=opts.AxisTickOpts(is_show=False),
        visualmap_opts=opts.VisualMapOpts(is_show=True,is_piecewise=True,pos_left='center',orient='horizontal',pieces=[{"value":200,"label":'正常',"color":'green'},{"value":404,"label":'异常',"color":'Orange'},{"value":408,"label":'超时',"color":'grey'}]),
        legend_opts=opts.LegendOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=True,
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            minor_split_line_opts=opts.MinorSplitLineOpts(is_show=True),
        ),
        yaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=True,
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
        ),
        
    )
    )
    return c

@app.route('/barChart',methods=('GET', 'POST'))
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()

@app.route('/gwjk')
def gwjk():
    return render_template('gwjk.html')

@app.route('/gwjknew')
def gwjknew():
    return render_template('gwjknew.html')

@app.route('/ycbj',methods=('GET', 'POST'))
def get_ycbj():
    dqzsj=datetime.datetime.now()-datetime.timedelta(hours=2) 
    time=dqzsj.strftime('%Y-%m-%d %H:%M')
    data={}
    data['data']=selectyc(time)
    return Response(json.dumps(data), mimetype='application/json')

if __name__ == '__main__':
    #日志
    # app.debug = True
    # handler = logging.FileHandler('flask.log')
    # app.logger.addHandler(handler)
    app.run(debug=True, port=80, host='0.0.0.0')
    