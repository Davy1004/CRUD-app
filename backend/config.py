import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "CRUD_app_Thotnr")
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crud_app.db'
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    # Render provides DATABASE_URL as 'postgres://...', but SQLAlchemy 2.x
    # only accepts 'postgresql://'. Rewrite the scheme if needed.
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///crud_app.db')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
