from flask import Flask
from flask import render_template
from flask import redirect
import sys,os
sys.path.append('/root/python/Video_monitor')
from flask_wtf.csrf import CsrfProtect
from model.checkPasswd import User
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user
from form.login_form import LoginForm
from flask import request,url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

# 设置密码
# @app.route('/setpwd')
# def setpwd():
#      User.password.setter('Osmond1689')
#      return '密码修改成功'

# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)

@app.route('/login',methods=('GET', 'POST'))
def login():
     form = LoginForm()
     if form.validate_on_submit():
        user_name = request.form.get('accountNumber', None)
        password = request.form.get('password', None)
        user = User(user_name)
        if user.verify_password(password):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main'))
     return render_template('login.html', title="Sign In", form=form)  

@app.route('/')
@app.route('/main')
@login_required
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

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')