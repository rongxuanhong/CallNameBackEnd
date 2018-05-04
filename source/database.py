from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

# engine = create_engine(
#     'sqlite:///database.db',
#     convert_unicode=True,
#     echo=True
# )
# 数据库信息配置的引擎
engine = create_engine(
    'mysql+pymysql://root:mysql@localhost:3306/projectdb?charset=utf8mb4&use_unicode=1',
    # pymysql:python3支持的 mysqldb 驱动
    convert_unicode=True,
    echo=True,  # 日志开关
)

# 定义会话，用于与数据库交流: 操作增删查改
# scoped_session :提供对session对象的域管理
db.session = scoped_session(
    sessionmaker(
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()  # 定义一个声明基类作为表关系映射类的基类(全局唯一实例)
Base.query = db.session.query_property()  # 查询对象(全局唯一实例)


def create_database():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.
    # Table对象都在MetaData集合中
    Base.metadata.create_all(bind=engine)
