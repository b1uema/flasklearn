import os

#基类config中包含通用配置，子类分别定义专用的配置，在不同环境中的配置
class Config:
    SECRET_KEY = 'you not guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'acmdlnu@163.com'
    FLASKY_ADMIN = '578233897@qq.com'


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

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/test'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/test'

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}