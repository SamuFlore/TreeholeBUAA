
SECRET_KEY = 'djkasndkjadi:das'

#数据库配置信息
HOSTNAME = '127.0.0.1'

PORT = '3306'

USERNAME = 'root'

PASSWORD = 'LiuJinYi102796'

DATABASE = 'treeholebuaa'

DB_URI ='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

#kqzmrpgdqfhrdiai

#邮箱配置
MAIL_SERVER = 'smtp.qq.com'

MAIL_PORT = 465

MAIL_USE_SSL = True

MAIL_USERNAME = 'chiai_chen@qq.com'

MAIL_PASSWORD = 'kqzmrpgdqfhrdiai'

MAIL_DEFAULT_SENDER = 'chiai_chen@qq.com'