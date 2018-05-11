class Config(object):
    SECRET_KEY = 'key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/projectdb?charset=utf8mb4&use_unicode=1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True


permissions = [""]
