import os
basedir = os.path.abspath(os.path.dirname(__file__))

#基类config中包含通用配置，子类分别定义专用的配置，在不同环境中的配置
class Config:
    SECRET_KEY = 'you not guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True #自动提交变动
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'acmdlnu@163.com'
    FLASKY_ADMIN = 'acmdlnu@163.com'
    FLASKY_POSTS_PER_PAGE = 7
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 30


    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'acmdlnu@163.com'
    MAIL_PASSWORD = 'dlnu521'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/blog'  #数据库配置文件，与狗书的配置不同

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/blog'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/blog'

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}