from flask_script import Manager, Server


from firstproject import app, db, User,Post, Tag



manager = Manager(app)
manager.add_command("server", Server())



@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag)

if __name__ == "__main__":
    manager.run()