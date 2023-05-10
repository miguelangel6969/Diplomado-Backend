import datetime
import os
import platform
from pathlib import Path, PureWindowsPath

from dotenv import load_dotenv

class Settings(object):

    def __init__(self):
        load_dotenv()
        minutes = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 15))
        self.JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=minutes)

        self.FLASK_ENV = os.getenv('FLASK_ENV')
        self.PROPAGATE_EXCEPTIONS = eval(os.getenv('PROPAGATE_EXCEPTIONS', "True").capitalize())
        self.JWT_ERROR_MESSAGE_KEY = os.getenv('JWT_ERROR_MESSAGE_KEY')
        self.API_PORT = os.getenv("API_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PASS = os.getenv("DB_PASS")

        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                                 'mssql+pyodbc://{user}:{pw}@{url}/{db}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'.format(
                                                     user=self.DB_USER,
                                                     pw=self.DB_PASS,
                                                     url=self.DB_HOST,
                                                     db=self.DB_NAME))
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.DEBUG = eval(os.getenv("API_DEBUG", "False").capitalize())
        self.JWT_SECRET_KEY = os.getenv("SECRET_KEY")
        self.JWT_HEADER_TYPE = 'JWT'
