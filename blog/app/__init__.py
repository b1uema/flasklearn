from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
import pymysql
pymysql.install_as_MySQLdb()
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()



login_manager = LoginManager()  #声明对象
login_manager.session_protection='strong'  #安全防护等级
login_manager.login_view='auth.login' #蓝本加路由

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    #db.create_all()


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    #将蓝本在主程序注册
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth') #url_prefix 为可选参数，url前会加上/auth


    return app