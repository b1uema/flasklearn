from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  #确认用户账户
from flask import current_app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager




#定义role和user数据表模型
class Role(db.Model):
    __tablename__="roles" #数据库中使用表名

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)

    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>'%self.name


class User(UserMixin,db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    confirmed = db.Column(db.Boolean,default=False) #如果给表中的某个字段添加了default约束，当向表中插入记录数据时，该字段如果不指定值，则系统自动填充default指定的值
    #账户确定字段。TRUE为账户已经确定过，FAlse为账户未确定通过。

    #password的处理
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #关系
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>'%self.username

    def generate_confirmation_token(self, expiration=3600): #确认令牌生成函数，生成一个待验证的token值
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm')!=self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
