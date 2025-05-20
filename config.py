import os

class Config:
    DEBUG = True
    HOST = '0.0.0.0'
    
    DB_USER = os.getenv('DB_USER', 'root') 
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'db') 
    DB_NAME = os.getenv('DB_NAME', 'meubanco')
    DB_PORT = os.getenv('DB_PORT', '3305')
    
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_ECHO = DEBUG
