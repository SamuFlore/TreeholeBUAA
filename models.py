from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), nullable = False)
    pswd = db.Column(db.String(1000), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    reg_time = db.Column(db.DateTime, default = datetime.now)

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captchas'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(100), nullable = False)
    captcha = db.Column(db.String(100), nullable = False)

class TreeholeModel(db.Model):
    __tablename__ = 'treeholes'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    create_time = db.Column(db.DateTime, default = datetime.now)

    author_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('UserModel', backref = "treeholes")#user有一个treeholes属性，返回所有该用户的帖子

class ReplyModel(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.Text, nullable = False)
    create_time = db.Column(db.DateTime, default = datetime.now)

    treehole_id = db.Column(db.Integer, db.ForeignKey('treeholes.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('UserModel', backref = "replies")
    treehole = db.relationship('TreeholeModel', backref = db.backref('replies'))
