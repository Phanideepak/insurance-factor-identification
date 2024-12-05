import os
from decouple import config
from datetime import timedelta

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY','8add7febe7a37f3a0b7127b7b22fd45664f753c4e23081a2971109ffd6ac4b87')
    JWT_ALGORITHM = config('JWT_ALGORITHM', 'HS256')

class DevelopmentConfig(Config):
    # DEBUG = config('DEBUG', cast = bool)
    SQLALCHEMY_ECHO =True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1/ems?password=Alekya@736'
    SQLALCHEMY_BINDS = {
    'ems_mysql': 'mysql://root:@127.0.0.1/ems?password=Phani@dev',
    'students_mysql': 'mysql://root:@127.0.0.1/students?password=Phani@dev'
}
    
class QAConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict = {
    'dev': DevelopmentConfig,
    'qa': QAConfig,
    'prod': ProdConfig
}
