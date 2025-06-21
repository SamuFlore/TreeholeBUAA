import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db
from werkzeug.security import check_password_hash
from flask import session

#验证前端数据，注册
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators = [Email(message="邮箱格式不合法")])
    captcha = wtforms.StringField(validators=[Length(min = 6, max = 6, message="验证码长度有误")])
    password = wtforms.StringField(validators=[Length(min = 8, max = 20, message="密码长度必须在8位到20位之间")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码输入不一致")])



    #邮箱是否被注册，验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email = email).first()
        if user:
            raise wtforms.ValidationError(message="邮箱已被注册")
    # 限制邮箱注册
    def validate_email_domain(self, field):
        email = field.data
        if not email.endswith("@buaa.edu.cn"):
            raise wtforms.ValidationError(message="请使用北京航空航天大学的邮箱注册")

    def validate_pswd_strength(self, field):
        pswd = field.data
        if not any(char.isdigit() for char in pswd):
            raise wtforms.ValidationError(message="密码必须包含数字，大写字母，小写字母")
        if not any(char.isupper() for char in pswd):
            raise wtforms.ValidationError(message="密码必须包含数字，大写字母，小写字母")
        if not any(char.islower() for char in pswd):
            raise wtforms.ValidationError(message="密码必须包含数字，大写字母，小写字母")
        
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_obj = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).order_by(EmailCaptchaModel.id.desc()).first()
        if not captcha_obj:
            raise wtforms.ValidationError(message="邮箱或验证码错误")
        else:
            db.session.delete(captcha_obj)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators = [Email(message="邮箱格式不合法")])
    password = wtforms.StringField(validators=[Length(min = 8, max = 20, message="密码长度必须在8位到20位之间")])

class TreeholeForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=1, max=100, message="标题长度必须在1到100之间")])
    content = wtforms.TextAreaField(validators=[Length(min=3, message="内容长度必须大于3")])

class ReplyForm(wtforms.Form):
    content = wtforms.TextAreaField(validators=[Length(min=3, message="内容长度必须大于3")])
    treehole_id = wtforms.IntegerField(validators=[InputRequired(message="请选择一个树洞")])

class UpdatePasswordForm(wtforms.Form):
    key = wtforms.IntegerField(validators=[InputRequired(message="请先登录")])
    old_password = wtforms.StringField(validators=[Length(min=8, max=20, message="密码长度必须在8位到20位之间")])
    new_password = wtforms.StringField(validators=[Length(min=8, max=20, message="密码长度必须在8位到20位之间")])
    new_password_confirm = wtforms.StringField(validators=[EqualTo("new_password", message="两次密码输入不一致")])

    def validate_old_password(self, field):
        old_password = field.data
        key = self.key.data
        user = UserModel.query.get(key)
        if not check_password_hash(user.pswd, old_password):
            raise wtforms.ValidationError(message="旧密码错误")
        
    def validate_new_password(self, field):
            new_password = field.data
            if not any(char.isdigit() for char in new_password):
                raise wtforms.ValidationError(message="密码必须包含数字，大写字母，小写字母")
            if not any(char.isupper() for char in new_password):
                raise wtforms.ValidationError(message="密码必须包含数字，大写字母，小写字母")
            if not any(char.islower() for char in new_password):
                raise wtforms.ValidationError(message="密码必须包含数字，大写字母，小写字母")
            if new_password == self.old_password.data:
                raise wtforms.ValidationError(message="新密码不能与旧密码相同")
            
class UpdateUsernameForm(wtforms.Form):
    key = wtforms.IntegerField(validators=[InputRequired(message="请先登录")])
    email = wtforms.StringField(validators = [Email(message="邮箱格式不合法")])
    captcha = wtforms.StringField(validators=[Length(min = 6, max = 6, message="验证码长度有误")])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email = email).first()
        if not user:
            raise wtforms.ValidationError(message="邮箱未注册")
        elif UserModel.query.filter_by(id = session.get("user_id")).first().email != email:
            raise wtforms.ValidationError(message="邮箱错误")
        
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_obj = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).order_by(EmailCaptchaModel.id.desc()).first()
        if not captcha_obj:
            raise wtforms.ValidationError(message="邮箱或验证码错误")
        else:
            db.session.delete(captcha_obj)
            db.session.commit()
    
    