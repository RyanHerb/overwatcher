class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SECRET_KEY = 'prod'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://overwatcher:*********@localhost/overwatcher'

class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://overwatcher-dev:**********@localhost/overwatcher_dev'
    DEBUG = True

class TestingConfig(Config):
    SECRET_KEY = 'test'
    TESTING = True
    RENDER_TEMPLATES = False
