import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


def get_list(text):
    return [item.strip() for item in text.split(',')]


class Settings(BaseSettings):
    API_PREFIX = '/sale-service'
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'Sale Service')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_URL = os.getenv('SQL_DATABASE_URL', '')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')
    MINIO_PORT = os.getenv('DEBUG', 9000)
    MINIO_URL = os.getenv('MINIO_URL', '')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', '')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', '')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '')
    RABBITMQ_URI = os.getenv('RABBITMQ_URI', '')
    RABBITMQ_JOB_EXCHANGE = os.getenv('RABBITMQ_JOB_EXCHANGE', 'jobs_exchange')
    RABBITMQ_JOB_CHANGE_QUEUE = os.getenv('RABBITMQ_JOB_CHANGE_QUEUE', 'job_change_queue')


settings = Settings()
