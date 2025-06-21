from flask import Flask, g, session
import config
from exts import db, mail
from models import UserModel
from blueprints.auth import auth_bp
from blueprints.qa import qa_bp
from flask_migrate import Migrate

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)
#初始化数据库
db.init_app(app)
#初始化邮件
mail.init_app(app)

migrate = Migrate(app, db)


app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)

#钩子函数
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

@app.context_processor
def context_processor():
    return {"user": g.user}
    


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)