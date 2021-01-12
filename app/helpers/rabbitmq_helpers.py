import logging

from app.helpers.fastapi_pika.fastapi_pika import Pika

_logger = logging.getLogger(__name__)

rabbitmq_client = Pika()


def init_rabbitmq(app, **kwargs):
    rabbitmq_client.init_app(app)
