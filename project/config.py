# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
mail_pass = "rqyersmdmtrzcsfh"
mail_address = "ad.coursehunter@gmail.com"


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    SECURE_KEY = 'hula-hula'
    SECURITY_PASSWORD_SALT = 'oh-baby-baby'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    # MAIL_USERNAME = "mingze.gao.gmz@gmail.com"
    # MAIL_PASSWORD = 'qtncejoibqbpgvfs'
    MAIL_USERNAME = mail_address
    MAIL_PASSWORD = mail_pass

    # mail accounts
    # MAIL_DEFAULT_SENDER = 'mingze.gao.gmz@gmail.com'
    MAIL_DEFAULT_SENDER = mail_address

    


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    """Production configuration."""
   # SECRET_KEY = 'my_precious'
    #DEBUG = False
    ###    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example' 
 #   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
 #  DEBUG_TB_ENABLED = False
  #    STRIPE_SECRET_KEY = 'foo'
 #   STRIPE_PUBLISHABLE_KEY = 'bar'
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    DEBUG_TB_ENABLED = False
