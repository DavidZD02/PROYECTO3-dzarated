from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = 'clave'