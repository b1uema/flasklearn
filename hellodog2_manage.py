#!/usr/bin/python3

import os

from hellodog2 import create_app,db
from hellodog2.models import User,Role
from flask_script import Manager,Shell

str = 'development'
app = create_app(str)
manager = Manager(app)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command("shell",Shell(make_context=make_shell_context()))

if __name__== "__main__":
    manager.run()
