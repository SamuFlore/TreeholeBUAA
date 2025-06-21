from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from models import UserModel, EmailCaptchaModel, TreeholeModel
from exts import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import string
import random
from .forms import RegisterForm, LoginForm, UpdatePasswordForm, UpdateUsernameForm
from decorators import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email = email).first()
            if not user:
                print('用户不存在')
                return redirect(url_for('auth.login'))
            if check_password_hash(user.pswd, password):
                #cookie只能存放少量数据
                #cookie一般用来保存登录授权的东西
                session['user_id'] = user.id
                return redirect('/')
            else:
                print('密码错误')
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))
        
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/manage')
def manage():
    return render_template('manage.html')
    

#GET：从服务器获取数据，POST：向服务器提交数据
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        #验证
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            table = (string.ascii_lowercase + string.digits) * 8
            username = ''.join(random.sample(table, 8))
            user = UserModel(username = username, pswd = generate_password_hash(password), email = email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))
        
    

@auth_bp.route('/captcha')
def send_captcha():
    email = request.args.get('email')
    src = string.digits * 6
    captcha = "".join(random.sample(src, 6))
    message = Message(subject='TreeholeBUAA验证码', recipients = [email], body=f'[TreeholeBUAA]\n{captcha}是您的验证码，请妥善保管。')
    mail.send(message)
    email_captcha = EmailCaptchaModel(email = email, captcha = captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code':200,'msg':'', 'data': None})

@auth_bp.route('/update/pswd' , methods=['GET', 'POST'])
@login_required
def update_pswd():
    if request.method == 'GET':
        return render_template('update_pswd.html')
    else:
        form = UpdatePasswordForm(request.form)
        if form.validate():
           key = session.get('user_id')
           user = UserModel.query.get(key)
           new_password = form.new_password.data
           user.pswd = generate_password_hash(new_password)
           db.session.commit()
           session.clear()
           return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.update_pswd'))
        
@auth_bp.route('/update/username', methods=['GET', 'POST'])
@login_required
def update_username():
    if request.method == 'GET':
        return render_template('update_username.html')
    else:
        form = UpdateUsernameForm(request.form)
        if form.validate():
            key = session.get('user_id')
            user = UserModel.query.get(key)
            table = (string.ascii_lowercase + string.digits) * 8
            new_username = ''.join(random.sample(table, 8))
            user.username = new_username
            db.session.commit()
            session.clear()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.manage'))

@auth_bp.route('/manage/treeholes', methods=['GET'])
@login_required
def manage_treeholes():
    user = UserModel.query.get(session.get('user_id'))
    return render_template('my_treeholes.html', treeholes = user.treeholes[::-1])

