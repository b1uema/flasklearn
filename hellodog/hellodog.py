from flask import Flask,make_response,render_template,session,redirect,url_for,flash
from flask_wtf import FlaskForm
from flask_mail import Mail,Message
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
import os
import pymysql
pymysql.install_as_MySQLdb()


from flask_script import Manager #使用flask_script

app = Flask(__name__)
#设置邮箱配置文件
app.config['MAIL_SERVER']="smtp.163.com"
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']='acmdlnu@163.com'
app.config['MAIL_PASSWORD']='dlnu521'
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='acmdlnu@163.com'
app.config['FLASKY_ADMIN'] = '578233897@qq.com'
mail = Mail(app)

app.config['SECRET_KEY']='you not guess'
bootstrap = Bootstrap(app)#使用Bootstrap模板


#配置数据库，db对象是sqlalchemy类的实例
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:12345@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)


#多线程异步发送邮件
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

#发送邮件
def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+''+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

#表单类
class NameForm(FlaskForm):
    name=StringField("what is your name?",validators=[Required()])
    submit=SubmitField("submit")

#定义role和user数据表模型
class Role(db.Model):
    __tablename__="roles" #数据库中使用表名

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)

    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>'%self.name

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>'%self.username

@app.route('/',methods=['GET','POST'])
def index():
    db.create_all()
    form=NameForm()
    if form.validate_on_submit():#如果表单接收到数据则返回true
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            #db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
            #flash('Look like you have changed your name!')

    return render_template("index.html",form=form,name=session.get('name'),known=session.get('known',False))


@app.route('/canshu')
def canshu():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

@app.route('/user/<name>') #动态路由
def user(name):
    return render_template("user.html",name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run(debug=True)
