import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '_qv3585a9i^w0dgdtcmj$osrna24$@+pzs5ga%h#efp&()mxg1'
    WTF_CSRF_ENABLED = True
    OPENAPI_URL_PREFIX = '/api/swagger'
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_VERSION = '3.22.0'


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True


config = {
    'dev': DevConfig,
    'prod': TestingConfig,
    'ProductionConfig': DevConfig,
}


FLASK_ADMIN_SWATCH = 'sketchy' #тема для админки https://bootswatch.com/
