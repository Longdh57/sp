import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


def get_list(text):
    return [item.strip() for item in text.split(',')]


class Settings(BaseSettings):
    API_PREFIX = '/api/v1'
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'Sale Service')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_URL = os.getenv('SQL_DATABASE_URL', '')


settings = Settings()
