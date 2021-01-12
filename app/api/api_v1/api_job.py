import json
import logging
from datetime import datetime
from io import BytesIO
from fastapi import APIRouter, File, UploadFile

from app.core.config import settings
from app.utils.minio_handler import MinioHandler
from app.helpers.rabbitmq_helpers import rabbitmq_client


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    data_file = MinioHandler().get_instance().put_object(
        file_data=BytesIO(await file.read()),
        file_name=file.filename,
        content_type=file.content_type
    )
    return {"data_file": data_file}


@router.get("/change-job-status")
async def change_job_status():
    try:
        channel = rabbitmq_client.channel()
        queue_name = settings.RABBITMQ_JOB_CHANGE_QUEUE

        channel.queue_declare(queue=queue_name)

        data = {
            'message': 'Hello World ' + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(data))
        rabbitmq_client.return_channel(channel)

    except Exception as e:
        logger.debug(f'[x] Excep: {e}')

    return {"message": "Success"}
