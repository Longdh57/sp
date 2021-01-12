import logging
import random
from datetime import datetime

from minio import Minio

from app.core.config import settings

logger = logging.getLogger()


class MinioHandler():
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not MinioHandler.__instance:
            MinioHandler.__instance = MinioHandler()
        return MinioHandler.__instance

    def __init__(self):
        self.minio_url = settings.MINIO_URL
        self.access_key = settings.MINIO_ACCESS_KEY
        self.secret_key = settings.MINIO_SECRET_KEY
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )

    def make_bucket(self, bucket_name=datetime.now().strftime("%d-%m-%Y")) -> str:
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        return bucket_name

    def presigned_get_object(self, bucket_name, object_name):
        url = self.client.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
        return url

    def check_file_name_exists(self, bucket_name, file_name):
        try:
            self.client.stat_object(bucket_name=bucket_name, object_name=file_name)
            return True
        except Exception as e:
            logger.debug(e)
            return False

    def put_object(self, file_data, file_name, content_type):
        try:
            bucket_name = self.make_bucket()
            object_name = file_name
            while self.check_file_name_exists(bucket_name=bucket_name, file_name=object_name):
                object_name = str(random.randint(1, 100000)) + file_name

            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=file_data,
                content_type=content_type,
                length=-1,
                part_size=10 * 1024 * 1024
            )
            url = self.presigned_get_object(bucket_name=bucket_name, object_name=object_name)
            data_file = {
                'bucket_name': bucket_name,
                'file_name': object_name,
                'url': url
            }
            return data_file
        except Exception as e:
            logger.warning(e)
            return None
