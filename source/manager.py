from flask_script import Manager, Shell
from app import app
from flask_migrate import MigrateCommand

from base.models import Role

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))

# 1.python manager.py db migrate 迁移数据库 2.python manager.py db upgrade 来更新数据库
if __name__ == '__main__':
    manager.run()
