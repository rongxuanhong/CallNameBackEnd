from config import DebugConfig
from flask import Flask
from flask_migrate import Migrate
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os.path import abspath, dirname, join, pardir
import sys
import sqlalchemy

# prevent python from writing *.pyc files / __pycache__ folders
sys.dont_write_bytecode = True

path_source = dirname(abspath(__file__))
path_parent = abspath(join(path_source, pardir))
if path_source not in sys.path:
    sys.path.append(path_source)

from database import db, create_database
from base.routes import login_manager


def register_extensions(app):
    # 相关框架功能初始化
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    """
    统一注册所有蓝图组织的文件夹
    :param app:
    :return:
    """
    for module_name in ('student_management','forms', 'ui', 'home', 'tables', 'data', 'additional', 'base'):
        module = import_module('{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_login_manager(app, User):
    @login_manager.user_loader #回调:用于从会话中存储的用户 ID 重新加载用户对象
    def user_loader(id):
        return db.session.query(User).filter_by(id=id).first()

    @login_manager.request_loader
    def request_loader(request):
        username = request.form.get('username')
        user = db.session.query(User).filter_by(username=username).first()
        return user if user else None


def configure_database(app):
    create_database()
    Migrate(app, db) # 数据库升级需要 1.flask db init 生成migrations directory 2.flask db migrate 3. flask db upgrade(需要加入版本控制)
                    #升级数据库，执行命令2，3

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    """
    日志捕获
    :param app:
    :return:
    """
    basicConfig(filename='error.log', level=DEBUG)
    logger = getLogger()
    logger.addHandler(StreamHandler())


def create_app(selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(DebugConfig)
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app) #注册蓝图 一般一个文件夹对应一个蓝图 url路径按文件来组织
    from base.models import User
    configure_login_manager(app, User)
    configure_database(app)
    configure_logs(app)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='localhost', port=8080, threaded=True)
